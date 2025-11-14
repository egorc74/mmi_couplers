from variables import *
from geometry import geometry
import plotly.graph_objects as go
def eme_solver_prep(sim, filename,width_ridge,mmi_length,taper_width,taper_width_in, delta_y):
    try:
        log = setup_logger("eme_solver", "logging/eme_solver.log")

        log.info(f"Starting eme_solver_prep()s \n width_ridge: {width_ridge}, \n mmi_length:{mmi_length},\n taper_width={taper_width},\n delta_y:{delta_y}")


        geometry(sim=sim,filename=filename,width_ridge=width_ridge,
                mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,
                    delta_y=delta_y)


        ##### Additional variables #######
        Xmin=-mmi_length/2 
        Xmax=mmi_length/2 #length of wg 4um
        Zmin=-height_margin 
        Zmax=thick_Si3N4 + height_margin
        Y_span=2*width_margin + width_ridge 
        Ymin=-Y_span/2 
        Ymax=-Ymin
        Xmin_waffer=Xmin-wg_length-4e-6
        Xmax_waffer=Xmax+wg_length+4e-6
        x_span=wg_length
        # width_eff=width_ridge+(wavelength/3.141592654)*(n_core**2-n_clad**2)**(-1/2)
        width_eff=width_ridge

        distance_wg=width_eff/6  ##effective distance




        sim.addeme()
        sim.set("solver type","3D: X Prop")
        center_z_offset=thick_Si3N4
        sim.set("wavelength",wavelength)
        sim.set("index",1)
        sim.set("z min",-height_margin/2)
        sim.set("z max", height_margin/2)
            

        sim.set("y",0)         
        sim.set("y span",Y_span+1e-6)
        sim.set("x min",Xmin_waffer+4e-6) 
        sim.set("number of cell groups",3)
        sim.set("display cells",1)
        sim.set("number of modes for all cell groups",20)
        sim.set("number of periodic groups",1)
        sim.set("energy conservation","make passive")
        sim.set("subcell method",np.array([1,0,1]))
        sim.set("cells",np.array([15,1,15]))
        sim.set("group spans",np.array([wg_length,mmi_length,wg_length]))
        sim.set("y min bc","Metal")
        sim.set("z min bc","Metal")
        sim.set("y max bc","Metal")
        sim.set("z max bc","metal")

        sim.set("allow custom eigensolver settings",1)
        sim.set("modes",np.array([20,50,20]))
        mesh_cells_y=int((Y_span+1e-6)/wavelength*10)
        sim.set("mesh cells y",mesh_cells_y)
        sim.set("mesh cells z",20)

        if(with_mesh==1):
            #input mesh 1
            x=Xmin-x_span/2
            sim.addmesh()
            sim.set("z",0)
            sim.set("z span",thick_Si3N4)
            sim.set("y",(distance_wg+delta_y)*(-1))         
            sim.set("y span",taper_width)
            sim.set("x",x)  
            sim.set("x span",x_span)
            sim.set("override x mesh",0)
            sim.set("y mesh multiplier",1)
            sim.set("z mesh multiplier",1)

            sim.set("name","input mesh")
            #input mesh 2
            x=Xmin-x_span/2
            sim.addmesh()
            sim.set("z",0)
            sim.set("z span",thick_Si3N4)
            sim.set("y",(distance_wg+delta_y)*(1))         
            sim.set("y span",taper_width)
            sim.set("x",x)  
            sim.set("x span",x_span)
            sim.set("override x mesh",0)
            sim.set("y mesh multiplier",1)
            sim.set("z mesh multiplier",1)

            sim.set("name","input mesh")


        #with output mesh 1\
            x=Xmax+x_span/2
            sim.addmesh()
            sim.set("z",0)
            sim.set("z span",thick_Si3N4)
            sim.set("y",(distance_wg+delta_y)*(-1)) 
            sim.set("y span",taper_width)
            sim.set("x",x)  
            sim.set("x span",x_span)
            sim.set("override x mesh",0)
            sim.set("y mesh multiplier",1)
            sim.set("z mesh multiplier",1)
            sim.set("name","output mesh1")
            #with output mesh 2
            sim.addmesh()
            sim.set("z",0)
            sim.set("z span",thick_Si3N4)
            sim.set("y",(distance_wg+delta_y)*(1)) 
            sim.set("y span",taper_width)
            sim.set("x",x)  
            sim.set("x span",x_span)
            sim.set("override x mesh",0)
            sim.set("y mesh multiplier",1)
            sim.set("z mesh multiplier",1)
            sim.set("name","output mesh2")
        




        #ports
        #### input 1 #####
        sim.setnamed("EME::Ports::port_1","y",(distance_wg+delta_y)*(1))
        sim.setnamed("EME::Ports::port_1","y span",wg_width+1e-6)
        sim.setnamed("EME::Ports::port_1","z min",-height_margin/2)
        sim.setnamed("EME::Ports::port_1","z max",height_margin/2)
        sim.setnamed("EME::Ports::port_1","mode selection","fundamental TE mode")
        sim.setnamed("EME::Ports::port_1","use full simulation span",0)

        sim.addemeport()
        sim.set("port location","right")
        sim.setnamed("EME::Ports::port_3","y",(distance_wg+delta_y)*(1))
        sim.setnamed("EME::Ports::port_3","y span",wg_width+1e-6)
        sim.setnamed("EME::Ports::port_3","z min",-height_margin/2)
        sim.setnamed("EME::Ports::port_3","z max",height_margin/2)
        sim.setnamed("EME::Ports::port_3","mode selection","fundamental TE mode")
        sim.setnamed("EME::Ports::port_3","use full simulation span",0)      

        sim.setnamed("EME::Ports::port_2","port location","left")
        sim.setnamed("EME::Ports::port_2","y",(distance_wg+delta_y)*(-1))
        sim.setnamed("EME::Ports::port_2","y span",wg_width+1e-6)
        sim.setnamed("EME::Ports::port_2","z min",-height_margin/2)
        sim.setnamed("EME::Ports::port_2","z max",height_margin/2)
        sim.setnamed("EME::Ports::port_2","mode selection","fundamental TE mode")
        sim.setnamed("EME::Ports::port_2","use full simulation span",0)

        sim.addemeport()
        sim.set("port location","right")
        sim.setnamed("EME::Ports::port_4","y",(distance_wg+delta_y)*(-1))
        sim.setnamed("EME::Ports::port_4","y span",wg_width+1e-6)
        sim.setnamed("EME::Ports::port_4","z min",-height_margin/2)
        sim.setnamed("EME::Ports::port_4","z max",height_margin/2)
        sim.setnamed("EME::Ports::port_4","mode selection","fundamental TE mode")
        sim.setnamed("EME::Ports::port_4","use full simulation span",0)


        #monitors
        sim.addemeprofile()
        sim.set("name","profile")
        sim.set("monitor type","2D Z-normal")
        sim.set("z",0)

        sim.set("y",0)         
        sim.set("y span",Y_span+5e-6)
        sim.set("x min",Xmin_waffer)  
        sim.set("x max",Xmax_waffer)

        sim.save(filename)
        sim.run()
    except Exception as e:
        log.info(f"Error occured: {e}")



