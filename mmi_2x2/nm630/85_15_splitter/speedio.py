from variables import *
from fdtd_solver import *
from data_analyser import data_analysis
import sys
import glob
import os

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Create necessary directories relative to script location
os.makedirs(os.path.join(SCRIPT_DIR, "chunks"), exist_ok=True)
os.makedirs(os.path.join(SCRIPT_DIR, "data"), exist_ok=True)
os.makedirs(os.path.join(SCRIPT_DIR, "logging"), exist_ok=True)

log = setup_logger("speedio", "logging/speedio.log")




#Recover data from chunks
def Recover_data(sim_name,span):
    log.info(f"Recovering data for {sim_name}")

    chunks_dir = os.path.join(SCRIPT_DIR, "chunks")
    data_dir = os.path.join(SCRIPT_DIR, "data")
    files = sorted(glob.glob(os.path.join(chunks_dir, f"{sim_name}*.npz")))
    if files:  # make sure the list is not empty
        log.info(f"Recovering data: Files found")
        last_file = files[-1]
        Zero_counter=0
        with np.load(last_file) as data:
                T_cross_values=data["T_cross_values"]    
                T_bar_values=data["T_bar_values"]
                E_lateral_values=data["E_lateral_values"]
                Span=data["Span"]
                log.info(f"Recovering data: Values are found {len(T_cross_values)}")

                #count results that were ommitted    
                Zero_counter = len(span) -len(T_cross_values)
                #save to a npz file
                log.info(f"Recovering data: Saving files")
                np.savez(os.path.join(data_dir, f'{sim_name}.npz'),Span=Span,T_cross_values=T_cross_values, T_bar_values=T_bar_values,E_lateral_values=E_lateral_values)
                log.info(f"Recovering data: Files saved")

        log.info(f"Recovering data: Delete previous Chunks")
        number_of_deleted=Delete_chunks(sim_name=sim_name)   
        log.info(f"Recovering data: Chunks were deleted")

        log.info(f"Missing Results: {Zero_counter} and  Deleted Chunks: {number_of_deleted} in summ they must be {len(span)}") 

    else:
        last_file = None
        log.info("Recovering data:No files found in the recovery")
        Zero_counter=0
        #As there is n
    #Count every zero in Result values
   
    return Zero_counter

#Delete Recovered chunks
def Delete_chunks(sim_name):
    chunks_dir = os.path.join(SCRIPT_DIR, "chunks")
    files = sorted(glob.glob(os.path.join(chunks_dir, f"{sim_name}*.npz")))
    for f in files:
        os.remove(f)
    return len(files)





