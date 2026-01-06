
import sys
import glob
import os

sys.path.append("..")
# from nm1550.fdtd_solver import fdtd_solver
from nm1550.variables import *
from nm1550.fdtd_solver_convergence import fdtd_solver
from evaluate import evaluate


def Recover_data(sim_name,span):
    files = sorted(glob.glob(f"chunks/{sim_name}*.npz"))
    print(f"recovering data with span length: {len(span)}")
    if files:  # make sure the list is not empty
        last_file = files[-1]
        Zero_counter=0
        with np.load(last_file) as data:
                T_cross_values=data["T_cross_values"]    
                T_bar_values=data["T_bar_values"]
                Span=data["Span"]
                #count results that were ommitted    
                Zero_counter = len(span) -len(T_cross_values)
                #save to a npz file
                np.savez(f'data/{sim_name}.npz',Span=Span,T_cross_values=T_cross_values, T_bar_values=T_bar_values)
                
                #delete previous chunks

        number_of_deleted=Delete_chunks(sim_name=sim_name)        
        print(f"Missing Results: {Zero_counter} and  Deleted Chunks: {number_of_deleted} in summ they must be {len(span)}") 

    else:
        last_file = None
        print("No files found")
        Zero_counter=0
        #As there is n
    #Count every zero in Result values
   
    return Zero_counter


def Delete_chunks(sim_name):
    files = sorted(glob.glob(f"chunks/{sim_name}*.npz"))
    for f in files:
        os.remove(f)
    return len(files)





def PML_distance_z_span(sim,RUN_AGAIN=False,args=None):    
    defaults = {
        "z_span": None,
        "y_span": None,
        "mesh_accuracy": None,
        "port_size":None,
        "TM_mode":None,

    }
    if args is not None:
        defaults.update(args)
    z_span = defaults["z_span"]
    y_span = defaults["y_span"]
    mesh_accuracy = defaults["mesh_accuracy"]
    port_size = defaults["port_size"]
    TM_mode = defaults["TM_mode"]


    log = setup_logger("pml_distance_z_span", "logging/pml_distance_z_span.log")
    log.info(f"Starting with args {defaults}")

    wg_length=opt_wg_length
    wg_width=1.6e-6
    width_ridge=opt_width_ridge
    mmi_length=opt_mmi_length
    taper_width=opt_taper_width
    taper_width_in=taper_width
    delta_y=0
    T_cross_values= []
    T_bar_values= []
    starting_point=0

    if TM_mode!=None:
        SIMULATION_NAME="PML_distance_z_span_TM_MODE"
    else:
        SIMULATION_NAME="PML_distance_z_span"

    if RUN_AGAIN:
        #if run again is used -> recover data and find last itteration, where to start.
        Recover_data(SIMULATION_NAME,span=z_span)
        if os.path.exists(f"data/{SIMULATION_NAME}.npz"):
            check_data=np.load(f'data/{SIMULATION_NAME}.npz', allow_pickle=True)
            #load Results
            T_cross_values=list(check_data['T_cross_values'])
            T_bar_values=list(check_data['T_bar_values'])
            starting_point=len(T_cross_values)

            if(starting_point==len(z_span)):
                starting_point=0
                T_cross_values=[]
                T_bar_values=[]
            z_span=z_span[starting_point:]
            print(f"starting for loop with z_span: starting point: {starting_point} and len of z span: {len(z_span)}")            

    #run simmulation 
    try:
        for ii,span in enumerate(z_span):
            T_cross,T_bar,E_lateral=fdtd_solver(sim=sim,filename=filename_fdtd,width_ridge=width_ridge,
                    mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,mesh_accuracy=mesh_accuracy,delta_y=delta_y,FDTD_z_span=span,FDTD_y_span=y_span,Port_size=port_size,TM_MODE=TM_mode)
            # Get new results or append to previous( if starting_point!= 0)
        
            T_cross_values.append(T_cross)
            T_bar_values.append(T_bar)
            log.info(f"T_cross:{T_cross},T_bar: {T_bar}")
            np.savez(f'chunks/{SIMULATION_NAME}_{ii+starting_point}_itteration.npz',Span=z_span,T_cross_values=T_cross_values, T_bar_values=T_bar_values)
       
        else:
            np.savez(f'data/{SIMULATION_NAME}.npz',Span=z_span,T_cross_values=T_cross_values, T_bar_values=T_bar_values)
            Delete_chunks(SIMULATION_NAME)      
                   
                                   
    
    except Exception as e:        
        log.error(f"An error has occured {e}, saving T_cross_value (len: {len(T_cross_values)}) and T_bar values({len(T_bar_values)}), with itteration files ")
        Zero_counter=Recover_data(sim_name=SIMULATION_NAME,span=z_span) 
        log.info(f"Recovered dataset from chunks with {Zero_counter} unfinished sweep points and deleted leftover chunks")




