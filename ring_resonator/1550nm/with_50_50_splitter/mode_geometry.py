from variables import *
def geometry(sim, filename,mmi_width,mmi_length,taper_width,taper_width_in, delta_y,curved_tapers=False):

    log = setup_logger("geometry", "logging/geometry.log")

    log.info(f"Starting geometry() built \n mmi_width: {mmi_width}, \n mmi_length:{mmi_length},\n taper_width={taper_width},\n delta_y:{delta_y}")




    #mmi length
    sim.switchtolayout()
    sim.deleteall()




    # set the material properties
    try:
        sim.setmaterial(sim.addmaterial("(n,k) Material"), "name", "air");  
        sim.setmaterial("air", {"Refractive Index": 1, "Imaginary Refractive Index": 0})
        color=np.zeros((1,4))
        color[:]=0.01
        sim.setmaterial("air", "color",color )

    except:
        pass

    # width_eff=mmi_width+(wavelength/3.141592654)*(n_core**2-n_clad**2)**(-1/2)
    width_eff=mmi_width

    log.info(f"width_eff: {width_eff}")
    mmi_pi_length=4*n_core*(width_eff**2)/3./wavelength
    log.info(f"mmi_pi_length: {mmi_pi_length}")
    Xmin=-mmi_length/2 
    Xmax=mmi_length/2 #length of wg 4um
    Zmin=-height_margin 
    Zmax=thick_Si3N4 + height_margin
    Y_span=2*width_margin + mmi_width 
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
    sim.set("y span",mmi_width)
    sim.set("z",0)     
    sim.set("z span", thick_Si3N4)
    sim.set("x min",Xmin)  
    sim.set("x max",Xmax)
    sim.set("override mesh order from material database",1)
    sim.set("mesh order",1)

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


    distance_wg=width_eff/6 ##effective distance




#draw box and waffer
    
    sim.addrect() 
    sim.set("name","BOX") 
    sim.set("material",material_BOX)
    sim.set("y",0)         
    sim.set("y span",Y_span+100e-6)
    sim.set("z min",-thick_BOX)     
    sim.set("z max", 0-thick_Si3N4/2)
    sim.set("x min",Xmin_waffer-50e-6)  
    sim.set("x max",Xmax_waffer+50e-6)
    sim.set("alpha",0.05)

    #draw waffer
    sim.addrect() 
    sim.set("name","Wafer") 
    sim.set("material",material_Si)
    sim.set("y",0)         
    sim.set("y span",Y_span+100e-6)
    sim.set("z min",-thick_BOX-thick_Substrate)     
    sim.set("z max", -thick_BOX)
    sim.set("x min",Xmin_waffer-50e-6)  
    sim.set("x max",Xmax_waffer+50e-6)
    sim.set("alpha",0.1)
    sim.save(filename)



#Draw curved tapers
    if(curved_tapers):