###1) Y_sweep of MMI
def Y_sweep(sim,span,args=None,RUN_AGAIN=False):
    defaults = {
        "y":None,
        "mmi_length": None,
        "twist_angle": None,
    }
    if args is not None:
        defaults.update(args)

        y = defaults["y"]
        mmi_length = defaults["mmi_length"]
        twist_angle = defaults["twist_angle"]


    SIMULATION_NAME="y_sweep"
    filename = os.path.join(SCRIPT_DIR, "speedio_fdtd_mmi")
    wg_length=10e-6
    wg_width=0.4e-6
    width_ridge=5.1e-6
    taper_width=1e-6
    taper_width_in=taper_width

    delta_y=0e-6
    Radius=80e-6
    #define ratio
    ratio=85/100
    #define cut angle at the ends of MMI core section
    cut_angle=90   #(degrees)  90==no cut
    mesh_accuracy=3
    
    #define middle section width
    T_cross_values=[]
    T_bar_values=[]
    E_lateral_values=[]

    log.info(f"Starting Y_sweep \n span: {span}, \n width_ridge: {width_ridge}, \n mmi_length:{mmi_length},\n taper_width={taper_width},\n ratio:{ratio}")
    
    data_dir = os.path.join(SCRIPT_DIR, "data")
    chunks_dir = os.path.join(SCRIPT_DIR, "chunks")
    starting_point=0

    if RUN_AGAIN:
        log.info(f"RUN AGAIN option is activated, first start recoverering data")

        #if run again is used -> recover data and find last itteration, where to start.
        Recover_data(SIMULATION_NAME,span=span)
        data_file = os.path.join(data_dir, f"{SIMULATION_NAME}.npz")
        if os.path.exists(data_file):
            check_data=np.load(data_file, allow_pickle=True)
            #load Results
            T_cross_values=list(check_data['T_cross_values'])
            T_bar_values=list(check_data['T_bar_values'])
            E_lateral_values=list(check_data['E_lateral_values'])
            starting_point=len(T_cross_values)

            if(starting_point==len(span)):
                starting_point=0
                T_cross_values=[]
                T_bar_values=[]
                E_lateral_values=[]
            span=span[starting_point:]

    #run simmulation 
    try:
        for ii,y in enumerate(span):
            T_cross,T_bar,E_lateral=fdtd_solver(sim=lumapi.FDTD(),Radius=Radius,filename=filename,wg_length=wg_length,wg_width=wg_width,width_ridge=width_ridge,
                mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,ratio=ratio,y=y,mesh_accuracy=mesh_accuracy,cut_angle=cut_angle,delta_y=delta_y,twist_angle=None,sweep_name=SIMULATION_NAME)
            log.info(f"T_cross: {T_cross}, T_bar: {T_bar}")
            # Get new results or append to previous( if starting_point!= 0)
        
            T_cross_values.append(T_cross)
            T_bar_values.append(T_bar)
            E_lateral_values.append(E_lateral)
            log.info(f"save chunks to {os.path.join(chunks_dir, f'{SIMULATION_NAME}_{ii+starting_point}_itteration.npz')}")

            np.savez(os.path.join(chunks_dir, f'{SIMULATION_NAME}_{ii+starting_point}_itteration.npz'),Span=span,T_cross_values=T_cross_values, T_bar_values=T_bar_values,E_lateral_values=E_lateral_values)
            log.info(f"Files were saved")
        else:
            log.info(f"save whole dataset to {os.path.join(data_dir, f'{SIMULATION_NAME}.npz')}")

            np.savez(os.path.join(data_dir, f'{SIMULATION_NAME}.npz'),Span=span,T_cross_values=T_cross_values, T_bar_values=T_bar_values,E_lateral_values=E_lateral_values)
            Delete_chunks(SIMULATION_NAME)      
                   
                                   
    
    except Exception as e:        
        log.error(f"An error has occured {e}, saving T_cross_value (len: {len(T_cross_values)}) and T_bar values({len(T_bar_values)}) and E_lateral_values ({len(E_lateral_values)}), with itteration files ")
        Zero_counter=Recover_data(sim_name=SIMULATION_NAME,span=span) 
        log.info(f"Recovered dataset from chunks with {Zero_counter} unfinished sweep points and deleted leftover chunks")




def Length_sweep(sim,span,args=None,RUN_AGAIN=False):

    defaults = {
        "y":None,
        "mmi_length": None,
        "twist_angle": None,
    }
    if args is not None:
        defaults.update(args)

        y = defaults["y"]
        mmi_length = defaults["mmi_length"]
        twist_angle = defaults["twist_angle"]

    SIMULATION_NAME="length_sweep"
    filename = os.path.join(SCRIPT_DIR, "speedio_fdtd_mmi")
    wg_length=10e-6
    wg_width=0.4e-6
    width_ridge=5.1e-6
    taper_width=1e-6
    taper_width_in=taper_width
    delta_y=0e-6
    Radius=80e-6
    #define ratio
    ratio=85/100
    #define cut angle at the ends of MMI core section
    cut_angle=90   #(degrees)  90==no cut
    mesh_accuracy=3
    
    #define middle section width
    T_cross_values=[]
    T_bar_values=[]
    E_lateral_values=[]

    log.info(f"Starting {SIMULATION_NAME} \n span: {span}, \n width_ridge: {width_ridge}, \n mmi_length:{mmi_length},\n taper_width={taper_width},\n y:{y},\n ratio:{ratio}")
    
    data_dir = os.path.join(SCRIPT_DIR, "data")
    chunks_dir = os.path.join(SCRIPT_DIR, "chunks")
    starting_point=0

    if RUN_AGAIN:
        log.info(f"RUN AGAIN option is activated, first start recoverering data")

        #if run again is used -> recover data and find last itteration, where to start.
        Recover_data(SIMULATION_NAME,span=span)
        data_file = os.path.join(data_dir, f"{SIMULATION_NAME}.npz")
        if os.path.exists(data_file):
            check_data=np.load(data_file, allow_pickle=True)
            #load Results
            T_cross_values=list(check_data['T_cross_values'])
            T_bar_values=list(check_data['T_bar_values'])
            E_lateral_values=list(check_data['E_lateral_values'])
            starting_point=len(T_cross_values)

            if(starting_point==len(span)):
                starting_point=0
                T_cross_values=[]
                T_bar_values=[]
                E_lateral_values=[]
            span=span[starting_point:]

    #run simmulation 
    try:
        for ii,mmi_length in enumerate(span):
            T_cross,T_bar,E_lateral=fdtd_solver(sim=sim,Radius=Radius,filename=filename,wg_length=wg_length,wg_width=wg_width,width_ridge=width_ridge,
                mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,ratio=ratio,y=y,mesh_accuracy=mesh_accuracy,cut_angle=cut_angle,delta_y=delta_y,twist_angle=None,sweep_name=SIMULATION_NAME)
            log.info(f"T_cross: {T_cross}, T_bar: {T_bar}")
            # Get new results or append to previous( if starting_point!= 0)
        
            T_cross_values.append(T_cross)
            T_bar_values.append(T_bar)
            E_lateral_values.append(E_lateral)
            log.info(f"save chunks to {os.path.join(chunks_dir, f'{SIMULATION_NAME}_{ii+starting_point}_itteration.npz')}")

            np.savez(os.path.join(chunks_dir, f'{SIMULATION_NAME}_{ii+starting_point}_itteration.npz'),Span=span,T_cross_values=T_cross_values, T_bar_values=T_bar_values,E_lateral_values=E_lateral_values)
            log.info(f"Files were saved")

        else:
            log.info(f"save whole dataset to {os.path.join(data_dir, f'{SIMULATION_NAME}.npz')}")
            np.savez(os.path.join(data_dir, f'{SIMULATION_NAME}.npz'),Span=span,T_cross_values=T_cross_values, T_bar_values=T_bar_values,E_lateral_values=E_lateral_values)
            Delete_chunks(SIMULATION_NAME)      
                   
                                   
    
    except Exception as e:        
        log.error(f"An error has occured {e}, saving T_cross_value (len: {len(T_cross_values)}) and T_bar values({len(T_bar_values)}) and E_lateral_values ({len(E_lateral_values)}), with itteration files ")
        Zero_counter=Recover_data(sim_name=SIMULATION_NAME,span=span) 
        log.info(f"Recovered dataset from chunks with {Zero_counter} unfinished sweep points and deleted leftover chunks")






