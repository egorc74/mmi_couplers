#mmi_wg_2d_draw
import lumapi
import numpy as np
import logging
import os
import inspect

# Get the directory where this script is located (nm1550 directory)
NM1550_DIR = os.path.dirname(os.path.abspath(__file__))
# --- Configure logging ---
def setup_logger(name, log_file, level=logging.INFO):
    """Set up a logger that appends to a file. Only create FileHandler once.
    
    If log_file is a relative path, it will be resolved relative to the calling script's directory,
    not the current working directory. This ensures logs are saved in the correct location regardless
    of where the script is executed from.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Only add handler if the logger has no handlers yet
    if not logger.handlers:
        # If log_file is a relative path, resolve it relative to the caller's script directory
        if not os.path.isabs(log_file):
            # Get the caller's file path (skip this function and any intermediate frames)
            frame = inspect.currentframe()
            try:
                caller_frame = frame.f_back
                while caller_frame:
                    caller_file = caller_frame.f_globals.get('__file__')
                    if caller_file and caller_file != __file__:
                        # Found the caller's file
                        caller_dir = os.path.dirname(os.path.abspath(caller_file))
                        log_file = os.path.join(caller_dir, log_file)
                        break
                    caller_frame = caller_frame.f_back
                else:
                    # Fallback: use current working directory if we can't find caller
                    log_file = os.path.abspath(log_file)
            finally:
                del frame
        
        # Ensure the directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        
        fh = logging.FileHandler(log_file, mode='a')  # append mode
        fh.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    
    return logger

wavelength=1.55e-6
wg_length=20e-6 


wg_width=1.6e-6
thick_Clad=2.0e-6
thick_Si3N4=0.3e-6
thick_BOX=1.5e-6
thick_Slab=0
thick_Substrate=2.0e-6
material_Clad="SiO2 (Glass) - Palik"
material_BOX="SiO2 (Glass) - Palik"
material_Si="Si (Silicon) - Palik"
material_Si3N4="Si3N4 (Silicon Nitride) - Phillip"

n_core=1.9963
n_clad=1.444
cladding=0

with_mesh=0
#MMI
N_in=1
N_out=2

width_margin = 2.0e-6
height_margin = 1.0e-6


##### Optimal values for 1x2 -3dB mmi splitter

opt_wg_length=20e-6
opt_width_ridge=9.5e-6
opt_mmi_length=47e-6
opt_taper_width=3.6e-6 
opt_wg_width=1.6e-6 

minimal_output_distance=1.1e-6

##Monitor Data
frequency_points=5
wavelength_span=0.1e-6



#file names
# Always save in the nm1550 directory, regardless of where the script is called from
filename_fdtd = os.path.join(NM1550_DIR, "mmi_1x2_fdtd")
