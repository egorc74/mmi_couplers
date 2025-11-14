from variables import *
def taper_geometry(sim, filename,taper_width,taper_length):
    log = setup_logger("geometry", "logging/geometry.log")
    log.info(f"Starting geometry() built \n width_ridge: {taper_width}, \n mmi_length:{taper_length}")

    #mmi length
    sim.switchtolayout()
    sim.deleteall()

    Xmin=-taper_length/2 
    Xmax=-Xmin
    Zmin=-height_margin 
    Zmax=thick_Si3N4 + height_margin
    Y_span=2*width_margin + taper_width 
    Ymin=-Y_span/2 
    Ymax=-Ymin

    ##Wafer size
    Xmin_waffer=Xmin-10e-6
    Xmax_waffer=-Xmin_waffer

    
    ##draw input wg



    #draw taper input
    ly_top=taper_width
    ly_base=wg_width
    x_span=taper_length
    z_span=thick_Si3N4
    z=0
    x=0
    y=0

    V = np.zeros((4, 2))

    # assign values row by row
    V[0, :] = [-ly_base/2, -x_span/2]
    V[1, :] = [-ly_top/2,  x_span/2]
    V[2, :] = [ ly_top/2,  x_span/2]
    V[3, :] = [ ly_base/2, -x_span/2]

    sim.addpoly()
    sim.set("x",x)
    sim.set("y",0)
    sim.set("z",z)
    sim.set("z span",z_span)
    sim.set("vertices",V)
    sim.set("material",material_Si3N4)
    sim.set("name","taper_input")
    sim.set("first axis","z")
    sim.set("rotation 1",-90)
    sim.set("override mesh order from material database",1)
    sim.set("mesh order",1)
    

    #draw box and waffer
    sim.addrect() 
    sim.set("name","BOX") 
    sim.set("material",material_BOX)
    sim.set("y",0)         
    sim.set("y span",Y_span+5e-6)
    sim.set("z min",-thick_BOX)     
    sim.set("z max", 0-thick_Si3N4/2)
    sim.set("x min",Xmin_waffer)  
    sim.set("x max",Xmax_waffer)
    sim.set("alpha",0.05)

    #draw waffer
    sim.addrect() 
    sim.set("name","Wafer") 
    sim.set("material",material_Si)
    sim.set("y",0)         
    sim.set("y span",Y_span+5e-6)
    sim.set("z min",-thick_BOX-thick_Substrate)     
    sim.set("z max", -thick_BOX)
    sim.set("x min",Xmin_waffer)  
    sim.set("x max",Xmax_waffer)
    sim.set("alpha",0.1)
    sim.save(filename)




if __name__=="__main__":
    filename="taper_length_span"
    taper_length=50e-6
    taper_width=2.5e-6
    taper_geometry(sim=lumapi.MODE(),filename=filename,taper_length=taper_length,taper_width=taper_width)



    