from variables import *
from fdtd_solver import *

log = setup_logger("speedio", "logging/speedio.log")

def Y_sweep(sim):
    sweep_name="y_sweep"

    filename="speedio_test"
    wg_length=15e-6
    wg_width=1.6e-6
    width_ridge=11e-6
    mmi_length=79*2e-6
    taper_width=2.5e-6
    taper_width_in=taper_width

    delta_y=0e-6
    n_core=1.9963
    cladding=0

    Radius=80e-6
    #define ratio
    ratio=50/100
    #define cut angle at the ends of MMI core section
    cut_angle=80   #(degrees)  90==no cut
    mesh_accuracy=3
    
    #define middle section width
    Y_span=np.linspace(0,10,11)*1e-6
    T_cross_values=[]
    T_bar_values=[]

    log.info(f"Starting Y_sweep \n Y_span: {Y_span}, \n width_ridge: {width_ridge}, \n mmi_length:{mmi_length},\n taper_width={taper_width},\n ratio:{ratio}")

    for y in Y_span:
        if os.path.isfile(f"{filename}.fsp"):
            T_cross,T_bar=fdtd_solver(sim=sim,filename=filename,wg_length=wg_length,Radius=Radius,wg_width=wg_width,width_ridge=width_ridge,
                mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,ratio=ratio,y=y,mesh_accuracy=mesh_accuracy,cut_angle=cut_angle,delta_y=delta_y,twist_angle=None,sweep_name=sweep_name)
            log.info(f"T_cross: {T_cross}, T_bar: {T_bar}")

        else:
            T_cross,T_bar=fdtd_solver(sim=lumapi.FDTD(),Radius=Radius,filename=filename,wg_length=wg_length,wg_width=wg_width,width_ridge=width_ridge,
                mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,ratio=ratio,y=y,mesh_accuracy=mesh_accuracy,cut_angle=cut_angle,delta_y=delta_y,twist_angle=None,sweep_name=sweep_name)
            log.info(f"T_cross: {T_cross}, T_bar: {T_bar}")

        T_cross_values.append(T_cross)
        T_bar_values.append(T_bar)
    np.savez('data/Y_sweep.npz', Y_span=Y_span,T_cross_values=T_cross_values, T_bar_values=T_bar_values)



def Length_sweep(sim):
    sweep_name="length_sweep"
    filename="speedio_test"
    wg_length=15e-6
    wg_width=1.6e-6
    width_ridge=11e-6
    mmi_length=79*2e-6
    taper_width=2.5e-6
    taper_width_in=taper_width

    delta_y=0e-6
    n_core=1.9963
    cladding=0

    Radius=80e-6
    #define ratio
    ratio=50/100
    #define middle section width
    #define cut angle at the ends of MMI core section
    cut_angle=80   #(degrees)  90==no cut
    mesh_accuracy=3
    y=5e-6
    
    Lengths=np.linspace(mmi_length-10e-6,mmi_length+10e-6,21)
    T_cross_values=[]
    T_bar_values=[]
    log.info(f"Starting Length Sweep \n Length_span: {Lengths}, \n width_ridge: {width_ridge}, \n mmi_length:{mmi_length},\n taper_width={taper_width},\n ratio:{ratio}")

    

    for mmi_length in Lengths:
        if os.path.isfile(f"{filename}.fsp"):
            T_cross,T_bar=fdtd_solver(sim=sim,filename=filename,wg_length=wg_length,Radius=Radius,wg_width=wg_width,width_ridge=width_ridge,
                mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,ratio=ratio,y=y,mesh_accuracy=mesh_accuracy,cut_angle=cut_angle,delta_y=delta_y,twist_angle=None,sweep_name=sweep_name)
            log.info(f"T_cross: {T_cross}, T_bar: {T_bar}")
            
        else:
            T_cross,T_bar=fdtd_solver(sim=lumapi.FDTD(),Radius=Radius,filename=filename,wg_length=wg_length,wg_width=wg_width,width_ridge=width_ridge,
                mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,ratio=ratio,y=y,mesh_accuracy=mesh_accuracy,cut_angle=cut_angle,delta_y=delta_y,twist_angle=None,sweep_name=sweep_name)
            log.info(f"T_cross: {T_cross}, T_bar: {T_bar}")

        T_cross_values.append(T_cross)
        T_bar_values.append(T_bar)
    np.savez('data/Length_sweep.npz', Lengths=Lengths,T_cross_values=T_cross_values, T_bar_values=T_bar_values)



