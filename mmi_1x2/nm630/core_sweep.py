


from variables import *
from eme_solver import eme_solver_prep
from taper_width_colormap import taper_width_colormap

def core_sweep(sim, filename,data_filename,mmi_width_span,width_ridge,mmi_length,
                    taper_width,taper_width_in, delta_y):
    log = setup_logger("core_sweep", "logging/core_sweep.log")

    log.info(f"Starting core_sweep() \n data_filename: {data_filename} \n mmi_width_span: {mmi_width_span}\n width_ridge: {width_ridge}, \n mmi_length:{mmi_length},\n taper_width={taper_width},\n delta_y:{delta_y}")
    try:
        # sweep parameters
        num_p = 801  # number of propagation points

        # transmission_matrix shape: [len(mmi_width_span), num_p, 2]
        transmission_matrix = np.zeros((len(mmi_width_span), num_p, 2))

        # ---------------------------------------------------------
        # Width sweep
        # ---------------------------------------------------------
        for dd, width_val in enumerate(mmi_width_span):
            sim.switchtolayout()
            sim.deleteall()

            width_ridge = width_val  # update width for this sweep

            eme_solver_prep(sim=sim,filename=filename,width_ridge=width_ridge,
                mmi_length=mmi_length,taper_width=taper_width,
                    taper_width_in=taper_width_in,delta_y=delta_y)
            
            sim.emepropagate()

            start_len = 80e-6
            stop_len  = 150e-6

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
            s21 = S['s21'] # (num_p × outputs)
            log.info(f"obtained S matrix for {width_ridge} with shape {s21.shape}")
            
            length_dx = 0.1e-6
            for mm in range(num_p):
                transmission_matrix[dd, mm, 0] = start_len + mm * length_dx
                transmission_matrix[dd, mm, 1] = np.abs(s21[mm])**2

        # ---------------------------------------------------------
        # Save data
        # ---------------------------------------------------------
        sim.savedata(f"data/{data_filename}")
        np.save(f"data/{data_filename}.npy",transmission_matrix)
         
        log.info(f"data from core_sweep is saved in {data_filename}"
                    f"with transmission_matrix.shape= {transmission_matrix.shape}")

        return transmission_matrix
    except Exception as e:
        log.error(f"in core_sweep error occured:{e}") 

if __name__=="__main__":
    filename="mmi_simulations_1x2"
    data_filename="core_sweep_from_7500nm_to_10500nm_with_taper_3000nm"
    mmi_width_span=np.linspace(7.5,10.5,31)*1e-6
    width_ridge=8.3e-6
    taper_width=3e-6
    mmi_length=101e-6
    transmission_core_matrix=core_sweep(sim=lumapi.MODE(filename), filename=filename,data_filename=data_filename,mmi_width_span=mmi_width_span,
                                                width_ridge=width_ridge,mmi_length=mmi_length,taper_width=taper_width,
                                                    taper_width_in=taper_width, delta_y=0)


 