#draw curved tapered wg
        for i in range(2):
            sim.addcustom()
            sim.set("name",f"Curved Taper{i}") 
            sim.set("material",material_Si3N4)
            sim.set("y",0)         
            sim.set("y span",100e-6)
            sim.set("z",0)     
            sim.set("z span", thick_Si3N4)
            sim.set("x",mmi_length/2 *(-1)**i)  
            sim.set("x span",Radius*2)
            sim.set("override mesh order from material database",1)
            sim.set("equation 1",f"-sqrt((18.5+0.7/16*abs(x))^2-x^2)+21.5")
            sim.set("make nonsymmetric",1)
            sim.set("equation 2","0")
            sim.set("mesh order",4)
    #draw etch 
            sim.addcustom()
            sim.set("name",f"Curved Taper {i} (Etch)") 
            sim.set("material","air")
            sim.set("y",0)         
            sim.set("y span",100e-6)
            sim.set("z",0)     
            sim.set("z span", thick_Si3N4)
            sim.set("x",mmi_length/2*(-1)**i)  
            sim.set("x span",Radius*2)
            sim.set("override mesh order from material database",1)
            sim.set("equation 1",f"-sqrt((21.5-0.7/16*abs(x))^2-x^2)+21.5")
            sim.set("make nonsymmetric",1)
            sim.set("equation 2","0")
            sim.set("mesh order",3)


    #draw air for other half

            sim.addrect() 
            sim.set("name","Air") 
            sim.set("material","air")
            sim.set("x",mmi_length/4 *(-1)**i)         
            sim.set("x span",mmi_length/2)
            sim.set("z",0)     
            sim.set("z span", thick_Si3N4)
            sim.set("y min",mmi_width/2)  
            sim.set("y max",mmi_width/2+Radius)
            sim.set("alpha",1)
            sim.set("override mesh order from material database",1)

            sim.set("mesh order",2)
        

        ##draw input wg
        sim.addrect() 
        sim.set("name",f"input_wg") 
        sim.set("material",material_Si3N4)
        sim.set("y",(distance_wg+delta_y)*(-1))         
        sim.set("y span",wg_width)
        sim.set("z",0)     
        sim.set("z span", thick_Si3N4)
        sim.set("x min",Xmin_waffer)  
        sim.set("x max",Xmin_waffer+wg_length)

        ##draw output wg

        sim.addrect() 
        sim.set("name",f"output_wg") 
        sim.set("material",material_Si3N4)
        sim.set("y",(distance_wg+delta_y)*(-1))         
        sim.set("y span",wg_width)
        sim.set("z",0)     
        sim.set("z span", thick_Si3N4)
        sim.set("x min",Xmax_waffer-wg_length)  
        sim.set("x max",Xmax_waffer)



        #draw tapers output
        x_span=wg_length

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
        sim.addpoly()
        sim.set("x",x)
        sim.set("y",(distance_wg+delta_y)*(-1))
        sim.set("z",z)
        sim.set("z span",z_span)
        sim.set("vertices",V)
        sim.set("material",material_Si3N4)
        sim.set("name",f"taper_output")
        sim.set("first axis","z")
        sim.set("rotation 1",90)
        sim.set("override mesh order from material database",1)
        sim.set("mesh order",1)


    #input taper
        ly_top=taper_width_in
        ly_base=wg_width
        x_span=wg_length
        z_span=thick_Si3N4
        z=0
        x=Xmin-x_span/2
        y=0

        V[0, :] = [-ly_base/2, -x_span/2]
        V[1, :] = [-ly_top/2,  x_span/2]
        V[2, :] = [ ly_top/2,  x_span/2]
        V[3, :] = [ ly_base/2, -x_span/2]

        sim.addpoly()
        sim.set("x",x)
        sim.set("y",(distance_wg+delta_y)*(-1))
        sim.set("z",z)
        sim.set("z span",z_span)
        sim.set("vertices",V)
        sim.set("material",material_Si3N4)
        sim.set("name",f"taper_input")
        sim.set("first axis","z")
        sim.set("rotation 1",-90)
        sim.set("override mesh order from material database",1)
        sim.set("mesh order",1)
        






        ##Draw two half Rings
        sim.addring()
        sim.set("name",f"left half ring") 
        sim.set("material",material_Si3N4)
        sim.set("y",mmi_width/2+Radius-mmi_width/3)  
        outer_radius=Radius+wg_width/2
        inner_radius=Radius-wg_width/2
        sim.set("outer radius",outer_radius)
        sim.set("inner radius",inner_radius)
        sim.set("theta start",90)
        sim.set("theta stop",-90)
        sim.set("z",0)     
        sim.set("z span", thick_Si3N4)
        sim.set("x",-mmi_length/2)  

        sim.addring()
        sim.set("name",f"left half ring") 
        sim.set("material",material_Si3N4)
        sim.set("y",mmi_width/2+Radius-mmi_width/3)  
        outer_radius=Radius+wg_width/2
        inner_radius=Radius-wg_width/2
        sim.set("outer radius",outer_radius)
        sim.set("inner radius",inner_radius)
        sim.set("theta start",-90)
        sim.set("theta stop",90)
        sim.set("z",0)     
        sim.set("z span", thick_Si3N4)
        sim.set("x",mmi_length/2)  

    #Conecting Wg
        sim.addrect() 
        sim.set("name",f"output_wg") 
        sim.set("material",material_Si3N4)
        sim.set("y",mmi_width/2+2*Radius-mmi_width/3)         
        sim.set("y span",wg_width)
        sim.set("z",0)     
        sim.set("z span", thick_Si3N4)
        sim.set("x",0)  
        sim.set("x span",mmi_length)
        
        ring_path=2*mmi_length+np.pi*2*Radius + wg_length*2
        

    





