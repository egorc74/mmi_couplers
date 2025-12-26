from nm1550.variables import *
from nm1550.geometry import geometry
import plotly.graph_objects as go
def fdtd_solver(sim,filename,width_ridge,mmi_length,taper_width,taper_width_in,mesh_accuracy,delta_y=0,sweep_name=None,FDTD_z_span=None,FDTD_y_span=None):

    log = setup_logger("fdtd_solver", "logging/fdtd_solver.log")

    log.info(f"Starting fdtd_solver() \n width_ridge: {width_ridge}, \n mmi_length:{mmi_length},\n taper_width={taper_width},\n ")
    geometry(sim=sim,filename=filename,width_ridge=width_ridge,
            mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,delta_y=delta_y)
  

    ##### FDTD dimensions #######
    margin=10e-6
    height_margin=1e-6
    Xmin=-(mmi_length+2*wg_length+margin)/2 
    Xmax=(mmi_length+2*wg_length+margin)/2
    Zmin=-1e-6
    Zmax=height_margin
    width_margin=5e-6

    Y_span=width_margin + width_ridge 
    Ymin=-Y_span/2 
    Ymax=-Ymin
    
    x_span=wg_length
    width_eff=width_ridge
    distance_wg=width_eff/4  ##effective distance




    
    ##Add fdtd
    sim.addfdtd()
    fdtd_margin=2e-6
    sim.set("x min",Xmin)
    sim.set("x max",Xmax)
    sim.set("y",0)
    sim.set("y span",Y_span)

    if FDTD_y_span:
        sim.set("y span",FDTD_y_span)
    else:
        sim.set("y span",Y_span)

    if FDTD_z_span:
        sim.set("z",0)
        sim.set("z span",FDTD_z_span)
    else:
        sim.set("z min",Zmin)
        sim.set("z max",Zmax)

    sim.set("mesh accuracy", mesh_accuracy)
    sim.set("x min bc","PML")  
    sim.set("x max bc","PML")
    sim.set("y min bc","PML") 
    sim.set("y max bc","PML")
    sim.set("z min bc","PML") 
    sim.set("z max bc","PML")




    #add source
    sim.setglobalsource("wavelength start",wavelength)
    sim.setglobalsource("wavelength stop",wavelength)

    sim.setglobalmonitor("use source limits",0)
    sim.setglobalmonitor("frequency points",1)
    sim.setglobalmonitor("wavelength center",wavelength)


    #Input port
    sim.addport()
    sim.set("name","source_port")
    sim.set("injection axis","x-axis")
    sim.set("direction","forward")
    sim.set("mode selection","fundamental TE mode")

    sim.set("y",0) 
    wg_spacing=width_ridge/3
    sim.set("y span",wg_spacing)
    sim.set("x",Xmin+2e-6) 
    sim.set("z min",Zmin) 
    sim.set("z max",Zmax)


    ##Through port

    sim.addport()
    sim.set("name","through_port")
    sim.set("injection axis","x-axis")
    sim.set("direction","backward")
    
            
    sim.set("y span",wg_spacing)
    sim.set("y",-distance_wg+delta_y) 
    sim.set("y span",wg_spacing)
    sim.set("x",Xmax-2e-6) 
    sim.set("z min",Zmin) 
    sim.set("z max",Zmax)

    ##Cross port 
    sim.addport()
    sim.set("name","cross_port")
    sim.set("injection axis","x-axis")
    sim.set("direction","backward")
    sim.set("y span",wg_spacing)
    sim.set("y",distance_wg-delta_y) 
    sim.set("x",Xmax-2e-6)
    sim.set("z min",Zmin) 
    sim.set("z max",Zmax) 

    sim.addmovie()
    sim.set("monitor type","2D Z-normal")
    sim.set("name",f"{filename}_{sweep_name}") 
    sim.set("x span",200e-6)
    sim.set("y span",20e-6)
    sim.set("x",0)
    sim.set("y",0)
    sim.set("z",0)

    # sim.addpower()
    sim.adddftmonitor()
    sim.set("monitor type","2D Z-normal")
    sim.set("name","lateral_monitor") 
    sim.set("x span",200e-6)
    sim.set("y span",20e-6)
    sim.set("x",0)
    sim.set("y",0)
    sim.set("z",0)

    sim.select("FDTD::ports")
    sim.set("source port", "source_port")


    sim.save(f"{filename}.fsp")
    
    #run fdtd

    # sim.run()

    # #get results from both monitors
    m1_name="FDTD::ports::cross_port"
    m2_name="FDTD::ports::through_port"
    m3_name="lateral_monitor"
    try:
        T_cross = sim.getresult(m1_name,"T")
        T_bar = sim.getresult(m2_name,"T")
        E_lateral = sim.getresult(m3_name,"E")
        log.info(f"Obtained T_cross {T_cross} and T_bar={T_bar}, E_lateral={len(E_lateral)}")

    except Exception as e:
        T_cross=0
        T_bar=0
        E_lateral=0
        log.error(f"Error occured: {e} Obtained T_cross {T_cross} and T_bar={T_bar} and E_lateral=0")

    input("Press Enter to continue...")


    sim.save(f"{filename}.fsp")

    

    return T_cross,T_bar,E_lateral






if __name__=="__main__":
    import os

    filename="mmi_1x2_fdtd"
    wg_length=15e-6
    wg_width=1.6e-6
    width_ridge=11e-6
    mmi_length=61e-6
    taper_width=4.4e-6
    taper_width_in=4.4e-6
    delta_y=0e-6
    n_core=1.9963
    cladding=0

    #define ratio
    mesh_accuracy=3
    if os.path.isfile(f"{filename}.fsp"):
        fdtd_solver(sim=lumapi.FDTD(filename),filename=filename,width_ridge=width_ridge,
             mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,mesh_accuracy=mesh_accuracy)

    else:
        fdtd_solver(sim=lumapi.FDTD(),filename=filename,wg_width=wg_width,width_ridge=width_ridge,
             mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,mesh_accuracy=mesh_accuracy)