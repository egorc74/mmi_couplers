from variables import *
from double_wg_geometry import double_wg_geometry
import matplotlib.pyplot as plt
def mode_solver(sim,filename,gap):

    double_wg_geometry(sim=sim,filename=filename,gap=gap)
    meshsize=0.02e-6
    sim.addfde()
    sim.set("solver type","2D X normal")
    sim.set("x",0)
    sim.set("y",0)
    sim.set("y span",gap+4e-6+wg_width*2)
        
    sim.set("z max",1.3e-6)
    sim.set("z min",-1.3e-6)

    sim.set("wavelength",wavelength)
    sim.set("solver type","2D X normal")
    sim.set("define y mesh by","maximum mesh step") 
    sim.set("dy",meshsize)    
    sim.set("define z mesh by","maximum mesh step") 
    sim.set("dz",meshsize)
    sim.set("z min bc","metal")
    sim.set("z max bc","metal")


    sim.set("number of trial modes",20)
    sim.set("search","in range")
    sim.set("n1","1.7")
    sim.set("n2","1.3")
    sim.cleardcard()
    n=sim.findmodes()
    
    print(n)
    Neffs=[]
    for n in range(2):
        Neff = np.real(sim.getdata(f'FDE::data::mode{n+1}','neff')[0]) 
        mode_polarization=sim.getdata(f'FDE::data::mode{n+1}','TE polarization fraction')
        # select first two TE modes
        Neffs.append(Neff[0])
    sim.save(filename)
    neff_dif=np.abs(Neffs[0]-Neffs[1])
    allowed_coupling=1e-6*100
    length=730e-6*2
    p_out=np.sin(np.pi * length * neff_dif / wavelength)**2
    print(p_out)
    
    req_length=wavelength/(np.pi * neff_dif) * np.arcsin(np.sqrt(allowed_coupling))
    print(f"length required for 1e-6 coupling: {req_length*1e3}mm with the gap: {gap*1e6} um")

    input("Press enter to close the program")

    # return neff_dif

def eme_solver(sim,filename,gap):
    double_wg_geometry(sim=sim,filename=filename,gap=gap)
    sim.addeme()
    sim.set("solver type","3D: X Prop")
    center_z_offset=thick_Si3N4
    sim.set("wavelength",wavelength)
    sim.set("index",1)
    Zmin=-1.3e-6
    Zmax=1.3e-6
    Xmin=-10e-6
    Xmax=10e-6

    sim.set("z min",Zmin)
    sim.set("z max", Zmax)
    sim.set("y",0)         
    sim.set("y span",wg_width*2+4e-6+gap)
    sim.set("x min",Xmin)
    sim.set("number of cell groups",1)
    sim.set("display cells",1)
    sim.set("number of modes for all cell groups",20)
    sim.set("number of periodic groups",1)
    sim.set("energy conservation","make passive")
    sim.set("cells",np.array([1]))
    sim.set("group spans",np.array([Xmax-Xmin]))
    sim.set("y min bc","Metal")
    sim.set("z min bc","Metal")
    sim.set("y max bc","Metal")
    sim.set("z max bc","metal")


    sim.setnamed("EME::Ports::port_1","y",(-wg_width/2-gap/2))
    sim.setnamed("EME::Ports::port_1","y span",(wg_width+2e-6))
    sim.setnamed("EME::Ports::port_1","z min",Zmin)
    sim.setnamed("EME::Ports::port_1","z max",Zmax)
    sim.setnamed("EME::Ports::port_1","mode selection","fundamental TE mode")
    sim.setnamed("EME::Ports::port_1","use full simulation span",0)


    sim.setnamed("EME::Ports::port_2","y",(-wg_width/2-gap/2)*(-1))
    sim.setnamed("EME::Ports::port_2","y span",(wg_width+2e-6))
    sim.setnamed("EME::Ports::port_2","z min",Zmin)
    sim.setnamed("EME::Ports::port_2","z max",Zmax)
    sim.setnamed("EME::Ports::port_2","mode selection","fundamental TE mode")
    sim.setnamed("EME::Ports::port_2","use full simulation span",0)


    input("Press enter to close the program")
    

if __name__=="__main__":
    widths=np.linspace(1.5,3,16)*1e-6
    # width_sweep(sim=lumapi.MODE(filename),filename=filename,widths=widths,plot=True)
    gap=3e-6
    sim=lumapi.MODE()
    filename="coupling_mode"
    # mode_solver(sim=sim,filename=filename,gap=gap)
    eme_solver(gap=gap,filename=filename,sim=sim)