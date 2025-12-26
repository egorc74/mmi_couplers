from mode_geometry import geometry
from variables import *

def mode_solver(sim, filename,mmi_width,mmi_length,taper_width,taper_width_in, delta_y,curved_tapers=False):
  
    geometry(sim=sim, filename=filename,mmi_width=mmi_width,
             mmi_length=mmi_length,taper_width=taper_width,
             taper_width_in=taper_width_in, delta_y=delta_y,curved_tapers=False)

#Sim borders
    margin=2e-6
    Sim_X_span=mmi_length + wg_length*2 + 2*Radius + 6*margin + 2* wg_width
    Sim_Y_min=-mmi_width/2-margin
    Sim_Y_max=mmi_width/2+2*Radius-mmi_width/3+margin+wg_width/2

    sim.addvarfdtd()
    sim.set("x",0)
    sim.set("x span",Sim_X_span)

    sim.set("y min",Sim_Y_min)
    sim.set("y max",Sim_Y_max)
    sim.set("z",0)
    sim.set("z span",margin)
    sim.set("simulation time",10000e-15)  # 5000 fs
#Effective index
    sim.set("x0",0)  #salb mode position
    sim.set("y0",Sim_Y_max-(Sim_Y_max-Sim_Y_min)/2)  
   
    sim.addindex()
    sim.set("name","index_monitor")

    sim.set("monitor type",3)  
    sim.set("x",0)
    sim.set("x span",Sim_X_span)
    sim.set("y min",Sim_Y_min)
    sim.set("y max",Sim_Y_max)


    sim.set("z",0)
  
    
    sim.setglobalsource("wavelength start",2e-6)
    sim.setglobalsource("wavelength stop",2e-6)

    input("press enter")


if __name__=="__main__":
    filename="mrr_with_50_50_splitter"
    wavelength=1.55e-6
    wg_length=25e-6
    wg_width=1.6e-6
    mmi_width=11e-6
    mmi_length=50e-6
    taper_width=2.5e-6
    taper_width_in=2.5e-6
    delta_y=0e-6
    n_core=1.9963
    cladding=0
    curved_tapers=False
    mode_solver(sim=lumapi.MODE(), filename=filename,mmi_width=mmi_width,
             mmi_length=mmi_length,taper_width=taper_width,
             taper_width_in=taper_width_in, delta_y=delta_y,curved_tapers=curved_tapers)
