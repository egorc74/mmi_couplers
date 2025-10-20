import numpy as np
from variables import *
from eme_solver import eme_solver_prep, find_optimal_length
def taper_width_colormap(
    sim, filename,data_filename, width_ridge, mmi_length,
    taper_width, taper_width_in, delta_y=0):
    log = setup_logger("taper_width_colormap", "logging/taper_width_colormap.log")

    """
    Sweep taper width and MMI width deviations to build transmission matrix.
    """
    log.info(f"Starting taper_width_colormap() \n data_filename: {data_filename} \n width_ridge: {width_ridge}, \n mmi_length:{mmi_length},\n taper_width={taper_width},\n delta_y:{delta_y}")
    try:
        # Parameters for sweep
        span = 0.5e-6
        taper_width_span = np.linspace(taper_width_in - span, taper_width_in + span, 11)
        mmi_width_span = np.linspace(width_ridge - span, width_ridge + span, 11)
        log.info(f" In taper_width_colormap() width_span {mmi_width_span},"
                    f"with taper span {taper_width_span}")

        transmission_matrix = np.zeros((len(taper_width_span), len(mmi_width_span)))
        

        eme_solver_prep(sim=sim,filename=filename,width_ridge=width_ridge,
                                mmi_length=mmi_length,taper_width=taper_width,
                                    taper_width_in=taper_width_in,delta_y=delta_y)
        optimal_length=find_optimal_length(sim=sim)
            
        # Outer loop: taper width sweep
        for kkk, taper_val in enumerate(taper_width_span):
            taper_width = taper_val
            taper_width_in = taper_val
            width_ridge = width_ridge

            sim.switchtolayout()
            sim.deleteall()

            # ---------------------------------------------------------
            # Length optimization for given taper width
            # ---------------------------------------------------------
            eme_solver_prep(sim=sim,filename=filename,width_ridge=width_ridge,
                                mmi_length=mmi_length,taper_width=taper_width,
                                    taper_width_in=taper_width_in,delta_y=delta_y)
            

            ###find optimal length and make 15e-6 span around it
        
            num_p = 301
            length_span=15e-6
            start_len = optimal_length-length_span
            stop_len = optimal_length+length_span

            sim.setemeanalysis("override wavelength", 1)
            sim.setemeanalysis("wavelength", wavelength)

            sim.setemeanalysis("propagation sweep", 1)
            sim.setemeanalysis("parameter", "group span 2")
            sim.setemeanalysis("start", start_len)
            sim.setemeanalysis("stop", stop_len)
            sim.setemeanalysis("number of points", num_p)
            log.info(f"Propagated from  {start_len} to {stop_len}")

            sim.emesweep()

            S = sim.getemesweep("S")
            s21 = S['s21']  # shape: (num_p, outputs)

            length_dx = 0.1e-6
            max_length = 0
            max_trans = 0

            for mm in range(num_p):
                opt_length = start_len + mm * length_dx
                trans = np.abs(s21[mm])**2
                if trans > max_trans:
                    max_trans = trans
                    max_length = opt_length
            log.info(f"In taper_width_colormap obtained max_trans:{max_trans},"
                            f"optimal_length: {max_length} for width_ridge{width_ridge}")
            mmi_length = max_length

            # ---------------------------------------------------------
            # Inner loop: MMI width sweep
            # ---------------------------------------------------------
            for lll, mmi_width in enumerate(mmi_width_span):
                sim.switchtolayout()
                sim.deleteall()

                itterating_width_ridge = mmi_width  # set new ridge width
                eme_solver_prep(sim=sim,filename=filename,width_ridge=itterating_width_ridge,
                        mmi_length=mmi_length,taper_width=taper_width,
                            taper_width_in=taper_width_in,delta_y=delta_y)
                        
                sim.emepropagate()

                start_len = wg_length
                stop_len = wg_length + 0.01e-6
                num_p = 2

                sim.setemeanalysis("override wavelength", 1)
                sim.setemeanalysis("wavelength", wavelength)

                sim.setemeanalysis("propagation sweep", 1)
                sim.setemeanalysis("parameter", "group span 1")
                sim.setemeanalysis("start", start_len)
                sim.setemeanalysis("stop", stop_len)
                sim.setemeanalysis("number of points", num_p)

                sim.emesweep()

                S = sim.getemesweep("S")
                s21 = S['s21']

                transmission_matrix[kkk, lll] = np.abs(s21[0])**2
            log.info(f"In taper_width_colormap obtained transmission_matrix with shape {transmission_matrix.shape}")

        # ---------------------------------------------------------
        # Save results
        # ---------------------------------------------------------
        sim.savedata(f"data/{data_filename}")
        np.save(f"data/{data_filename}.npy",transmission_matrix)
    
        return transmission_matrix,taper_width_span,mmi_width_span
    except Exception as e:
        log.error(f"in taper_width_colormap() error occured:{e}")
if __name__=="__main__":
    data_filename="taper_width_colormap_4400_11000nm"
    filename="mmi_simulations_1x2"
    width_ridge=11e-6
    taper_width=4.4e-6
    mmi_length=60e-6
   

    import os   
    if os.path.isfile(f"{filename}.lms"):
        sim=lumapi.MODE(filename)
    else:
        sim=lumapi.MODE()

    colormap_transmission_matrix,colormap_taper_width_span,colormap_mmi_width_span=taper_width_colormap(sim=sim,filename=filename,data_filename=data_filename,
                                                                                    width_ridge=width_ridge,
                                                                                        taper_width=taper_width,taper_width_in=taper_width,mmi_length=mmi_length)
    