def find_optimal_length(sim,plot=None):
    log = setup_logger("eme_solver", "logging/eme_solver.log")


    num_p = 601

    sim.emepropagate()
    
    start_len = 100e-6  # common start length
    stop_len  = 160e-6   # common stop length
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

    s41 = S['s41']  # should be a numpy array

    # assign values to transmission matrix
    length_dx = 0.1e-6
    max_length = 0
    max_trans = 0

    for mm in range(num_p):  # Python indexing starts at 0
        opt_length = start_len + mm * length_dx  # (mm-1) in MATLAB → mm in Python
        trans = np.abs(s41[mm])**2            # elementwise abs^2
        if trans> max_trans:
            max_trans = trans
            max_length = opt_length
    log.info(f"In find_optimal_length: Optimal length : {max_length} , with max transmission {max_trans}")
    if plot!= None:
        s31 = S['s31']
        curve_41=np.abs(s41[:])**2
        curve_31=np.abs(s31[:])**2
        x=np.linspace(start_len,stop_len,num_p)

        fig = go.Figure()

        # Add first curve
        fig.add_trace(go.Scatter(x=x, y=curve_41, mode='lines', name='Curve 41'))

        # Add second curve
        fig.add_trace(go.Scatter(x=x, y=curve_31, mode='lines', name='Curve 31'))

        # Labels & layout
        fig.update_layout(
        title="Two Curves over X",
        xaxis_title="X",
        yaxis_title="Value",
        template="plotly_white"
        )

        fig.show()    
    
    
    return max_length




if __name__=="__main__":
    filename="mmi_simulations_2x2"
    #### for W_mmi = 11 e-6 ######
    # width_ridge=11e-6
    # mmi_length=80*2e-6
    # taper_width=2.5e-6
    # taper_width_in=2.5e-6


    #### for W_mmi = 8.1 e-6 ######
    width_ridge=8.1e-6
    mmi_length=80*2e-6
    taper_width=1.6e-6
    taper_width_in=1.6e-6


    
    delta_y=0e-6
    sim=lumapi.MODE(filename)
    eme_solver_prep(sim=sim,filename=filename,width_ridge=width_ridge,
                    mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,
                        delta_y=delta_y)
    # print(find_optimal_length(sim=sim,plot=1))
  