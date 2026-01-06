
import sys
import glob
import os
# from nm1550.fdtd_solver import fdtd_solver
from variables import *
from mode_solver import mode_solver

def Recover_data(sim_name,span):
    files = sorted(glob.glob(f"chunks/{sim_name}*.npz"))

    if files:  # make sure the list is not empty
        last_file = files[-1]
        Zero_counter=0
        with np.load(last_file) as data:
                neff_values=data["neff_values"]    
                Span=data["Span"]
                #count results that were ommitted    
                Zero_counter = len(span) -len(neff_values)
                #save to a npz file
                np.savez(f'data/{sim_name}.npz',Span=Span,neff_values=neff_values)
                
                #delete previous chunks

        number_of_deleted=Delete_chunks(sim_name=sim_name)        
        print(f"Missing Results: {Zero_counter} and  Deleted Chunks: {number_of_deleted} in summ they must be {len(span)}") 

    else:
        last_file = None
        print("No files found")
        Zero_counter=0
    #Count every zero in Result values
   
    return Zero_counter


def Delete_chunks(sim_name):
    files = sorted(glob.glob(f"chunks/{sim_name}*.npz"))
    for f in files:
        os.remove(f)
    return len(files)





def FDE_z_span(sim,RUN_AGAIN=False,args=None):

    defaults = {
        "z_span": None,
        "y_span": None,
        "mesh_z": None,
        "mesh_y": None,
    }

    # Merge user args into defaults
    if args is not None:
        defaults.update(args)
    z_span = defaults["z_span"]
    y_span = defaults["y_span"]
    mesh_z = defaults["mesh_z"]
    mesh_y = defaults["mesh_y"]

    log = setup_logger("FDE_z_span", "logging/FDE_z_span.log")
    wg_length=opt_wg_length
    wg_width=1.6e-6
    width_ridge=opt_width_ridge
    mmi_length=opt_mmi_length
    taper_width=opt_taper_width
    taper_width_in=taper_width
    delta_y=0
    mesh_accuracy=1
    neff_values= []
    starting_point=0

    if RUN_AGAIN:
        #if run again is used -> recover data and find last itteration, where to start.
        Recover_data("FDE_z_span",span=z_span)
        if os.path.exists("data/FDE_z_span.npz"):
            check_data=np.load('data/FDE_z_span.npz', allow_pickle=True)
            #load Results
            neff_values=list(check_data['neff_values'])
            print(neff_values)
            starting_point=len(neff_values)

            if(starting_point==len(z_span)):
                starting_point=0
            z_span=z_span[starting_point:]
            print(f"starting for loop with z_span: {len(z_span)}")
    #run simmulation 
    try:
        for ii,span in enumerate(z_span):
            neff=mode_solver(sim=sim,filename=filename,FDE_z_span=span,FDE_y_span=y_span,mesh_y=mesh_y,mesh_z=mesh_z)[0]
            # Get new results or append to previous( if starting_point!= 0)
        
            neff_values.append(neff)
            log.info(f"neff:{neff}")
            np.savez(f'chunks/FDE_z_span_{ii+starting_point}_itteration.npz',Span=z_span,neff_values=neff_values)
       
        else:
            np.savez('data/FDE_z_span.npz',Span=z_span,neff_values=neff_values)
            Delete_chunks("FDE_z_span")                                     
    
    except Exception as e:        
        log.error(f"An error has occured {e}, saving neff_value (len: {len(neff_values)}), with itteration files ")
        Zero_counter=Recover_data(sim_name="FDE_z_span",span=z_span) 
        log.info(f"Recovered dataset from chunks with {Zero_counter} unfinished sweep points and deleted leftover chunks")


