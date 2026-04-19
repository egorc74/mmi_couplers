from variables import *
from geometry import geometry
import matplotlib.pyplot as plt
def bend_FDE(sim,filename,plot=None,run_again=True):
    try:
        log = setup_logger("bend_FDE", "logging/bend_FDE.log")

        if run_again:
            geometry(sim=sim,filename=filename)
            log.info("starting bend_FDE()")
            # define simulation parameters
            # maximum mesh size 40 gives reasonable results
            meshsize      = 20e-9       
            modes         = 20           # modes to output

            # add 2D mode solver (waveguide cross-section)
            sim.addfde()  
            sim.set("solver type", "2D X normal")
            sim.set("x", 0)  
            Zmin = -height_margin  
            Zmax = thick_Si3N4 + height_margin
            sim.set('z max', Zmax)  
            sim.set('z min', Zmin)
            Y_span = 2*width_margin + wg_width 
            Ymin = -Y_span/2  
            Ymax = -Ymin
            sim.set('y',0)  
            sim.set('y span', Y_span)
            sim.set("wavelength", wavelength)   
            sim.set("solver type","2D X normal")
            sim.set("y min bc","PML")
            sim.set("y max bc","PML") # radiation loss
            sim.set("z min bc","metal")
            sim.set("z max bc","metal")  
            sim.set("define y mesh by","maximum mesh step") 
            sim.set("dy", meshsize)
            sim.set("define z mesh by","maximum mesh step") 
            sim.set("dz", meshsize)
            sim.set("number of trial modes",modes)
            sim.cleardcard()

            # solve modes in the waveguide:
            radii = np.array([0,150,100,75,50,25]) * 1e-6

            n=len(radii)
            Neff=np.zeros(n,dtype=complex)
            LossdB_cm=np.zeros(n) 
            LossPerBend=np.zeros(n) 
            power_coupling=np.zeros(n) 
            for i in range(n):
                if (radii[i]==0):
                    sim.setanalysis ('bent waveguide', 0) # Cartesian
                else: 
                    sim.setanalysis ('bent waveguide', 1) # cylindrical 
                    sim.setanalysis ('bend radius', radii[i])
                
                sim.setanalysis ('number of trial modes', modes) 
                nn = sim.findmodes()
                log.info(f"Modes were found for radii: {radii[i]};"
                        f"\n modes:{nn}")

                if (nn>0): 
                    Neff[i] = sim.getdata('FDE::data::mode1','neff')[0] 
                    log.info(f"Neff:{Neff[i]}")
                    LossdB_cm[i] = -sim.getdata('FDE::data::mode1','loss') # per cm
                    log.info(f"LossdB_cm:{LossdB_cm}")
                    ##Loss is in cm --> convert to m
                    LossPerBend[i] = LossdB_cm[i]*1e2 * 2*np.pi*radii[i]/4  #90 degree bend
                    log.info(f"Loss per bend: {LossPerBend}")

                    sim.copydcard('mode1', f'radius{int(radii[i]*1e6)}')
                    log.info("card was copied")
                    # Perform mode-overlap calculations between the straight and bent waveguides 
                    if (radii[i]>0):
                        out = sim.overlap('::radius0',f'::radius{int(radii[i]*1e6)}') 
                        log.info(f"overlap power: {out}")
                        power_coupling[i]=out[1] # power coupling
                        log.info(f"Power coupling from overlap of R=0 and R={radii[i]}: {out[1]}")


                    # plot mode profile:
                    E3=sim.pinch(sim.getelectric('FDE::data::mode1')) 
                    y=sim.getdata('FDE::data::mode1','y') 
                    z=sim.getdata('FDE::data::mode1','z') 
                    sim.image(y,z,E3)
                    sim.exportfigure(f'data/bend_mode_profile_radius{int(radii[i]*1e6)}') 
                    
            PropagationLoss=-3 #dB/cm
            epsilon = 1e-20  
            ##modes coupling power losses
            LossMM=10*np.log10(power_coupling**2 + epsilon) # plot 2X couplings per 90 degree bend vs radius (^2 for two)
            ##Bending loss
            LossR=LossPerBend   # radiational loss 
            ### loss is in db/cm --> convert to db/m
            ## Propagation loss 
            ## Could be negative due to errors in fitting  
            LossP=PropagationLoss*1e2*2*np.pi*radii/4 # quarter turn

            np.savez('data/Bending_loss.npz', radii=radii,LossMM=LossMM, LossR=LossR,LossP=LossP,Loss_T=LossMM + LossR + LossP)
            log.info("Found losses: "
                    f"\n LossMM: {LossMM}"
                    f"\n LossR: {LossR}"
                    f"\n LossP: {LossP}"
                    )
        else:
            log.info("Skipping simulation. Loading existing data from file.")
            data_path="data/Bending_loss.npz"
            if os.path.exists(data_path):
                data = np.load(data_path)
                radii = data['radii']
                LossMM = data['LossMM']
                LossR = data['LossR']
                LossP = data['LossP']
                # Loss_T can be recalculated or loaded
            else:
                log.error(f"Data file {data_path} not found. Cannot plot without data.")
                return
        if plot is not None:
            x = radii[1:] * 1e6

            plt.figure()

            # Mode mismatch loss
            plt.plot(x, LossMM[1:], marker='o', linestyle='-', label='Mode Mismatch Loss')

            # Radiation loss
            plt.plot(x, LossR[1:], marker='o', linestyle='-', label='Radiation loss')
            
            #Propagation loss
            plt.plot(x, LossP[1:], marker='o', linestyle='-', label='Propagation loss')

            # Total loss
            plt.plot(x, LossMM[1:] + LossR[1:] + LossP[1:], marker='o', linestyle='-', label='Total Loss')

            # Log-log scale
       

            # Labels and title
            plt.xlabel("Radius [µm]")
            plt.ylabel("Loss [dB]")
            plt.title("Bend Loss")

            # Grid and legend
            plt.grid(True, which="both", linestyle='--', linewidth=0.5)
            plt.legend()

            plt.tight_layout()
            plt.show()
            
            
            sim.save(filename)

    except Exception as e:
        log.error(e)
if __name__=="__main__":
    filename="bend_calculations"
    import os   
    if os.path.isfile(f"{filename}.lms"):
        sim=lumapi.MODE(filename)
    else:
        sim=lumapi.MODE()

    bend_FDE(sim=sim,filename=filename,plot=1,run_again=False)