def Twist_angle_sweep(sim,span,args=None,RUN_AGAIN=False):
    defaults = {
        "y":None,
        "mmi_length": None,
        "twist_angle": None,
    }
    if args is not None:
        defaults.update(args)

        y = defaults["y"]
        mmi_length = defaults["mmi_length"]
        twist_angle = defaults["twist_angle"]


    SIMULATION_NAME="twist_angle_sweep"
    filename = os.path.join(SCRIPT_DIR, "speedio_fdtd_mmi")
    wg_length=10e-6
    wg_width=0.4e-6
    width_ridge=5.1e-6
    taper_width=1e-6
    taper_width_in=taper_width
    delta_y=0e-6
    Radius=80e-6
    #define ratio
    ratio=85/100
    #define cut angle at the ends of MMI core section
    cut_angle=90   #(degrees)  90==no cut
    mesh_accuracy=3
    
    #define middle section width
    T_cross_values=[]
    T_bar_values=[]
    E_lateral_values=[]

    log.info(f"Starting {SIMULATION_NAME} \n span: {span}, \n width_ridge: {width_ridge}, \n mmi_length:{mmi_length},\n taper_width={taper_width},\n y:{y},\n ratio:{ratio}")
    
    data_dir = os.path.join(SCRIPT_DIR, "data")
    chunks_dir = os.path.join(SCRIPT_DIR, "chunks")
    starting_point=0

    if RUN_AGAIN:
        #if run again is used -> recover data and find last itteration, where to start.
        Recover_data(SIMULATION_NAME,span=span)
        data_file = os.path.join(data_dir, f"{SIMULATION_NAME}.npz")
        if os.path.exists(data_file):
            check_data=np.load(data_file, allow_pickle=True)
            #load Results
            T_cross_values=list(check_data['T_cross_values'])
            T_bar_values=list(check_data['T_bar_values'])
            E_lateral_values=list(check_data['E_lateral_values'])
            starting_point=len(T_cross_values)

            if(starting_point==len(span)):
                starting_point=0
                T_cross_values=[]
                T_bar_values=[]
                E_lateral_values=[]
            span=span[starting_point:]

    #run simmulation 
    try:
        for ii,twist_angle in enumerate(span):
            T_cross,T_bar,E_lateral=fdtd_solver(sim=sim,Radius=Radius,filename=filename,wg_length=wg_length,wg_width=wg_width,width_ridge=width_ridge,
                mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,ratio=ratio,y=y,mesh_accuracy=mesh_accuracy,cut_angle=cut_angle,delta_y=delta_y,twist_angle=twist_angle,sweep_name=SIMULATION_NAME)
            log.info(f"T_cross: {T_cross}, T_bar: {T_bar}")
            # Get new results or append to previous( if starting_point!= 0)
        
            T_cross_values.append(T_cross)
            T_bar_values.append(T_bar)
            E_lateral_values.append(E_lateral)
            log.info(f"save chunks to {os.path.join(chunks_dir, f'{SIMULATION_NAME}_{ii+starting_point}_itteration.npz')}")

            np.savez(os.path.join(chunks_dir, f'{SIMULATION_NAME}_{ii+starting_point}_itteration.npz'),Span=span,T_cross_values=T_cross_values, T_bar_values=T_bar_values,E_lateral_values=E_lateral_values)
            log.info(f"Files were saved")

        else:
            log.info(f"save whole dataset to {os.path.join(data_dir, f'{SIMULATION_NAME}.npz')}")

            np.savez(os.path.join(data_dir, f'{SIMULATION_NAME}.npz'),Span=span,T_cross_values=T_cross_values, T_bar_values=T_bar_values,E_lateral_values=E_lateral_values)
            Delete_chunks(SIMULATION_NAME)      
                   
                                   
    
    except Exception as e:        
        log.error(f"An error has occured {e}, saving T_cross_value (len: {len(T_cross_values)}) and T_bar values({len(T_bar_values)}) and E_lateral_values ({len(E_lateral_values)}), with itteration files ")
        Zero_counter=Recover_data(sim_name=SIMULATION_NAME,span=span) 
        log.info(f"Recovered dataset from chunks with {Zero_counter} unfinished sweep points and deleted leftover chunks")



