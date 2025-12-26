from variables import *
def geometry(sim, filename,width_ridge):
    
    #mmi length
    sim.switchtolayout()
    sim.deleteall()
    Xmax=10e-6
    Xmin=-10e-6
    ## draw MMI center section
    sim.addrect() 
    sim.set("name","mmi_section") 
    sim.set("material",material_Si3N4)
    sim.set("y",0)         
    sim.set("y span",width_ridge)
    sim.set("z",0)     
    sim.set("z span", thick_Si3N4)
    sim.set("x min",Xmin)  
    sim.set("x max",Xmax)


    #draw box and waffer
    sim.addrect() 
    sim.set("name","BOX") 
    sim.set("material",material_BOX)
    sim.set("y",0)         
    sim.set("y span",width_ridge+100e-6)
    sim.set("z min",-thick_BOX)     
    sim.set("z max", 0-thick_Si3N4/2)
    sim.set("x min",Xmin)  
    sim.set("x max",Xmax)
    sim.set("alpha",0.05)

    #draw waffer
    sim.addrect() 
    sim.set("name","Wafer") 
    sim.set("material",material_Si)
    sim.set("y",0)         
    sim.set("y span",width_ridge+100e-6)
    sim.set("z min",-thick_BOX-thick_Substrate)     
    sim.set("z max", -thick_BOX)
    sim.set("x min",Xmin)  
    sim.set("x max",Xmax)
    sim.set("alpha",0.1)
    sim.save(filename)




if __name__=="__main__":
    filename="waveguide_width"
    wavelength=1.55e-6
    wg_length=25e-6
    wg_width=1.6e-6
    width_ridge=9e-6
    mmi_length=50e-6
    taper_width=3.0e-6
    taper_width_in=3.0e-6
    delta_y=0e-6
    n_core=1.9963
    cladding=0
    geometry(sim=lumapi.MODE(filename),filename=filename,width_ridge=1.6e-6)




    