########################
########################
## WITHOUT CURVED TAPERS
########################
    else:

        sim.addrect() 
        sim.set("name",f"input_wg") 
        sim.set("material",material_Si3N4)
        sim.set("y",(distance_wg+delta_y)*(-1))         
        sim.set("y span",wg_width)
        sim.set("z",0)     
        sim.set("z span", thick_Si3N4)
        sim.set("x min",Xmin_waffer)  
        sim.set("x max",Xmin_waffer+wg_length)

        ##draw output wg

        sim.addrect() 
        sim.set("name",f"output_wg") 
        sim.set("material",material_Si3N4)
        sim.set("y",(distance_wg+delta_y)*(-1))         
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

        for ii in range(N_in):
            sim.addpoly()
            sim.set("x",x)
            sim.set("y",(distance_wg+delta_y)*(-1)**ii)
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
        for ii in range(N_out):
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


    ##Draw two half Rings
        sim.addring()
        sim.set("name",f"left half ring") 
        sim.set("material",material_Si3N4)
        sim.set("y",mmi_width/2+Radius-mmi_width/3)  
        outer_radius=Radius+wg_width/2
        inner_radius=Radius-wg_width/2
        sim.set("outer radius",outer_radius)
        sim.set("inner radius",inner_radius)
        sim.set("theta start",90)
        sim.set("theta stop",-90)
        sim.set("z",0)     
        sim.set("z span", thick_Si3N4)
        sim.set("x",-mmi_length/2-wg_length)  

        sim.addring()
        sim.set("name",f"left half ring") 
        sim.set("material",material_Si3N4)
        sim.set("y",mmi_width/2+Radius-mmi_width/3)  
        outer_radius=Radius+wg_width/2
        inner_radius=Radius-wg_width/2
        sim.set("outer radius",outer_radius)
        sim.set("inner radius",inner_radius)
        sim.set("theta start",-90)
        sim.set("theta stop",90)
        sim.set("z",0)     
        sim.set("z span", thick_Si3N4)
        sim.set("x",mmi_length/2+wg_length)  

    #Conecting Wg
        sim.addrect() 
        sim.set("name",f"output_wg") 
        sim.set("material",material_Si3N4)
        sim.set("y",mmi_width/2+2*Radius-mmi_width/3)         
        sim.set("y span",wg_width)
        sim.set("z",0)     
        sim.set("z span", thick_Si3N4)
        sim.set("x",0)  
        sim.set("x span",mmi_length + wg_length*2)
        
        ring_path=2*mmi_length+np.pi*2*Radius + wg_length*2
    
    
    
    





if __name__=="__main__":
    filename="mrr_with_50_50_splitter"
    wavelength=1.55e-6
    wg_length=25e-6
    wg_width=1.6e-6
    mmi_width=9e-6
    mmi_length=50e-6
    taper_width=3.0e-6
    taper_width_in=3.0e-6
    delta_y=0e-6
    n_core=1.9963
    cladding=0
    geometry(sim=lumapi.MODE(), filename=filename,mmi_width=mmi_width,
             mmi_length=mmi_length,taper_width=taper_width,
             taper_width_in=taper_width_in, delta_y=delta_y,curved_tapers=True)



    