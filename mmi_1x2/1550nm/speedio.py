from variables import *
from fdtd_solver import *

log = setup_logger("speedio", "logging/speedio.log")



def Length_sweep(sim):
    sweep_name="length_sweep"
    filename="speedio_test"
    wg_length=20e-6
    wg_width=1.6e-6
    width_ridge=9.5e-6
    mmi_length=47e-6
    taper_width=3.6e-6
    taper_width_in=taper_width

    delta_y=0e-6
    n_core=1.9963
    cladding=0

    mesh_accuracy=3
    
    Lengths=np.linspace(mmi_length-5e-6,mmi_length+5e-6,11)
    T_cross_values=[]
    T_bar_values=[]
    log.info(f"Starting Length Sweep \n Length_span: {Lengths}, \n width_ridge: {width_ridge}, \n mmi_length:{mmi_length},\n taper_width={taper_width}")

    for mmi_length in Lengths:
        if os.path.isfile(f"{filename}.fsp"):
            T_cross,T_bar=fdtd_solver(sim=lumapi.FDTD(filename),filename=filename,width_ridge=width_ridge,
             mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,mesh_accuracy=mesh_accuracy,delta_y=delta_y,sweep_name=sweep_name)
            log.info(f"T_cross: {T_cross}, T_bar: {T_bar}")


            
        else:
            T_cross,T_bar=fdtd_solver(sim=lumapi.FDTD(),filename=filename,width_ridge=width_ridge,
             mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,mesh_accuracy=mesh_accuracy,delta_y=delta_y,sweep_name=sweep_name)
            log.info(f"T_cross: {T_cross}, T_bar: {T_bar}")

        T_cross_values.append(T_cross)
        T_bar_values.append(T_bar)
    np.savez('data/Length_sweep.npz', Lengths=Lengths,T_cross_values=T_cross_values, T_bar_values=T_bar_values)



def Width_sweep(sim):
    sweep_name="width_sweep"
    filename="speedio_test"
    wg_length=20e-6
    wg_width=1.6e-6
    width_ridge=9.5e-6
    mmi_length=47e-6
    taper_width=3.6e-6
    taper_width_in=taper_width
    delta_y=0e-6
    n_core=1.9963
    cladding=0


    mesh_accuracy=3
    
    Widths=np.linspace(width_ridge-0.5e-6,width_ridge+0.5e-6,11)
    
    T_cross_values=[]
    T_bar_values=[]
    log.info(f"Starting Width sweep\n Width_span: {Widths}, \n width_ridge: {width_ridge}, \n mmi_length:{mmi_length},\n taper_width={taper_width}")


    for width_ridge in Widths:
        ###move tapers so that the gap is kept as 1.1um
        delta_y=(width_ridge/2-1.1e-6-taper_width)/2
        if os.path.isfile(f"{filename}.fsp"):
            T_cross,T_bar=fdtd_solver(sim=lumapi.FDTD(filename),filename=filename,width_ridge=width_ridge,
             mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,mesh_accuracy=mesh_accuracy,delta_y=delta_y,sweep_name=sweep_name)
            log.info(f"T_cross: {T_cross}, T_bar: {T_bar}")

            
        else:
            T_cross,T_bar=fdtd_solver(sim=lumapi.FDTD(),filename=filename,width_ridge=width_ridge,
             mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,mesh_accuracy=mesh_accuracy,delta_y=delta_y,sweep_name=sweep_name)
            log.info(f"T_cross: {T_cross}, T_bar: {T_bar}")

        T_cross_values.append(T_cross)
        T_bar_values.append(T_bar)
    np.savez('data/Width_sweep.npz', Widths=Widths,T_cross_values=T_cross_values, T_bar_values=T_bar_values)



def Taper_width_sweep(sim):
    sweep_name="taper_width"
    filename="speedio_test"
    wg_length=20e-6
    wg_width=1.6e-6
    width_ridge=9.5e-6
    mmi_length=47e-6
    taper_width=3.6e-6
    taper_width_in=taper_width
    delta_y=0e-6
    n_core=1.9963
    cladding=0


    mesh_accuracy=3
    
    Taper_widths=np.linspace(taper_width-0.5e-6,taper_width+0.5e-6,11)
    T_cross_values=[]
    T_bar_values=[]
    log.info(f"Starting Width sweep\n Width_span: {Taper_widths}, \n width_ridge: {width_ridge}, \n mmi_length:{mmi_length},\n taper_width={taper_width}")


    for taper in Taper_widths:
        ###move tapers so that the gap is kept as 1.1um
        taper_width=taper
        taper_width_in=taper
        if os.path.isfile(f"{filename}.fsp"):
            T_cross,T_bar=fdtd_solver(sim=lumapi.FDTD(filename),filename=filename,width_ridge=width_ridge,
             mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,mesh_accuracy=mesh_accuracy,delta_y=delta_y,sweep_name=sweep_name)
            log.info(f"T_cross: {T_cross}, T_bar: {T_bar}")

            
        else:
            T_cross,T_bar=fdtd_solver(sim=lumapi.FDTD(),filename=filename,width_ridge=width_ridge,
             mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,mesh_accuracy=mesh_accuracy,delta_y=delta_y,sweep_name=sweep_name)
            log.info(f"T_cross: {T_cross}, T_bar: {T_bar}")

        T_cross_values.append(T_cross)
        T_bar_values.append(T_bar)
    np.savez('data/Taper_width_sweep.npz', Taper_widths=Taper_widths,T_cross_values=T_cross_values, T_bar_values=T_bar_values)





if __name__ =="__main__":
    filename="speedio_test"
    if os.path.isfile(f"{filename}.fsp"):
        Width_sweep(sim=lumapi.FDTD(filename))

        pass
    else:
        Width_sweep(sim=lumapi.FDTD())
    
        pass