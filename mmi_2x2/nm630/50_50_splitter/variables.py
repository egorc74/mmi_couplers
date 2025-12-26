#mmi_wg_2d_draw
import lumapi
import numpy as np
import logging
import os
# --- Configure logging ---
def setup_logger(name, log_file, level=logging.INFO):
    """Set up a logger that appends to a file. Only create FileHandler once."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Only add handler if the logger has no handlers yet
    if not logger.handlers:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True) if os.path.dirname(log_file) else None
        
        fh = logging.FileHandler(log_file, mode='a')  # append mode
        fh.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    
    return logger

wavelength=0.63e-6
wg_length=62e-6 
wg_width=0.4e-6
thick_Clad=2.0e-6
thick_Si3N4=0.3e-6
thick_BOX=1.5e-6
thick_Slab=0
thick_Substrate=2.0e-6
material_Clad="SiO2 (Glass) - Palik"
material_BOX="SiO2 (Glass) - Palik"
material_Si="Si (Silicon) - Palik"
material_Si3N4="Si3N4 (Silicon Nitride) - Phillip"

n_core=2.0398
n_clad=1.444
cladding=0

with_mesh=0
#MMI
N_in=2
N_out=2

width_margin = 4.0e-6
height_margin = 0.8e-6