def FDE_y_span(sim,RUN_AGAIN=False,args=None):
    #Define default None arguments
    defaults = {
        "z_span": None,
        "y_span": None,
        "mesh_z": None,
        "mesh_y": None,
    }

    # Merge user args into defaults
    if args is not None:
        defaults.update(args)
    z_span = defaults["z_span"]
    y_span = defaults["y_span"]
    mesh_z = defaults["mesh_z"]
    mesh_y = defaults["mesh_y"]


    log = setup_logger("FDE_y_span", "logging/FDE_y_span.log")
    wg_length=opt_wg_length
    wg_width=1.6e-6
    width_ridge=opt_width_ridge
    mmi_length=opt_mmi_length
    taper_width=opt_taper_width
    taper_width_in=taper_width
    delta_y=0
    mesh_accuracy=1
    neff_values= []
    starting_point=0

    if RUN_AGAIN:
        #if run again is used -> recover data and find last itteration, where to start.
        Recover_data("FDE_y_span",span=y_span)
        if os.path.exists("data/FDE_y_span.npz"):
            check_data=np.load('data/FDE_y_span.npz', allow_pickle=True)
            #load Results
            neff_values=list(check_data['neff_values'])
            print(neff_values)
            starting_point=len(neff_values)

            if(starting_point==len(y_span)):
                starting_point=0
            y_span=y_span[starting_point:]
            print(f"starting for loop with y_span: {len(y_span)}")
    #run simmulation 
    try:
        for ii,span in enumerate(y_span):
            neff=mode_solver(sim=sim,filename=filename,FDE_z_span=z_span,FDE_y_span=span,mesh_y=mesh_y,mesh_z=mesh_z)[0]
            # Get new results or append to previous( if starting_point!= 0)
        
            neff_values.append(neff)
            log.info(f"neff:{neff}")
            np.savez(f'chunks/FDE_y_span_{ii+starting_point}_itteration.npz',Span=y_span,neff_values=neff_values)
       
        else:
            np.savez('data/FDE_y_span.npz',Span=y_span,neff_values=neff_values)
            Delete_chunks("FDE_y_span")                                     
    
    except Exception as e:        
        log.error(f"An error has occured {e}, saving neff_value (len: {len(neff_values)}), with itteration files ")
        Zero_counter=Recover_data(sim_name="FDE_y_span",span=y_span) 
        log.info(f"Recovered dataset from chunks with {Zero_counter} unfinished sweep points and deleted leftover chunks")



def Mesh_accuracy_z(sim,RUN_AGAIN=False,args=None):

    #Define default None arguments
    defaults = {
        "z_span": None,
        "y_span": None,
        "mesh_z": None,
        "mesh_y": None,
    }

    # Merge user args into defaults
    if args is not None:
        defaults.update(args)
    z_span = defaults["z_span"]
    y_span = defaults["y_span"]
    mesh_z = defaults["mesh_z"]
    mesh_y = defaults["mesh_y"]

    log = setup_logger("Mesh_accuracy_z", "logging/Mesh_accuracy_z.log")
    wg_length=opt_wg_length
    wg_width=1.6e-6
    width_ridge=opt_width_ridge
    mmi_length=opt_mmi_length
    taper_width=opt_taper_width
    taper_width_in=taper_width
    delta_y=0
    neff_values= []
    starting_point=0

    if RUN_AGAIN:
        #if run again is used -> recover data and find last itteration, where to start.
        Recover_data("Mesh_accuracy_z",span=mesh_z)
        if os.path.exists("data/Mesh_accuracy_z.npz"):
            check_data=np.load('data/Mesh_accuracy_z.npz', allow_pickle=True)
            #load Results
            neff_values=list(check_data['neff_values'])
            print(neff_values)
            starting_point=len(neff_values)
            if(starting_point==len(mesh_z)):
                starting_point=0
            print(f"starting  point{starting_point}")
            mesh_z=mesh_z[starting_point:]
            print(f"starting for loop with mesh_z: {len(mesh_z)}")
    #run simmulation 
    try:
        for ii,mesh in enumerate(mesh_z):
            neff=mode_solver(sim=sim,filename=filename,FDE_z_span=z_span,FDE_y_span=y_span,mesh_y=mesh_y,mesh_z=mesh)[0]
            # Get new results or append to previous( if starting_point!= 0)
            neff_values.append(neff)
            log.info(f"neff:{neff}")
            np.savez(f'chunks/Mesh_accuracy_z_{ii+starting_point}_itteration.npz',Span=y_span,neff_values=neff_values)
       
        else:
            np.savez('data/Mesh_accuracy_z.npz',Span=mesh_z,neff_values=neff_values)
            Delete_chunks("Mesh_accuracy_z")                                     
    
    except Exception as e:        
        log.error(f"An error has occured {e}, saving neff_value (len: {len(neff_values)}) with itteration files ")
        Zero_counter=Recover_data(sim_name="Mesh_accuracy_z",span=mesh_z) 
        log.info(f"Recovered dataset from chunks with {Zero_counter} unfinished sweep points and deleted leftover chunks")


