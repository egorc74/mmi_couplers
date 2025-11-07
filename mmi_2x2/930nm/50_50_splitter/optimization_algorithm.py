from variables import *
from core_sweep import core_sweep
from taper_width_colormap import taper_width_colormap
from evaluations import core_evaluation,colormap_evaluation
import h5py


def optimization(sim,start_taper):
    log = setup_logger("optimization_algorithm", "logging/optimization_algorithm.log")

    
    ## functions:  1)evaluate -- evaluates deviation and returns curve T(width_ridge)
    ##             2)taper_width_with_deviation returns curve T(taper_width_in)     
    
    ######################## 1 ############################
    ## start with taper width. condition must be met 0.3<= |taper_width/width_ridge|
    ## second condition: Width_eff/4-taper_width/2=> 0.6

    N_MAX_TRIES=5
    MAX_TRANSMISSION_MATRIX=np.zeros((N_MAX_TRIES,3))     #1)transmission 2)taper 3)core_width
    
    log.info(f"Starting optimization algorith with number of tries: {N_MAX_TRIES} ")
                
    filename="mmi_simulations_1x2"
    try:
        width_ridge=8e-6
        mmi_length=50e-6

        for ii in range(N_MAX_TRIES):
            taper_width=start_taper
            taper_width_in=start_taper
            delta_y=0e-6
            
            ## Check first condition
            K_min=0.3
            K_max=0.366
            min_width_1condition=taper_width/(K_max+0.02)
            max_width=taper_width/(K_min-0.02)

            
            #Second condition
            min_width_2condition=4*(1.2e-6 / 2 +taper_width/2)
            min_width=max(min_width_1condition,min_width_2condition)
            start_width=min_width-0.5e-6
            stop_width= max_width+0.5e-6
            step=0.1e-6
            num_steps = int(np.floor((stop_width - start_width) / step)) + 1

            mmi_width_span = np.round(np.linspace(start_width,stop_width,num_steps),7)
            min_w_um = int(start_width * 1e9)   # in nm
            max_w_um = int(stop_width * 1e9)   # in nm
            taper_um = int(taper_width * 1e9) # in nm
            

            data_filename = f"core_sweep_from_{min_w_um}nm_to_{max_w_um}nm_with_taper_{taper_um}nm"
            log.info(f"Optimization itteration {ii} "
                        f"\n min_width_1condition: {min_width_1condition}"
                        f"\n min_width_2condition: {min_width_2condition}"
                        f"\n min_width: {min_width}"
                        f"\n mmi_width_span: {mmi_width_span[:3]}...{mmi_width_span[-3:]}"
                        f"\n taper start_width: {taper_width}")

            ###START ALGORITHM

            ###### Max tries N=10   ######
            log.info(f"Starting core_sweep with data_filename: {data_filename} ")
            # if ii==0:
                            
            #     transmission_core_matrix = np.load("core_sweep_from_5756nm_to_7642nm_with_taper_2000nm.npy", allow_pickle=True)
            # else:
            transmission_core_matrix=core_sweep(sim, filename=filename,data_filename=data_filename,mmi_width_span=mmi_width_span,
                                                width_ridge=width_ridge,mmi_length=mmi_length,taper_width=taper_width,
                                                    taper_width_in=taper_width, delta_y=0)
            optimal_curve=core_evaluation(transmission_matrix=transmission_core_matrix,width_span=mmi_width_span,taper_width=taper_width,plot=1)
            ##Find max of optimal curve
            trimmed_curve = optimal_curve[5:-5, 0]   # keep only the middle part
         
            # Find max value and its index relative to trimmed array
            max_value_from_core_sweep = np.max(trimmed_curve)
            max_index_trimmed = np.argmax(trimmed_curve)

            #calculate index relative to the full curve:
            max_index = max_index_trimmed + 5
            #new core width
            opt_width_from_core_sweep=mmi_width_span[max_index]
            log.info(f"After core_evaluation\n trimmed_curve: {trimmed_curve[:3]}...{trimmed_curve[-3:]}"
                        f"\n optimal_curve: {optimal_curve[:3]}...{optimal_curve[-3:]}"
                        f"\n max_value_from_core_sweep: {max_value_from_core_sweep}"
                        f"\n opt_width_from_core_sweep: {opt_width_from_core_sweep}")
            

            #calculate colourmap around opt_width_from_core_sweep and taper
            opt_width_um=int(opt_width_from_core_sweep * 1e9) 
            data_filename=f"taper_width_colormap_{taper_um}_{opt_width_um}nm"
            log.info(f"Starting taper_width_colormap with data_filename: {data_filename} ")

            colormap_transmission_matrix,colormap_taper_width_span,colormap_mmi_width_span=taper_width_colormap(sim=sim,filename=filename,data_filename=data_filename,
                                                                                    width_ridge=opt_width_from_core_sweep,
                                                                                        taper_width=taper_width,taper_width_in=taper_width,mmi_length=mmi_length)
            optimal_curve=colormap_evaluation(transmission_matrix=colormap_transmission_matrix,
                                            colormap_taper_span=colormap_taper_width_span,
                                            colormap_width_span=colormap_mmi_width_span)
            ##Find max of optimal curve
            max_value_from_colormap = np.max(optimal_curve)
            max_index = np.argmax(optimal_curve)
            opt_taper_width_from_colormap=colormap_taper_width_span[max_index]
            log.info(f"After taper_width_colormap"
                        f"\n optimal_curve: {optimal_curve[:3]}...{optimal_curve[-3:]}"
                        f"\n max_value_from_core_sweep: {max_value_from_colormap}"
                        f"\n opt_width_from_core_sweep: {opt_taper_width_from_colormap}")
            

            
            ####compare max values
            if (max_value_from_colormap >= max_value_from_core_sweep-0.005):
                start_taper=opt_taper_width_from_colormap
                MAX_TRANSMISSION_MATRIX[ii,0]=max_value_from_colormap
                MAX_TRANSMISSION_MATRIX[ii,1]=opt_taper_width_from_colormap
                MAX_TRANSMISSION_MATRIX[ii,2]=opt_width_from_core_sweep
                log.info(f"In {ii} itteration colormap gave better results"
                             f"\n max_value_from_colormap{MAX_TRANSMISSION_MATRIX[ii,0]}"
                             f"\n opt_taper_width_from_colormap{MAX_TRANSMISSION_MATRIX[ii,1]}"
                             f"\n opt_width_from_colormap{MAX_TRANSMISSION_MATRIX[ii,2]}")

                
            else:
                start_taper=start_taper-0.2e-6
                log.info(f"In {ii} itteration core_width  gave better results."
                             f"\n starting with new start_taper_width: {start_taper}")

        np.save("max_transmission_matrix.npy", MAX_TRANSMISSION_MATRIX)
    except Exception as e:
        np.save("max_transmission_matrix.npy", MAX_TRANSMISSION_MATRIX)
        log.error(f"Error occured {e}. Start saving transmission_matrix")


if __name__=="__main__":
    start_taper=3e-6
    filename="mmi_simulations_1x2"
    optimization(sim=lumapi.MODE(filename),start_taper=start_taper)