def PML_distance_y_span(sim,RUN_AGAIN=False,args=None):
    defaults = {
        "z_span": None,
        "y_span": None,
        "mesh_accuracy": None,
        "port_size":None,
        "TM_mode":None,

    }
    if args is not None:
        defaults.update(args)
    z_span = defaults["z_span"]
    y_span = defaults["y_span"]
    mesh_accuracy = defaults["mesh_accuracy"]
    port_size = defaults["port_size"]
    TM_mode = defaults["TM_mode"]


    log = setup_logger("pml_distance_y_span", "logging/pml_distance_y_span.log")
    log.info(f"Starting with args {defaults}")

    wg_length=opt_wg_length
    wg_width=1.6e-6
    width_ridge=opt_width_ridge
    mmi_length=opt_mmi_length
    taper_width=opt_taper_width
    taper_width_in=taper_width
    delta_y=0
    T_cross_values= []
    T_bar_values= []
    starting_point=0
    
    if TM_mode!=None:
        SIMULATION_NAME="PML_distance_y_span_TM_MODE"
    else:
        SIMULATION_NAME="PML_distance_y_span"


    if RUN_AGAIN:
        #if run again is used -> recover data and find last itteration, where to start.
        Recover_data(SIMULATION_NAME,span=y_span)
        if os.path.exists(f"data/{SIMULATION_NAME}.npz"):
            check_data=np.load(f'data/{SIMULATION_NAME}.npz', allow_pickle=True)
            #load Results
            T_cross_values=list(check_data['T_cross_values'])
            T_bar_values=list(check_data['T_bar_values'])
            starting_point=len(T_cross_values)

            if(starting_point==len(y_span)):
                starting_point=0
                T_cross_values=[]
                T_bar_values=[]
            y_span=y_span[starting_point:]
            print(f"starting for loop with y_span: {len(y_span)}")
    #run simmulation 
    try:
        for ii,span in enumerate(y_span):
            T_cross,T_bar,E_lateral=fdtd_solver(sim=sim,filename=filename_fdtd,width_ridge=width_ridge,
                    mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,mesh_accuracy=mesh_accuracy,delta_y=delta_y,FDTD_y_span=span,FDTD_z_span=z_span,Port_size=port_size,TM_MODE=TM_mode)
            # Get new results or append to previous( if starting_point!= 0)
        
            T_cross_values.append(T_cross)
            T_bar_values.append(T_bar)
            log.info(f"T_cross:{T_cross},T_bar: {T_bar}")
            np.savez(f'chunks/{SIMULATION_NAME}_{ii+starting_point}_itteration.npz',Span=y_span,T_cross_values=T_cross_values, T_bar_values=T_bar_values)
       
        else:
            np.savez(f'data/{SIMULATION_NAME}.npz',Span=y_span,T_cross_values=T_cross_values, T_bar_values=T_bar_values)
            Delete_chunks(SIMULATION_NAME)                                     
    
    except Exception as e:        
        log.error(f"An error has occured {e}, saving T_cross_value (len: {len(T_cross_values)}) and T_bar values({len(T_bar_values)}), with itteration files ")
        Zero_counter=Recover_data(sim_name=SIMULATION_NAME,span=y_span) 
        log.info(f"Recovered dataset from chunks with {Zero_counter} unfinished sweep points and deleted leftover chunks")


