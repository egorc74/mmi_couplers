from variables import *
from fdtd_solver import *

def Y_sweep(sim):
    filename="speedio_test"
    wg_length=62e-6
    wg_width=0.4e-6
    width_ridge=11e-6
    mmi_length=478e-6
    taper_width=2.5e-6
    taper_width_in=taper_width

    delta_y=0e-6
    n_core=2.0398
    cladding=0

    Radius=80e-6
    #define ratio
    ratio=85/100
    #define cut angle at the ends of MMI core section
    cut_angle=80   #(degrees)  90==no cut
    mesh_accuracy=3
    
    #define middle section width
    Y_span=np.linspace(0,10,10)*1e-6
    T_cross_values=[]
    T_bar_values=[]
    for y in Y_span:
        if os.path.isfile(f"{filename}.fsp"):
            T_cross,T_bar=fdtd_solver(sim=sim,filename=filename,wg_length=wg_length,Radius=Radius,wg_width=wg_width,width_ridge=width_ridge,
                mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,ratio=ratio,y=y,mesh_accuracy=mesh_accuracy,cut_angle=cut_angle,twist_angle=None)

        else:
            T_cross,T_bar=fdtd_solver(sim=lumapi.FDTD(),Radius=Radius,filename=filename,wg_length=wg_length,wg_width=wg_width,width_ridge=width_ridge,
                mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,ratio=ratio,y=y,mesh_accuracy=mesh_accuracy,cut_angle=cut_angle,twist_angle=None)

        T_cross_values.append(T_cross)
        T_bar_values.append(T_bar)
    np.savez('data/Y_sweep.npz', Y_span=Y_span,T_cross_values=T_cross_values, T_bar_values=T_bar_values)

def Length_sweep(sim):
    filename="speedio_test"
    wg_length=62e-6
    wg_width=0.4e-6
    width_ridge=11e-6
    mmi_length=478e-6
    taper_width=2.5e-6
    taper_width_in=taper_width

    delta_y=0e-6
    n_core=2.0398
    cladding=0

    Radius=80e-6
    #define ratio
    ratio=85/100
    #define middle section width
    #define cut angle at the ends of MMI core section
    cut_angle=80   #(degrees)  90==no cut
    mesh_accuracy=3
    y=5e-6
    
    Lengths=np.linspace(mmi_length-20e-6,mmi_length+20e-6,21)
    T_cross_values=[]
    T_bar_values=[]
    

    for mmi_length in Lengths:
        if os.path.isfile(f"{filename}.fsp"):
            T_cross,T_bar=fdtd_solver(sim=sim,filename=filename,wg_length=wg_length,Radius=Radius,wg_width=wg_width,width_ridge=width_ridge,
                mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,ratio=ratio,y=y,mesh_accuracy=mesh_accuracy,cut_angle=cut_angle,twist_angle=None)

        else:
            T_cross,T_bar=fdtd_solver(sim=lumapi.FDTD(),Radius=Radius,filename=filename,wg_length=wg_length,wg_width=wg_width,width_ridge=width_ridge,
                mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,ratio=ratio,y=y,mesh_accuracy=mesh_accuracy,cut_angle=cut_angle,twist_angle=None)
        T_cross_values.append(T_cross)
        T_bar_values.append(T_bar)
    np.savez('data/Length_sweep.npz', Lengths=Lengths,T_cross_values=T_cross_values, T_bar_values=T_bar_values)



def Width_sweep(sim):
    filename="speedio_test"
    wg_length=62e-6
    wg_width=0.4e-6
    width_ridge=11e-6
    mmi_length=478e-6
    taper_width=2.5e-6
    taper_width_in=taper_width
    delta_y=0e-6
    n_core=2.0398
    cladding=0

    Radius=80e-6
    #define ratio
    ratio=85/100
    #define middle section width
    #define cut angle at the ends of MMI core section
    cut_angle=80   #(degrees)  90==no cut
    mesh_accuracy=3
    y=5e-6
    
    Widths=np.linspace(width_ridge-0.5e-6,width_ridge+0.5e-6,11)
    T_cross_values=[]
    T_bar_values=[]
    

    for width_ridge in Widths:
        if os.path.isfile(f"{filename}.fsp"):
            T_cross,T_bar=fdtd_solver(sim=sim,filename=filename,wg_length=wg_length,Radius=Radius,wg_width=wg_width,width_ridge=width_ridge,
                mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,ratio=ratio,y=y,mesh_accuracy=mesh_accuracy,cut_angle=cut_angle,twist_angle=None)

        else:
            T_cross,T_bar=fdtd_solver(sim=lumapi.FDTD(),Radius=Radius,filename=filename,wg_length=wg_length,wg_width=wg_width,width_ridge=width_ridge,
                mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,ratio=ratio,y=y,mesh_accuracy=mesh_accuracy,cut_angle=cut_angle,twist_angle=None)
        T_cross_values.append(T_cross)
        T_bar_values.append(T_bar)
    np.savez('data/Width_sweep.npz', Widths=Widths,T_cross_values=T_cross_values, T_bar_values=T_bar_values)



def Twist_angle_sweep(sim):
    filename="speedio_test"
    wg_length=62e-6
    wg_width=0.4e-6
    width_ridge=11e-6
    mmi_length=478e-6
    taper_width=2.5e-6
    taper_width_in=taper_width
    delta_y=0e-6
    n_core=2.0398
    cladding=0

    Radius=80e-6
    #define ratio
    ratio=85/100
    #define middle section width
    #define cut angle at the ends of MMI core section
    cut_angle=80   #(degrees)  90==no cut
    mesh_accuracy=3
    y=5e-6
    

    #First calculate twist angle

    d_phase=2*np.arccos(np.sqrt(ratio)) #phase calculation
    S=width_ridge/3

    # Calculate neff of launching mode
    N_eff=1.76  #Neff of 1st order(average), if W=W_taper
    k_0=2*np.pi/wavelength*N_eff
    twist_angle=np.arctan(d_phase/(2*S*k_0))    #use n_eff
    print(twist_angle)




    Twist_angles=np.linspace(twist_angle-0.0005,twist_angle+0.0005,11)
    print(Twist_angles)
    T_cross_values=[]
    T_bar_values=[]
    

    for twist_angle in Twist_angles:
        if os.path.isfile(f"{filename}.fsp"):
            T_cross,T_bar=fdtd_solver(sim=sim,filename=filename,wg_length=wg_length,Radius=Radius,wg_width=wg_width,width_ridge=width_ridge,
                mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,ratio=ratio,y=y,mesh_accuracy=mesh_accuracy,cut_angle=cut_angle,twist_angle=twist_angle)

        else:
            T_cross,T_bar=fdtd_solver(sim=lumapi.FDTD(),Radius=Radius,filename=filename,wg_length=wg_length,wg_width=wg_width,width_ridge=width_ridge,
                mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,ratio=ratio,y=y,mesh_accuracy=mesh_accuracy,cut_angle=cut_angle,twist_angle=twist_angle)
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