from variables import *
def geometry(sim, filename,width_ridge,mmi_length,taper_width,taper_width_in, delta_y):
    log = setup_logger("geometry", "logging/geometry.log")

    log.info(f"Starting geometry() built \n width_ridge: {width_ridge}, \n mmi_length:{mmi_length},\n taper_width={taper_width},\n delta_y:{delta_y}")

    #mmi length
    sim.switchtolayout()
    sim.deleteall()
    width_eff=width_ridge
    log.info(f"width_eff: {width_eff}")
    mmi_pi_length=4*n_core*(width_eff**2)/3./wavelength
    log.info(f"mmi_pi_length: {mmi_pi_length}")
    Xmin=-mmi_length/2 
    Xmax=mmi_length/2 #length of wg 4um
    Zmin=-height_margin 
    Zmax=thick_Si3N4 + height_margin
    Y_span=2*width_margin + width_ridge 
    Ymin=-Y_span/2 
    Ymax=-Ymin

    ##Wafer size
    Xmin_waffer=Xmin-wg_length-4e-6
    Xmax_waffer=Xmax+wg_length+4e-6

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

    #mmi_draw

    #draw cladd
    if (cladding==1):
        sim.addrect()
        sim.set("name","Clad") 
        sim.set("material",material_Clad)
        sim.set("y",0)         
        sim.set("y span",Y_span+5e-6)
        sim.set("z min",-thick_Si3N4/2)     
        sim.set("z max", thick_Clad)
        sim.set("x min",Xmin_waffer)  
        sim.set("x max",Xmax_waffer)
        sim.set("alpha",0.05)
        sim.set("override mesh order from material database",1)
        sim.set("mesh order",4)


    distance_wg=width_eff/4  ##effective distance
    ##draw input wg

    sim.addrect() 
    sim.set("name",f"input_wg") 
    sim.set("material",material_Si3N4)
    sim.set("y",0)         
    sim.set("y span",wg_width)
    sim.set("z",0)     
    sim.set("z span", thick_Si3N4)
    sim.set("x min",Xmin_waffer)  
    sim.set("x max",Xmin_waffer+wg_length)





    ##draw output wg

    for ii in range(1,N_out+1):
        sim.addrect() 
        sim.set("name",f"output_wg{ii}") 
        sim.set("material",material_Si3N4)
        sim.set("y",(distance_wg+delta_y)*(-1)**ii)         
        sim.set("y span",wg_width)
        sim.set("z",0)     
        sim.set("z span", thick_Si3N4)
        sim.set("x min",Xmax_waffer-wg_length)  
        sim.set("x max",Xmax_waffer)
        


    #draw taper input
    ly_top=taper_width_in
    ly_base=wg_width
    x_span=wg_length
    z_span=thick_Si3N4
    z=0
    x=Xmin-x_span/2
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
    sim.set("name",f"taper_input{ii}")
    sim.set("first axis","z")
    sim.set("rotation 1",-90)
    sim.set("override mesh order from material database",1)
    sim.set("mesh order",1)
    




    #draw tapers output
    ly_top=taper_width
    ly_base=wg_width
    z_span=thick_Si3N4
    z=0
    x=Xmax+x_span/2
    y=0


    V = np.zeros((4, 2))

    # assign values row by row
    V[0, :] = [-ly_base/2, -x_span/2]
    V[1, :] = [-ly_top/2,  x_span/2]
    V[2, :] = [ ly_top/2,  x_span/2]
    V[3, :] = [ ly_base/2, -x_span/2]
    for ii in range(N_out+1):
        sim.addpoly()
        sim.set("x",x)
        sim.set("y",(distance_wg+delta_y)*(-1)**ii)
        sim.set("z",z)
        sim.set("z span",z_span)
        sim.set("vertices",V)
        sim.set("material",material_Si3N4)
        sim.set("name",f"taper_output{ii}")
        sim.set("first axis","z")
        sim.set("rotation 1",90)
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
    filename="mmi_simulations_1x2"
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
    geometry(sim=lumapi.MODE(filename),filename=filename,wavelength=wavelength,wg_length=wg_length,wg_width=wg_width,width_ridge=width_ridge,
             mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,delta_y=delta_y,n_core=n_core,cladding=cladding)





    