def Width_sweep(sim,span,args=None,RUN_AGAIN=False):

    defaults = {
        "y":None,
        "mmi_length": None,
        "twist_angle": None,
    }
    if args is not None:
        defaults.update(args)

        y = defaults["y"]
        mmi_length = defaults["mmi_length"]
        twist_angle = defaults["twist_angle"]

    SIMULATION_NAME="width_sweep"
    filename = os.path.join(SCRIPT_DIR, "speedio_fdtd_mmi")
    wg_length=10e-6
    wg_width=0.4e-6
    width_ridge=5.1e-6
    taper_width=1e-6
    taper_width_in=taper_width
    delta_y=0e-6
    Radius=80e-6
    #define ratio
    ratio=85/100
    #define cut angle at the ends of MMI core section
    cut_angle=90   #(degrees)  90==no cut
    mesh_accuracy=3


    
        
    #define middle section width
    T_cross_values=[]
    T_bar_values=[]
    E_lateral_values=[]

    log.info(f"Starting {SIMULATION_NAME} \n span: {span}, \n width_ridge: {width_ridge}, \n mmi_length:{mmi_length},\n taper_width={taper_width},\n y:{y},\n twist angle:{twist_angle},\n ratio:{ratio}")
    
    data_dir = os.path.join(SCRIPT_DIR, "data")
    chunks_dir = os.path.join(SCRIPT_DIR, "chunks")
    starting_point=0

    if RUN_AGAIN:
        #if run again is used -> recover data and find last itteration, where to start.
        Recover_data(SIMULATION_NAME,span=span)
        data_file = os.path.join(data_dir, f"{SIMULATION_NAME}.npz")
        if os.path.exists(data_file):
            check_data=np.load(data_file, allow_pickle=True)
            #load Results
            T_cross_values=list(check_data['T_cross_values'])
            T_bar_values=list(check_data['T_bar_values'])
            E_lateral_values=list(check_data['E_lateral_values'])
            starting_point=len(T_cross_values)

            if(starting_point==len(span)):
                starting_point=0
                T_cross_values=[]
                T_bar_values=[]
                E_lateral_values=[]
            span=span[starting_point:]

    #run simmulation 
    try:
        for ii,width_ridge in enumerate(span):

            dist=opt_width_ridge/3-taper_width
            delta_y=dist/2+taper_width/2-width_ridge/6



            T_cross,T_bar,E_lateral=fdtd_solver(sim=sim,Radius=Radius,filename=filename,wg_length=wg_length,wg_width=wg_width,width_ridge=width_ridge,
                mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,ratio=ratio,y=y,mesh_accuracy=mesh_accuracy,cut_angle=cut_angle,delta_y=delta_y,twist_angle=twist_angle,sweep_name=SIMULATION_NAME)
            log.info(f"T_cross: {T_cross}, T_bar: {T_bar}")
            # Get new results or append to previous( if starting_point!= 0)
        
            T_cross_values.append(T_cross)
            T_bar_values.append(T_bar)
            E_lateral_values.append(E_lateral)
            log.info(f"save chunks to {os.path.join(chunks_dir, f'{SIMULATION_NAME}_{ii+starting_point}_itteration.npz')}")
            np.savez(os.path.join(chunks_dir, f'{SIMULATION_NAME}_{ii+starting_point}_itteration.npz'),Span=span,T_cross_values=T_cross_values, T_bar_values=T_bar_values,E_lateral_values=E_lateral_values)
            log.info(f"Files were saved")

        else:
            log.info(f"save whole dataset to {os.path.join(data_dir, f'{SIMULATION_NAME}.npz')}")
            np.savez(os.path.join(data_dir, f'{SIMULATION_NAME}.npz'),Span=span,T_cross_values=T_cross_values, T_bar_values=T_bar_values,E_lateral_values=E_lateral_values)
            Delete_chunks(SIMULATION_NAME)      
                   
                                   
    
    except Exception as e:        
        log.error(f"An error has occured {e}, saving T_cross_value (len: {len(T_cross_values)}) and T_bar values({len(T_bar_values)}) and E_lateral_values ({len(E_lateral_values)}), with itteration files ")
        Zero_counter=Recover_data(sim_name=SIMULATION_NAME,span=span) 
        log.info(f"Recovered dataset from chunks with {Zero_counter} unfinished sweep points and deleted leftover chunks")






