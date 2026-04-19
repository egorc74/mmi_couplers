from variables import *
from geometry import geometry
import matplotlib.pyplot as plt
def mode_solver(sim,filename,width_ridge):


    geometry(sim=sim,filename=filename,width_ridge=width_ridge)
    meshsize=0.02e-6
    sim.addfde()
    sim.set("solver type","2D X normal")
    sim.set("x",0)
    sim.set("y",0)
    sim.set("y span",width_ridge+2e-6)
        
    sim.set("z max",1.3e-6)
    sim.set("z min",-2e-6)

    sim.set("wavelength",wavelength)
    sim.set("solver type","2D X normal")
    sim.set("define y mesh by","maximum mesh step") 
    sim.set("dy",meshsize)    
    sim.set("define z mesh by","maximum mesh step") 
    sim.set("dz",meshsize)
    sim.set("z min bc","PML")
    sim.set("z max bc","PML")


    sim.set("number of trial modes",20)
    sim.set("search","in range")
    sim.set("n1","1.7")
    sim.set("n2","1.3")
    
    sim.cleardcard()
    n=sim.findmodes()
    print(n)
    Neffs=[]
    for n in range(int(n)):
        Neff = np.real(sim.getdata(f'FDE::data::mode{n+1}','neff')[0]) 
        mode_polarization=sim.getdata(f'FDE::data::mode{n+1}','TE polarization fraction')
        # select first TE mode
        if mode_polarization>0.5:  
            Neffs.append(Neff[0])
            print(f"Effective index of first TE launching mode{Neff} with width ridge={width_ridge} and polarization = {mode_polarization}")
    sim.save(filename)
    return Neffs

def width_sweep(sim, widths, filename,plot=False):
    results = {
        "widths": widths,
        "mode_1": [],
        "mode_2": [],
        "mode_3": [],
        "mode_4": [],
        
    }


    for width in widths:
        # Assuming mode_solver returns a list of Neff values
        neffs = mode_solver(sim=sim,filename=filename, width_ridge=width)
        
        # Capture the first mode if it exists, else None or 0
        m1 = neffs[0] if len(neffs) > 0 else 0
        results["mode_1"].append(m1)
        
        # Capture the second mode safely using length check
        m2 = neffs[1] if len(neffs) > 1 else 0
        results["mode_2"].append(m2)

        m3 = neffs[2] if len(neffs) > 2 else 0
        results["mode_3"].append(m3)
        
        # Capture the second mode safely using length check
        m4 = neffs[3] if len(neffs) > 3 else 0
        results["mode_4"].append(m4)
    
    if plot:
        plt.figure(figsize=(8, 6))
        
        # Plot Mode 1 - using .real to ensure we plot magnitude/real index
        plt.plot(widths * 1e6, np.real(results["mode_1"]), 
                 'o-', label='Fundamental Mode (TE00)', markersize=4)
        
        # Plot Mode 2
        plt.plot(widths * 1e6, np.real(results["mode_2"]), 
                 's--', label='First Order Mode (TE01)', markersize=4)
    
        # Plot Mode 3
        plt.plot(widths * 1e6, np.real(results["mode_3"]), 
                 's--', label='First Order Mode (TE02)', markersize=4)

        # Plot Mode 4
        plt.plot(widths * 1e6, np.real(results["mode_4"]), 
                 's--', label='First Order Mode (TE03)', markersize=4)


        # Formatting
        plt.xlabel("Waveguide Width [µm]")
        plt.ylabel("Effective Index ($n_{eff}$)")
        plt.title("Width Sweep: Mode Dispersion")
        plt.grid(True, which="both", linestyle=':', alpha=0.7)
        plt.legend()
        
        # Adjust layout and show
        plt.tight_layout()
        plt.show()
    return results




if __name__=="__main__":
    widths=np.linspace(1.5,3,16)*1e-6
    width_sweep(sim=lumapi.MODE(filename),filename=filename,widths=widths,plot=True)