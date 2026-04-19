from variables import *
from fdtd_solver import *
# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Create necessary directories relative to script location
os.makedirs(os.path.join(SCRIPT_DIR, "chunks"), exist_ok=True)
os.makedirs(os.path.join(SCRIPT_DIR, "data"), exist_ok=True)
os.makedirs(os.path.join(SCRIPT_DIR, "logging"), exist_ok=True)

data_dir = os.path.join(SCRIPT_DIR, "data")

log = setup_logger("speedio", "logging/speedio.log")

def Speedio():
    filename="speedio"
    width_ridge=5e-6
    mmi_length=37e-6
    taper_width=width_ridge/2-1.1e-6
    taper_width_in=taper_width
    delta_y=0e-6
    mesh_accuracy=3
    
    T_cross_values=[]
    T_bar_values=[]
    E_lateral_values=[]
    log.info(f"Starting Speedio FDTD \n Length: {mmi_length}, \n width_ridge: {width_ridge}, \n mmi_length:{mmi_length},\n taper_width={taper_width}")


    if os.path.isfile(f"{filename}.fsp"):
        T_cross,T_bar,E_lateral=fdtd_solver(sim=lumapi.FDTD(filename),filename=filename,width_ridge=width_ridge,
            mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,mesh_accuracy=mesh_accuracy,delta_y=delta_y)
        log.info(f"T_cross: {T_cross}, T_bar: {T_bar}, E_lateral:{E_lateral}")


            
    else:
        T_cross,T_bar,E_lateral=fdtd_solver(sim=lumapi.FDTD(),filename=filename,width_ridge=width_ridge,
            mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,mesh_accuracy=mesh_accuracy,delta_y=delta_y)
        log.info(f"T_cross: {T_cross}, T_bar: {T_bar}, E_lateral:{E_lateral}")

    T_cross_values.append(T_cross)
    T_bar_values.append(T_bar)
    E_lateral_values.append(E_lateral)


    np.savez(os.path.join(data_dir, f'speedio_1x2_{int(wavelength*1e9)}nm.npz'),T_cross_values=T_cross_values, T_bar_values=T_bar_values,E_lateral_values=E_lateral_values)


if __name__=="__main__":
    Speedio()