def Mesh_accuracy(sim,RUN_AGAIN=False,args=None):

    defaults = {
        "z_span": None,
        "y_span": None,
        "mesh_accuracy": None,
        "port_size":None,
        "TM_mode":None,

    }
    if args is not None:
        defaults.update(args)
    z_span = defaults["z_span"]
    y_span = defaults["y_span"]
    mesh_accuracy = defaults["mesh_accuracy"]
    port_size = defaults["port_size"]
    TM_mode = defaults["TM_mode"]



    mesh_span=np.linspace(1,6,6)
    log = setup_logger("mesh_accuracy", "logging/mesh_accuracy.log")
    log.info(f"Starting with args {defaults}")

    wg_length=opt_wg_length
    wg_width=1.6e-6
    width_ridge=opt_width_ridge
    mmi_length=opt_mmi_length
    taper_width=opt_taper_width
    taper_width_in=taper_width
    delta_y=0
    T_cross_values= []
    T_bar_values= []
    starting_point=0

    
    if TM_mode!=None:
        SIMULATION_NAME="Mesh_accuracy_TM_MODE"
    else:
        SIMULATION_NAME="Mesh_accuracy"


    if RUN_AGAIN:
        #if run again is used -> recover data and find last itteration, where to start.
        Recover_data(SIMULATION_NAME,span=mesh_span)
        if os.path.exists(f"data/{SIMULATION_NAME}.npz"):
            check_data=np.load(f'data/{SIMULATION_NAME}.npz', allow_pickle=True)
            #load Results
            T_cross_values=list(check_data['T_cross_values'])
            T_bar_values=list(check_data['T_bar_values'])
            starting_point=len(T_cross_values)
            if(starting_point==len(mesh_span)):
                starting_point=0
                T_cross_values=[]
                T_bar_values=[]
            mesh_span=mesh_span[starting_point:]
            print(f"starting for loop with mesh_span: {len(mesh_span)}")
    #run simmulation 
    try:
        for ii,mesh in enumerate(mesh_span):
            T_cross,T_bar,E_lateral=fdtd_solver(sim=sim,filename=filename_fdtd,width_ridge=width_ridge,
                    mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,mesh_accuracy=mesh,delta_y=delta_y,FDTD_y_span=y_span,FDTD_z_span=z_span,Port_size=port_size,TM_MODE=TM_mode)
            # Get new results or append to previous( if starting_point!= 0)
            T_cross_values.append(T_cross)
            T_bar_values.append(T_bar)
            log.info(f"T_cross:{T_cross},T_bar: {T_bar}")
            np.savez(f'chunks/{SIMULATION_NAME}_{ii+starting_point}_itteration.npz',Span=y_span,T_cross_values=T_cross_values, T_bar_values=T_bar_values)
       
        else:
            np.savez(f'data/{SIMULATION_NAME}.npz',Span=mesh_span,T_cross_values=T_cross_values, T_bar_values=T_bar_values)
            Delete_chunks(SIMULATION_NAME)                                     
    
    except Exception as e:        
        log.error(f"An error has occured {e}, saving T_cross_value (len: {len(T_cross_values)}) and T_bar values({len(T_bar_values)}), with itteration files ")
        Zero_counter=Recover_data(sim_name=SIMULATION_NAME,span=mesh_span) 
        log.info(f"Recovered dataset from chunks with {Zero_counter} unfinished sweep points and deleted leftover chunks")


def Port_size(sim,RUN_AGAIN=False,args=None):
    defaults = {
        "z_span": None,
        "y_span": None,
        "mesh_accuracy": None,
        "port_size":None,
        "TM_mode":None,
        

    }
    if args is not None:
        defaults.update(args)
    z_span = defaults["z_span"]
    y_span = defaults["y_span"]
    mesh_accuracy = defaults["mesh_accuracy"]
    port_size = defaults["port_size"]
    TM_mode = defaults["TM_mode"]


    log = setup_logger("port_size", "logging/port_size.log")
    log.info(f"Starting with args {defaults}")

    port_distance=minimal_output_distance+opt_taper_width
    max_port_size=port_distance
    min_port_size=opt_wg_width+1e-6
    port_span=np.linspace(min_port_size,max_port_size,10)
    log.info(f" And port_span {port_span}")


    wg_length=opt_wg_length
    wg_width=1.6e-6
    width_ridge=opt_width_ridge
    mmi_length=opt_mmi_length
    taper_width=opt_taper_width
    taper_width_in=taper_width
    delta_y=0
    T_cross_values= []
    T_bar_values= []
    starting_point=0
    
    if TM_mode!=None:
        SIMULATION_NAME="Port_size_TM_MODE"
    else:
        SIMULATION_NAME="Port_size"

    if RUN_AGAIN:
        #if run again is used -> recover data and find last itteration, where to start.
        Recover_data(SIMULATION_NAME,span=port_span)
        if os.path.exists(f"data/{SIMULATION_NAME}.npz"):
            check_data=np.load(f'data/{SIMULATION_NAME}.npz', allow_pickle=True)
            #load Results
            T_cross_values=list(check_data['T_cross_values'])
            T_bar_values=list(check_data['T_bar_values'])
            starting_point=len(T_cross_values)
            if(starting_point==len(port_span)):
                starting_point=0
                T_cross_values=[]
                T_bar_values=[]
            port_span=port_span[starting_point:]
    #run simmulation 
    try:
        for ii,size in enumerate(port_span):
            T_cross,T_bar,E_lateral=fdtd_solver(sim=sim,filename=filename_fdtd,width_ridge=width_ridge,
                    mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,mesh_accuracy=mesh_accuracy,delta_y=delta_y,Port_size=size,FDTD_y_span=y_span,FDTD_z_span=z_span,TM_MODE=TM_mode)
            # Get new results or append to previous( if starting_point!= 0)
        
            T_cross_values.append(T_cross)
            T_bar_values.append(T_bar)
            log.info(f"T_cross:{T_cross},T_bar: {T_bar}")
            np.savez(f'chunks/{SIMULATION_NAME}_{ii+starting_point}_itteration.npz',Span=port_span,T_cross_values=T_cross_values, T_bar_values=T_bar_values)
       
        else:
            np.savez(f'data/{SIMULATION_NAME}.npz',Span=port_span,T_cross_values=T_cross_values, T_bar_values=T_bar_values)
            Delete_chunks(SIMULATION_NAME)                                     
    
    except Exception as e:        
        log.error(f"An error has occured {e}, saving T_cross_value (len: {len(T_cross_values)}) and T_bar values({len(T_bar_values)}), with itteration files ")
        Zero_counter=Recover_data(sim_name=SIMULATION_NAME,span=port_span) 
        log.info(f"Recovered dataset from chunks with {Zero_counter} unfinished sweep points and deleted leftover chunks")




