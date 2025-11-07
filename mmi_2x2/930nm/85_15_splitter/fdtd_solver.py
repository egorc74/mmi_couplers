from variables import *
from geometry import geometry
import plotly.graph_objects as go
def fdtd_solver(sim,Radius,filename,y,width_ridge,mmi_length,wg_length,wg_width,taper_width,taper_width_in,ratio,mesh_accuracy,cut_angle):

    log = setup_logger("fdtd_solver", "logging/fdtd_solver.log")
    delta_y=0

    log.info(f"Starting fdtd_solver() \n width_ridge: {width_ridge}, \n mmi_length:{mmi_length},\n taper_width={taper_width},\n ratio:{ratio}")
    X,twist_angle=geometry(sim=sim,filename=filename,Radius=Radius,wg_length=wg_length,wg_width=wg_width,width_ridge=width_ridge,
            mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,ratio=ratio,y=y,cut_angle=cut_angle)
  

    ##### FDTD dimensions #######
    margin=10e-6
    height_margin=0.5e-6
    Xmin=-(mmi_length+2*wg_length+margin)/2 
    Xmax=(mmi_length+2*wg_length+margin)/2
    Zmin=-0.8e-6
    Zmax=thick_Si3N4 + height_margin
    width_margin=5e-6

    rotation_margin=(mmi_length+wg_length)*np.sin(twist_angle)
    Y_span=2*width_margin + width_ridge + rotation_margin 
    Ymin=-Y_span/2 
    Ymax=-Ymin
    
    x_span=wg_length
    width_eff=width_ridge
    distance_wg=width_eff/6  ##effective distance




    
    ##Add fdtd
    sim.addfdtd()
    fdtd_margin=2e-6
    sim.set("x min",Xmin)
    sim.set("x max",Xmax)
    sim.set("y",0)
    sim.set("y span",Y_span+2e-6)
    sim.set("z min",-0.5e-6)
    sim.set("z max",0.5e-6)
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
    sim.set("y",(Xmin+3e-6)*np.sin(twist_angle)+distance_wg+delta_y) 
    wg_spacing=(width_ridge/6-wg_width/2)*2
    sim.set("y span",wg_width+wg_spacing)
    sim.set("x",Xmin+2e-6) 
    sim.set("z min",Zmin) 
    sim.set("z max",Zmax)



    ##Through port

    sim.addport()
    sim.set("name","through-port")
    sim.set("injection axis","x-axis")
    sim.set("direction","backward")
            
    sim.set("y span",wg_width+wg_spacing)
    sim.set("y",(Xmin+3e-6)*np.sin(twist_angle)+distance_wg+delta_y) 
    sim.set("y span",wg_width+wg_spacing)
    sim.set("x",Xmax-2e-6) 
    sim.set("z min",Zmin) 
    sim.set("z max",Zmax)

    ##Cross port 
    sim.addport()
    sim.set("name","cross_port")
    sim.set("injection axis","x-axis")
    sim.set("direction","backward")
    sim.set("y span",wg_width+wg_spacing)
    sim.set("y",(Xmin+3e-6)*np.sin(twist_angle)-distance_wg+delta_y) 
    sim.set("x",Xmax-2e-6)
    sim.set("z min",Zmin) 
    sim.set("z max",Zmax) 

    sim.adddftmonitor()
    sim.set("x span",200e-6)
    sim.set("y span",20e-6)
    sim.set("x",0)
    sim.set("y",0)
    sim.set("z",0)


    sim.save(filename)
    
    #run fdtd

    # sim.run()
    sim.save(filename)

    

if __name__=="__main__":
    import os

    filename="mmi_2x2_fdtd"
    wg_length=25e-6
    wg_width=1.6e-6
    width_ridge=8e-6
    mmi_length=87e-6
    taper_width=2.0e-6
    taper_width_in=2.0e-6
    delta_y=0e-6
    n_core=1.9963
    cladding=0

    Radius=80e-6
    #define ratio
    ratio=85/100
    #define middle section width
    y=5e-6/2
    #define cut angle at the ends of MMI core section
    cut_angle=80   #(degrees)  90==no cut
    mesh_accuracy=2
    if os.path.isfile(f"{filename}.fsp"):
        fdtd_solver(sim=lumapi.FDTD(filename),filename=filename,wg_length=wg_length,Radius=Radius,wg_width=wg_width,width_ridge=width_ridge,
             mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,ratio=ratio,y=y,mesh_accuracy=mesh_accuracy,cut_angle=cut_angle)

    else:
        fdtd_solver(sim=lumapi.FDTD(),Radius=Radius,filename=filename,wg_length=wg_length,wg_width=wg_width,width_ridge=width_ridge,
             mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,ratio=ratio,y=y,mesh_accuracy=mesh_accuracy,cut_angle=cut_angle)








