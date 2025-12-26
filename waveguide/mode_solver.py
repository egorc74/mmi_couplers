from variables import *
from geometry import geometry
def mode_solver(sim,filename,width_ridge):
    geometry(sim=sim,filename=filename,width_ridge=width_ridge)
    meshsize=0.02e-6
    sim.addfde()
    sim.set("solver type","2D X normal")
    sim.set("x",0)
    sim.set("y",0)
    sim.set("y span",width_ridge+4e-6)
    sim.set("z",0)
    sim.set("z span",thick_Si3N4+3e-6)
    sim.set("wavelength",wavelength)
    
    sim.set("solver type","2D X normal")
    sim.set("define y mesh by","maximum mesh step") 
    sim.set("dy",meshsize)
    sim.set("define z mesh by","maximum mesh step") 
    sim.set("dz",meshsize)
    sim.set("number of trial modes",20)
    sim.cleardcard()
    n=sim.findmodes()
    for n in range(20):
        Neff = np.real(sim.getdata(f'FDE::data::mode{n+1}','neff')[0]) 
        mode_polarization=sim.getdata(f'FDE::data::mode{n+1}','TE polarization fraction')
        # select first TE mode
        if Neff[0]>1.43:
            print(f"Effective index of first TE launching mode{Neff} with width ridge={width_ridge} and polarization = {mode_polarization}")
        
    sim.save(filename)

if __name__=="__main__":
    filename="waveguide_width"
    widths=np.linspace(1.6e-6,2.5e-6,10)
    for w in widths:
        mode_solver(sim=lumapi.MODE(filename),filename=filename,width_ridge=w)