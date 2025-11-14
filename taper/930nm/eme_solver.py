from variables import *
from geometry import taper_geometry
def eme_solver_prep(sim, filename,taper_length,taper_width):
    try:
        log = setup_logger("eme_solver", "logging/eme_solver.log")


        taper_geometry(sim=sim,filename=filename,taper_length=taper_length,taper_width=taper_width)

        ##### Additional variables #######
        Xmin=-taper_length/2 
        Xmax=taper_length/2 #length of wg 4um
        Zmin=-height_margin 
        Zmax=thick_Si3N4 + height_margin
        Y_span=4*width_margin + taper_width 
        Ymin=-Y_span/2 
        Ymax=-Ymin




        sim.addeme()
        sim.set("solver type","3D: X Prop")
        center_z_offset=thick_Si3N4
        sim.set("wavelength",wavelength)
        sim.set("index",1)
        sim.set("z min",-height_margin/2)
        sim.set("z max", height_margin/2)
            

        sim.set("y",0)         
        sim.set("y span",Y_span)
        sim.set("x min",Xmin) 

        sim.set("number of cell groups",1)
        sim.set("display cells",1)
        sim.set("number of modes for all cell groups",20)
        sim.set("number of periodic groups",1)
        sim.set("energy conservation","make passive")
        sim.set("subcell method",np.array([1]))
        sim.set("cells",np.array([20]))
        sim.set("group spans",np.array([taper_length]))
        sim.set("y min bc","Metal")
        sim.set("z min bc","Metal")
        sim.set("y max bc","Metal")
        sim.set("z max bc","metal")

        sim.set("allow custom eigensolver settings",1)
        sim.set("modes",np.array([20,50,20]))
        mesh_cells_y=int((Y_span+1e-6)/wavelength*10)
        sim.set("mesh cells y",mesh_cells_y)
        sim.set("mesh cells z",20)

        #ports
        #### input 1 #####
        sim.setnamed("EME::Ports::port_1","y",0)
        sim.setnamed("EME::Ports::port_1","y span",taper_width+2e-6)
        sim.setnamed("EME::Ports::port_1","z min",-height_margin/2)
        sim.setnamed("EME::Ports::port_1","z max",height_margin/2)
        sim.setnamed("EME::Ports::port_1","mode selection","fundamental TE mode")
        sim.setnamed("EME::Ports::port_1","use full simulation span",0)

        #### input 1 #####
        sim.setnamed("EME::Ports::port_2","y",0)
        sim.setnamed("EME::Ports::port_2","y span",taper_width+2e-6)
        sim.setnamed("EME::Ports::port_2","z min",-height_margin/2)
        sim.setnamed("EME::Ports::port_2","z max",height_margin/2)
        sim.setnamed("EME::Ports::port_2","mode selection","fundamental TE mode")
        sim.setnamed("EME::Ports::port_2","use full simulation span",0)

        #monitors
        sim.addemeprofile()
        sim.set("name","profile")
        sim.set("monitor type","2D Z-normal")
        sim.set("z",0)

        sim.set("y",0)         
        sim.set("y span",Y_span+5e-6)
        sim.set("x min",Xmin)  
        sim.set("x max",Xmax)

        sim.save(filename)
        sim.run()
        sim.save(filename)

        input("Press Enter to continue...")

    except Exception as e:
        log.info(f"Error occured: {e}")



def find_optimal_length(sim):
    log = setup_logger("eme_solver", "logging/eme_solver.log")


    num_p = 801

    sim.emepropagate()
    
    start_len = 40e-6  # common start length
    stop_len  = 120e-6   # common stop length
    # configure EME analysis
    sim.setemeanalysis("override wavelength", 1)
    sim.setemeanalysis("wavelength", wavelength)

    sim.setemeanalysis("propagation sweep", 1)
    sim.setemeanalysis("parameter", "group span 2")
    sim.setemeanalysis("start", start_len)
    sim.setemeanalysis("stop", stop_len)
    sim.setemeanalysis("number of points", num_p)

    # run propagation sweep tool
    sim.emesweep()

    # get propagation sweep result
    S = sim.getemesweep("S")

    s21 = S['s21']  # should be a numpy array

    # assign values to transmission matrix
    length_dx = 0.1e-6
    max_length = 0
    max_trans = 0

    for mm in range(num_p):  # Python indexing starts at 0
        opt_length = start_len + mm * length_dx  # (mm-1) in MATLAB → mm in Python
        trans = np.abs(s21[mm])**2            # elementwise abs^2
        if trans> max_trans:
            max_trans = trans
            max_length = opt_length
    log.info(f"In find_optimal_length: Optimal length : {max_length} , with max transmission {max_trans}")
    return max_length




if __name__=="__main__":
    filename="taper_length_span"
    taper_length=40e-6
    taper_width=2.5e-6
    eme_solver_prep(sim=lumapi.MODE(filename),filename=filename,taper_width=taper_width,taper_length=taper_length)