if __name__ =="__main__":


    # ######################
    # #1) Y_sweep
    # SIMULATION_NAME="y_sweep"
    # Y_span=np.linspace(0,10,5)*1e-6
    # args = {
    #     "y":5e-6,
    #     "mmi_length": 32*2e-6,
    #     "twist_angle": None,
    # }
    # Y_sweep(sim=lumapi.FDTD(),span=Y_span,args=args,RUN_AGAIN=False)
    # OPT_Y=data_analysis(dataset=os.path.join(SCRIPT_DIR, "data", SIMULATION_NAME),measurement="max_transmission")  #extract optimal value
    # if OPT_Y==None:
    #     OPT_Y=5e-6  #default value

    OPT_Y=5e-6  #default value

    ###################
    #2) Length_sweep
    SIMULATION_NAME="length_sweep"
    opt_mmi_length=51*2e-6
    Lengths=np.linspace(opt_mmi_length-3e-6,opt_mmi_length+3e-6,3)
    
    args = {
        "y":OPT_Y,
        "mmi_length": 51*2e-6,
        "twist_angle": None,
    }

    Length_sweep(sim=lumapi.FDTD(),span=Lengths,args=args,RUN_AGAIN=False)
    OPT_LENGTH=data_analysis(dataset=os.path.join(SCRIPT_DIR, "data", SIMULATION_NAME),measurement="max_transmission") #extract optimal value
    if OPT_LENGTH==None:
        OPT_LENGTH=51*2e-6  #default value



    ######################
    #3) Twist_angle_span
   
    SIMULATION_NAME="twist_angle_sweep"
    Twist_angles=np.linspace(opt_twist_angle-0.001,opt_twist_angle+0.001,3)
    args = {
        "y":OPT_Y,
        "mmi_length": OPT_LENGTH,
        "twist_angle": None,
    }

    Twist_angle_sweep(sim=lumapi.FDTD(),span=Twist_angles,args=args,RUN_AGAIN=False)
    OPT_ANGLE=data_analysis(dataset=os.path.join(SCRIPT_DIR, "data", SIMULATION_NAME),measurement="optimal_angle")
    if OPT_ANGLE==None:
        OPT_ANGLE=None     #default value


    ######################
    #4) Width_sweep
    SIMULATION_NAME="width_sweep"

    args = {
        "y":OPT_Y,
        "mmi_length": OPT_LENGTH,
        "twist_angle": OPT_ANGLE,
    }
    
    opt_width_ridge=5.1e-6
    Widths=np.linspace(opt_width_ridge-0.5e-6,opt_width_ridge+0.5e-6,2)
    Width_sweep(sim=lumapi.FDTD(),span=Widths,args=args,RUN_AGAIN=False)
    OPT_WIDTH=data_analysis(dataset=os.path.join(SCRIPT_DIR, "data", SIMULATION_NAME),measurement="optimal_angle") #closest value to a defined ratio


    log.info(f"Sweeps have been completed, optimal values: \n OPT_Y: {OPT_Y} \n OPT_LENGTH: {OPT_LENGTH} \n OPT_ANGLE: {OPT_ANGLE} \n OPT_WIDTH: {OPT_WIDTH} ")





    
    
    
    