if __name__=="__main__":
    # filename="../nm1550/mmi_1x2_fdtd"





    ############ TE MODE ################
    #  1) distance to PML (in z direction)     

    z_span=np.linspace(1.8e-6,2.5e-6,10)

    args = {
        "z_span": z_span,
        "y_span": None,
        "mesh_accuracy": 3,
        "port_size":None,
        "TM_mode":None, 

    }

    PML_distance_z_span(sim=lumapi.FDTD(),RUN_AGAIN=False, args=args)
   
    #   2) distance to PML (in y direction)

    min_y_span=opt_width_ridge+2e-6
    max_y_span=opt_width_ridge+6e-6
    
    y_span=np.linspace(min_y_span,max_y_span,10)

    args = {
        "z_span": None,
        "y_span": y_span,
        "mesh_accuracy": 3,
        "port_size": None,
        "TM_mode":None,


    }

    
    PML_distance_y_span(sim=lumapi.FDTD(),RUN_AGAIN=False,args=args)

    #   3) Mesh Accuracy from 1 to 6

    args = {
        "z_span": None,
        "y_span": None,
        "mesh_accuracy": None,  #default from 1 to 6 (change span inside the function)
        "port_size":None,
        "TM_mode":None

    }
    Mesh_accuracy(sim=lumapi.FDTD(),RUN_AGAIN=False,args=args)


    # #   4) Port size
    args = {
        "z_span": None,
        "y_span": None,
        "mesh_accuracy": 3, 
        "port_size":None,    #default from wg_width+0.5e-6 to half the distance between output ports(change span inside the function)
        "TM_mode":None,
    }
    Port_size(sim=lumapi.FDTD(),RUN_AGAIN=False,args=args)
       
       
       
       
       
    ############ TM MODE ################

    #  1) distance to PML (in z direction)     

    z_span=np.linspace(1.8e-6,2.5e-6,10)+0.5e-6

    args = {
        "z_span": z_span,
        "y_span": None,
        "mesh_accuracy": 3,
        "port_size":None,
        "TM_mode":True, 

    }

    PML_distance_z_span(sim=lumapi.FDTD(),RUN_AGAIN=False, args=args)
    # Evaluate achieved results
    evaluate(datafile="data/dataset_PML_distance_z_span")
   
    #   2) distance to PML (in y direction)

    min_y_span=opt_width_ridge+2e-6
    max_y_span=opt_width_ridge+6e-6
    
    y_span=np.linspace(min_y_span,max_y_span,10)

    args = {
        "z_span": None,
        "y_span": y_span,
        "mesh_accuracy": 3,
        "port_size": None,
        "TM_mode":True,

    }

    
    PML_distance_y_span(sim=lumapi.FDTD(),RUN_AGAIN=False,args=args)

    #   3) Mesh Accuracy from 1 to 6

    args = {
        "z_span": None,
        "y_span": None,
        "mesh_accuracy": None,  #default from 1 to 6 (change span inside the function)
        "port_size":None,
        "TM_mode":True,

    }
    Mesh_accuracy(sim=lumapi.FDTD(),RUN_AGAIN=False,args=args)


    # #   4) Port size
    args = {
        "z_span": None,
        "y_span": None,
        "mesh_accuracy": 3, 
        "port_size":None,    #default from wg_width+0.5e-6 to half the distance between output ports(change span inside the function)
        "TM_mode":True,
    }
    Port_size(sim=lumapi.FDTD(),RUN_AGAIN=False,args=args)