def Width_sweep(sim):
    sweep_name="width_sweep"
    filename="speedio_test"
    wg_length=15e-6
    wg_width=1.6e-6
    width_ridge=11e-6
    mmi_length=79*2e-6
    taper_width=2.5e-6
    taper_width_in=taper_width
    delta_y=0e-6
    n_core=1.9963
    cladding=0

    Radius=80e-6
    #define ratio
    ratio=50/100
    #define middle section width
    #define cut angle at the ends of MMI core section
    cut_angle=80   #(degrees)  90==no cut
    mesh_accuracy=3
    y=5e-6
    
    Widths=np.linspace(width_ridge-0.5e-6,width_ridge+0.5e-6,11)
    T_cross_values=[]
    T_bar_values=[]
    log.info(f"Starting Width sweep\n Width_span: {Widths}, \n width_ridge: {width_ridge}, \n mmi_length:{mmi_length},\n taper_width={taper_width},\n ratio:{ratio}")


    for width_ridge in Widths:
        ###move tapers so that the gap is kept as 1.1um
        delta_y=(width_ridge/3-1.1e-6-taper_width)/2
        if os.path.isfile(f"{filename}.fsp"):
            T_cross,T_bar=fdtd_solver(sim=sim,filename=filename,wg_length=wg_length,Radius=Radius,wg_width=wg_width,width_ridge=width_ridge,
                mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,ratio=ratio,y=y,mesh_accuracy=mesh_accuracy,cut_angle=cut_angle,delta_y=delta_y,twist_angle=None,sweep_name=sweep_name)
            log.info(f"T_cross: {T_cross}, T_bar: {T_bar}")

        else:
            T_cross,T_bar=fdtd_solver(sim=lumapi.FDTD(),Radius=Radius,filename=filename,wg_length=wg_length,wg_width=wg_width,width_ridge=width_ridge,
                mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,ratio=ratio,y=y,mesh_accuracy=mesh_accuracy,cut_angle=cut_angle,delta_y=delta_y,twist_angle=None,sweep_name=sweep_name)
            log.info(f"T_cross: {T_cross}, T_bar: {T_bar}")

        T_cross_values.append(T_cross)
        T_bar_values.append(T_bar)
    np.savez('data/Width_sweep.npz', Widths=Widths,T_cross_values=T_cross_values, T_bar_values=T_bar_values)



def Twist_angle_sweep(sim):
    sweep_name="twist_angle_sweep"
    filename="speedio_test"
    wg_length=15e-6
    wg_width=1.6e-6
    width_ridge=11e-6
    mmi_length=79*2e-6
    taper_width=2.5e-6
    taper_width_in=taper_width
    delta_y=0e-6
    n_core=1.9963
    cladding=0

    Radius=80e-6
    #define ratio
    ratio=50/100
    #define middle section width
    #define cut angle at the ends of MMI core section
    cut_angle=80   #(degrees)  90==no cut
    mesh_accuracy=3
    y=5e-6
    

    #First calculate twist angle

    d_phase=2*np.arccos(np.sqrt(ratio)) #phase calculation
    S=width_ridge/3

    # Calculate neff of launching mode
    N_eff=1.580     #Neff of 1st order(average), if W=W_taper
    k_0=2*np.pi/wavelength*N_eff
    twist_angle=np.arctan(d_phase/(2*S*k_0))    #use n_eff




    Twist_angles=np.linspace(twist_angle-0.0005,twist_angle+0.0005,11)
    

    T_cross_values=[]
    T_bar_values=[]
    
    log.info(f"Starting Twist angle sweep \n Twist_angles_span: {Twist_angles}, \n width_ridge: {width_ridge}, \n mmi_length:{mmi_length},\n taper_width={taper_width},\n ratio:{ratio}")

    for twist_angle in Twist_angles:
        if os.path.isfile(f"{filename}.fsp"):
            T_cross,T_bar=fdtd_solver(sim=sim,filename=filename,wg_length=wg_length,Radius=Radius,wg_width=wg_width,width_ridge=width_ridge,
                mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,ratio=ratio,y=y,mesh_accuracy=mesh_accuracy,cut_angle=cut_angle,twist_angle=twist_angle,delta_y=delta_y,sweep_name=sweep_name)
            log.info(f"T_cross: {T_cross}, T_bar: {T_bar}")

        else:
            T_cross,T_bar=fdtd_solver(sim=lumapi.FDTD(),Radius=Radius,filename=filename,wg_length=wg_length,wg_width=wg_width,width_ridge=width_ridge,
                mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,ratio=ratio,y=y,mesh_accuracy=mesh_accuracy,cut_angle=cut_angle,twist_angle=twist_angle,delta_y=delta_y,sweep_name=sweep_name)
            log.info(f"T_cross: {T_cross}, T_bar: {T_bar}")

        T_cross_values.append(T_cross)
        T_bar_values.append(T_bar)
    np.savez('data/Twist_angle_sweep.npz', Twist_angles=Twist_angles,T_cross_values=T_cross_values, T_bar_values=T_bar_values)




if __name__ =="__main__":
    filename="speedio_test"
    if os.path.isfile(f"{filename}.fsp"):
        # Y_sweep(sim=lumapi.FDTD(filename))
        # Length_sweep(sim=lumapi.FDTD(filename))
        # Width_sweep(sim=lumapi.FDTD(filename))
        # Twist_angle_sweep(sim=lumapi.FDTD())

        pass
    else:
        # Y_sweep(sim=lumapi.FDTD())
        # Length_sweep(sim=lumapi.FDTD())
        # Width_sweep(sim=lumapi.FDTD())
        # Twist_angle_sweep(sim=lumapi.FDTD())
        pass