from variables import *
from mode_solver import mode_solver
def geometry(sim, filename,y,width_ridge,Radius,mmi_length,wg_length,wg_width,taper_width,taper_width_in,ratio,cut_angle):
    #Loger setup
    delta_y=0
    log = setup_logger("geometry", "logging/geometry.log")
    log.info(f"Starting geometry() built \n width_ridge: {width_ridge}, \n mmi_length:{mmi_length},\n taper_width={taper_width},\n delta_y:{delta_y}")
    #Clean
    sim.switchtolayout()
    sim.deleteall()

    width_eff=width_ridge
    log.info(f"width_eff: {width_eff}")
    mmi_pi_length=4*n_core*(width_eff**2)/3./wavelength
    log.info(f"mmi_pi_length: {mmi_pi_length}")

    distance_wg=width_eff/6 ##effective distance



    #### Geometry calculation #####
    ##Wg bent


    ##Twist angle
    d_phase=2*np.arccos(np.sqrt(ratio)) #phase calculation
    log.info(f"phase must be achieved, to get ratio {ratio} : {d_phase}")
    S=width_ridge/3

    #Calculate neff of launching mode
    # filename_mode="mode_effective_index"
    # import os
    # if os.path.isfile(f"{filename_mode}.lms"):
    #     MODE_SIMULATION=lumapi.MODE(filename=filename_mode)
    # else:
    #     MODE_SIMULATION=lumapi.MODE()

    # N_eff=mode_solver(sim=MODE_SIMULATION,filename=filename_mode,width_ridge=taper_width)[0]
    N_eff=1.600       #Neff of 3rd order mode, if W=Wmmi
    k_0=2*np.pi/wavelength*N_eff
    twist_angle=np.arctan(d_phase/(2*S*k_0))    #use n_eff
    # twist_angle=0 
    log.info(f"Angle of twist is calculated: {twist_angle}")

    #Lenghts
    Y=y #middle section
    X=(mmi_length-Y)/2  #Left and right sections


    #Cut angle ~ 20 degree
    pheta_cut=cut_angle*np.pi/180

    #Side sections
    B=(S-taper_width/2)/np.tan(pheta_cut)
    A=X-B

    #Midle section
    Z=width_ridge/np.tan((np.pi-twist_angle)/2)
    TOP=2*Z+Y
    

    #DRAW LEFT PART
    sim.addstructuregroup()
    sim.set("name","left_part")
 
    # I part
    sim.addrect() 
    sim.set("name","first_part") 
    sim.set("material",material_Si3N4)
    sim.set("y",0)         
    sim.set("y span",width_ridge)
    sim.set("z",0)     
    sim.set("z span", thick_Si3N4)
    sim.set("x",0)  
    sim.set("x span",A)
    
    sim.select("first_part")
    sim.addtogroup("::model::left_part")
    
    #II part

    V = np.zeros((4, 2))
    ly_top=width_ridge
    ly_base=S+taper_width
    x_span=B
    z_span=thick_Si3N4
    z=0
    y=0


    # assign values row by row
    V[0, :] = [-ly_base/2, -x_span/2]
    V[1, :] = [-ly_top/2,  x_span/2]
    V[2, :] = [ ly_top/2,  x_span/2]
    V[3, :] = [ ly_base/2, -x_span/2]


    sim.addpoly()
    sim.set("x",-A/2-B/2)
    sim.set("y",0)
    sim.set("z",z)
    sim.set("z span",z_span)
    sim.set("vertices",V)
    sim.set("material",material_Si3N4)
    sim.set("first axis","z")
    sim.set("rotation 1",-90)
    sim.set("override mesh order from material database",1)
    sim.set("mesh order",1)
    sim.set("name","second_part")
        
    sim.select("second_part")
    sim.addtogroup("::model::left_part")


    # III part

    sim.addtriangle()
    sim.set("name","third_part") 
    sim.set("material",material_Si3N4)
    sim.set("y",0)         
    sim.set("z",0) 
    sim.set("z span",z_span)
    
    sim.set("x",A/2) 


    ly_top=Z
    V = np.zeros((3, 2))

    # assign values row by row
    V[0, :] = [0, -width_ridge/2]
    V[1, :] = [0,width_ridge/2]
    V[2, :] = [Z,  width_ridge/2]

    sim.set("vertices",V)
    
    sim.select("third_part")
    sim.addtogroup("::model::left_part")




    ## Draw tapers
    x_span=wg_length
    ly_top=taper_width
    ly_base=wg_width
    z_span=thick_Si3N4
    z=0
    x=-A/2-B-x_span/2
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
        sim.set("rotation 1",-90)
        sim.set("override mesh order from material database",1)
        sim.set("mesh order",1)
        sim.addtogroup("::model::left_part")

        


    #Draw waveguides
    for ii in range(N_out):
        # bend end of wg to make right angle

        sim.addring()
        sim.set("name",f"bent_output_wg{ii}") 
        sim.set("material",material_Si3N4)
        sim.set("y",(distance_wg+delta_y)*(-1)**ii+Radius)  
        outer_radius=Radius+wg_width/2
        inner_radius=Radius-wg_width/2
        sim.set("outer radius",outer_radius)
        sim.set("inner radius",inner_radius)
        sim.set("theta start",-90-twist_angle*180/np.pi)
        sim.set("theta stop",-90)
        sim.set("z",0)     
        sim.set("z span", thick_Si3N4)
        sim.set("x",-A/2-B-wg_length)  
        sim.addtogroup("::model::left_part")

        
        sim.addrect() 
        sim.set("name",f"output_wg{ii}") 
        sim.set("material",material_Si3N4)
        sim.set("y",(distance_wg+delta_y)*(-1)**ii+wg_length/2*np.tan(twist_angle)+Radius/2*np.tan(twist_angle)*np.sin(twist_angle))         
        sim.set("y span",wg_width)
        sim.set("z",0)     
        sim.set("z span", thick_Si3N4)
        start=x-x_span/2
        sim.set("x max",start-Radius*np.sin(twist_angle)+(1-np.cos(twist_angle))*wg_length/2)
        sim.set("x min",start-wg_length-Radius*np.tan(twist_angle)*np.cos(twist_angle))  
        sim.set("first axis","z")
        sim.set("rotation 1",-twist_angle*180/np.pi)
        sim.addtogroup("::model::left_part")
        sim.save()



    




    
    
    ## GROUP ROTATIONS
    sim.select("::model::left_part")
    sim.set("first axis","z")
    sim.set("rotation 1",twist_angle*180/np.pi)

    sim.set("x",-A/2+(A/2+Z/2)*(1-np.cos(twist_angle))-Y/2-Z)
    sim.set("y",-(A/2+Z/2)*np.sin(twist_angle))


    








    #####################
    ## DRAW Right PART ##
    #####################

    sim.addstructuregroup()
    sim.set("name","right_part")
 
    # I part
    sim.addrect() 
    sim.set("name","first_part") 
    sim.set("material",material_Si3N4)
    sim.set("y",0)         
    sim.set("y span",width_ridge)
    sim.set("z",0)     
    sim.set("z span", thick_Si3N4)
    sim.set("x",0)  
    sim.set("x span",A)
    
    sim.select("first_part")
    sim.addtogroup("::model::right_part")
    
    #II part

    V = np.zeros((4, 2))
    ly_top=width_ridge
    ly_base=S+taper_width
    x_span=B
    z_span=thick_Si3N4
    z=0
    y=0


    # assign values row by row
    V[0, :] = [-ly_base/2, -x_span/2]
    V[1, :] = [-ly_top/2,  x_span/2]
    V[2, :] = [ ly_top/2,  x_span/2]
    V[3, :] = [ ly_base/2, -x_span/2]


    sim.addpoly()
    sim.set("x",-A/2-B/2)
    sim.set("y",0)
    sim.set("z",z)
    sim.set("z span",z_span)
    sim.set("vertices",V)
    sim.set("material",material_Si3N4)
    sim.set("first axis","z")
    sim.set("rotation 1",-90)
    sim.set("override mesh order from material database",1)
    sim.set("mesh order",1)
    sim.set("name","second_part")
        
    sim.select("second_part")
    sim.addtogroup("::model::right_part")


    # III part

    sim.addtriangle()
    sim.set("name","third_part") 
    sim.set("material",material_Si3N4)
    sim.set("y",0)         
    sim.set("z",0) 
    sim.set("z span",z_span)
    
    sim.set("x",A/2) 


    ly_top=Z
    V = np.zeros((3, 2))

    # assign values row by row
    V[0, :] = [0, -width_ridge/2]
    V[1, :] = [0,width_ridge/2]
    V[2, :] = [Z,  -width_ridge/2]

    sim.set("vertices",V)
    
    sim.select("third_part")
    sim.addtogroup("::model::right_part")

    
    ## Draw tapers
    x_span=wg_length
    ly_top=taper_width
    ly_base=wg_width
    z_span=thick_Si3N4
    z=0
    x=-A/2-B-x_span/2
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
        sim.set("rotation 1",-90)
        sim.set("override mesh order from material database",1)
        sim.set("mesh order",1)
        sim.addtogroup("::model::right_part")


    #Draw waveguides
    for ii in range(N_out):
        # bend end of wg to make right angle

        sim.addring()
        sim.set("name",f"bent_output_wg{ii}") 
        sim.set("material",material_Si3N4)
        sim.set("y",(distance_wg+delta_y)*(-1)**ii-Radius)  
        outer_radius=Radius+wg_width/2
        inner_radius=Radius-wg_width/2
        sim.set("outer radius",outer_radius)
        sim.set("inner radius",inner_radius)
        sim.set("theta start",90)
        sim.set("theta stop",90+twist_angle*180/np.pi)
        sim.set("z",0)     
        sim.set("z span", thick_Si3N4)
        sim.set("x",-A/2-B-wg_length)
      
        sim.addtogroup("::model::right_part")

        
        sim.addrect() 
        sim.set("name",f"output_wg{ii}") 
        sim.set("material",material_Si3N4)
        sim.set("y",-((distance_wg+delta_y)*(-1)**ii+wg_length/2*np.tan(twist_angle)+Radius/2*np.tan(twist_angle)*np.sin(twist_angle)))         
        sim.set("y span",wg_width)
        sim.set("z",0)     
        sim.set("z span", thick_Si3N4)
        start=x-x_span/2
        sim.set("x max",start-Radius*np.sin(twist_angle)+(1-np.cos(twist_angle))*wg_length/2)
        sim.set("x min",start-wg_length-Radius*np.tan(twist_angle)*np.cos(twist_angle))  
        sim.set("first axis","z")
        sim.set("rotation 1",+twist_angle*180/np.pi)
        sim.addtogroup("::model::right_part")
        sim.save()

    
    ## GROUP ROTATIONS


    sim.select("::model::right_part")
    sim.set("first axis","z")
    sim.set("rotation 1",180-twist_angle*180/np.pi)
    sim.set("x",A/2-(A/2+Z/2)*(1-np.cos(twist_angle))+Y/2+Z)
    sim.set("y",-(A/2+Z/2)*np.sin(twist_angle))






    ####################
    ## ADD middlepart ##
    ####################
    V = np.zeros((4, 2))
    ly_top=TOP
    ly_base=Y
    x_span=width_ridge
    z_span=thick_Si3N4
    z=0
    y=0
    sim.addstructuregroup()
    sim.set("name","midle_part")

    V[0, :] = [-ly_base/2, -x_span/2]
    V[1, :] = [-ly_top/2,  x_span/2]
    V[2, :] = [ ly_top/2,  x_span/2]
    V[3, :] = [ ly_base/2, -x_span/2]


    sim.addpoly()
    sim.set("x",0)
    sim.set("y",0)
    sim.set("z",z)
    sim.set("z span",z_span)
    sim.set("vertices",V)
    sim.set("material",material_Si3N4)
    sim.set("first axis","z")
    sim.set("override mesh order from material database",1)
    sim.set("mesh order",1)
    sim.set("name","middle_section")

        
    sim.select("middle_section")
    sim.addtogroup("::model::midle_part")

    sim.select("::model::midle_part")
    sim.set("first axis","z")


    ##BOX AND WAFER
        
    Y_span=200e-6
    Xmin_waffer=-(mmi_length+2*wg_length)/2-50e-6
    Xmax_waffer=(mmi_length+2*wg_length)/2+50e-6

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
    return X , twist_angle



if __name__=="__main__":
    filename="mmi_2x2_fdtd"
    wg_length=25e-6
    wg_width=1.6e-6
    width_ridge=11e-6
    mmi_length=81e-6
    taper_width=2.5e-6
    taper_width_in=2.5e-6
    delta_y=0e-6
    n_core=1.9963
    cladding=0
    ratio=50/100

    y=10e-6
    

    import os
    if os.path.isfile(f"{filename}.fsp"):
        geometry(sim=lumapi.FDTD(filename),filename=filename,wg_length=wg_length,wg_width=wg_width,width_ridge=width_ridge,
             mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,ratio=ratio,y=y)
    else:
        geometry(sim=lumapi.FDTD(),filename=filename,wg_length=wg_length,wg_width=wg_width,width_ridge=width_ridge,
             mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,ratio=ratio,y=y)




    