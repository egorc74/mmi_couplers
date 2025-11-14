from variables import *
def mode_solver(sim,filename,width_ridge):
    sim.switchtolayout()
    sim.deleteall()
    width_margin = 2.0e-6
    height_margin = 1.0e-6

    Xmin=-8e-6 
    Xmax=8e-6 #length of wg 16um
    Zmin=-height_margin
    Zmax=thick_Si3N4 + height_margin
    Y_span=2*width_margin + width_ridge
    Ymin=-Y_span/2
    Ymax=-Ymin


    #draw box and waffer
    sim.addrect() 
    sim.set("name","BOX") 
    sim.set("material",material_BOX)
    sim.set("y",0)         
    sim.set("y span",Y_span+5e-6)
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
    sim.set("y span",Y_span+5e-6)
    sim.set("z min",-thick_BOX-thick_Substrate)     
    sim.set("z max", -thick_BOX)
    sim.set("x min",Xmin)  
    sim.set("x max",Xmax)
    sim.set("alpha",0.1)

    ## draw waveguide
    sim.addrect()
    sim.set("name","waveguide")
    sim.set("material",material_Si3N4)
    sim.set("y",0)         
    sim.set("y span",width_ridge)
    sim.set("z span",thick_Si3N4)
    sim.set("z", 0)
    sim.set("x min",Xmin)
    sim.set("x max",Xmax)
    sim.save(filename)

    meshsize=20e-9
    modes=20


    sim.addfde()
    sim.set("solver type","2D X normal")
    sim.set("x",0)
    sim.set("y",0)
    sim.set("y span",Y_span)
    sim.set("z max",Zmax)
    sim.set("z min",Zmin)
    sim.set("wavelength",wavelength)
    sim.set("solver type","2D X normal")
    sim.set("define y mesh by","maximum mesh step") 
    sim.set("dy",meshsize)
    sim.set("define z mesh by","maximum mesh step") 
    sim.set("dz",meshsize)
    sim.set("number of trial modes",modes)
    sim.cleardcard()
    n=sim.findmodes()
    Neff = np.real(sim.getdata('FDE::data::mode1','neff')[0]) 
    print(f"Effective index of first TE launching mode{Neff}")
    sim.save(filename)
    return Neff




if __name__=="__main__":
    filename="mode_effective_index"
    taper_width=2.5e-6
    width_ridge=8e-6
    mode_solver(sim=lumapi.MODE(filename),width_ridge=width_ridge,filename=filename)