def Mesh_accuracy_y(sim,RUN_AGAIN=False,args=None):
#Define default None arguments
    defaults = {
        "z_span": None,
        "y_span": None,
        "mesh_z": None,
        "mesh_y": None,
    }

    # Merge user args into defaults
    if args is not None:
        defaults.update(args)
    z_span = defaults["z_span"]
    y_span = defaults["y_span"]
    mesh_z = defaults["mesh_z"]
    mesh_y = defaults["mesh_y"]

    mesh_y=np.linspace(1,6,6)
    log = setup_logger("Mesh_accuracy_y", "logging/Mesh_accuracy_y.log")
    wg_length=opt_wg_length
    wg_width=1.6e-6
    width_ridge=opt_width_ridge
    mmi_length=opt_mmi_length
    taper_width=opt_taper_width
    taper_width_in=taper_width
    delta_y=0
    neff_values= []
    starting_point=0

    if RUN_AGAIN:
        #if run again is used -> recover data and find last itteration, where to start.
        Recover_data("Mesh_accuracy_y",span=mesh_y)
        if os.path.exists("data/Mesh_accuracy_y.npz"):
            check_data=np.load('data/Mesh_accuracy_y.npz', allow_pickle=True)
            #load Results
            neff_values=list(check_data['neff_values'])
            print(neff_values)
            starting_point=len(neff_values)

            if(starting_point==len(mesh_y)):
                starting_point=0
            
            print(f"starting  point {starting_point}")
            mesh_y=mesh_y[starting_point:]
            print(f"starting for loop with mesh_y: {len(mesh_y)}")
    #run simmulation 
    try:
        for ii,mesh in enumerate(mesh_y):
            neff=mode_solver(sim=sim,filename=filename,FDE_z_span=z_span,FDE_y_span=y_span,mesh_y=mesh,mesh_z=mesh_z)[0]
            # Get new results or append to previous( if starting_point!= 0)
            neff_values.append(neff)
            log.info(f"neff:{neff}")
            np.savez(f'chunks/Mesh_accuracy_y_{ii+starting_point}_itteration.npz',Span=y_span,neff_values=neff_values)
       
        else:
            np.savez('data/Mesh_accuracy_y.npz',Span=mesh_y,neff_values=neff_values)
            Delete_chunks("Mesh_accuracy_y")                                     
    
    except Exception as e:        
        log.error(f"An error has occured {e}, saving neff_value (len: {len(neff_values)}) with itteration files ")
        Zero_counter=Recover_data(sim_name="Mesh_accuracy_y",span=mesh_y) 
        log.info(f"Recovered dataset from chunks with {Zero_counter} unfinished sweep points and deleted leftover chunks")







if __name__=="__main__":
    filename="waveguide_width"
    min_y_span=1.6e-6+0.5e-6
    max_y_span=min_y_span+1.5e-6
    y_span=np.linspace(min_y_span,max_y_span,10)
    
    min_y_span=thick_Si3N4+1.7e-6
    max_y_span=min_y_span+3e-6
    z_span=np.linspace(min_y_span,max_y_span,10)
    



    #form mesh_z span
    d_max=0.1e-6
    d_min=0.005e-6
    mesh_z=np.zeros(10)
    for i in range(10):
        d_mesh=d_max*(d_min/d_max)**(i/9)
        mesh_z[i]=d_mesh
    args={"z_span":2.6e-6,
          "y_span":3e-6,
          "mesh_z":mesh_z}
    
    print(mesh_z)



    # FDE_z_span(sim=lumapi.MODE(filename),RUN_AGAIN=False,args=args)
    Mesh_accuracy_z(sim=lumapi.MODE(filename),RUN_AGAIN=True,args=args)
    # min_y_span=opt_width_ridge+2e-6
    # Port_size(sim=lumapi.FDTD(filename_fdtd))
    # FDE_z_span(sim=lumapi.FDTD(filename_fdtd),z_span=z_span)
    # z_span=np.linspace(1.8e-6,2.5e-6,2)