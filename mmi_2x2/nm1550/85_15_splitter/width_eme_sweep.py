from variables import *
from  eme_solver import eme_solver_prep
import matplotlib.pyplot as plt


def evaluate(filepath):
    data = np.load(filepath)

    Span = data["Span"]

    # --- Two data sets ---
    T_cross_1 = data["T_cross_values"][0:11]
    T_bar_1   = data["T_bar_values"][0:11]

    T_cross_2 = data["T_cross_values"][11:22]
    T_bar_2   = data["T_bar_values"][11:22]

    # --- Ratios ---
    ratio_1 = T_bar_1 / T_cross_1
    ratio_2 = T_bar_2 / T_cross_2

    # --- Target ratio ---
    ratio_85_15 = 15 / 85
    target_ratio = np.ones_like(Span[:11]) * ratio_85_15

    # --- Metrics function ---
    def compute_metrics(T_cross, ratio, label):
        max_dev = np.max(np.abs((np.max(T_cross) - T_cross))) / np.max(T_cross)
        dev_mean = (np.max(T_cross) - np.mean(T_cross)) / np.max(T_cross)

        max_ratio_dev = np.max(np.abs(ratio - ratio[5])) / ratio[5]

        dev_ratio_mean = np.abs(np.mean(ratio[0:5]) - ratio[5]) / ratio[5]

        print(f"\n--- {label} ---")
        print(f"Max deviation from maximum (%): {max_dev * 100}")
        print(f"Mean deviation from maximum (%): {dev_mean * 100}")
        print(f"Max ratio deviation (%): {max_ratio_dev * 100}")
        print(f"Mean ratio deviation (%): {dev_ratio_mean * 100}")

    compute_metrics(T_cross_1, ratio_1, "Set 1")
    compute_metrics(T_cross_2, ratio_2, "Set 2")

    # =========================
    # Transmission plot
    # =========================
    plt.figure()
    plt.plot(Span[:11], T_cross_1, 'o-', label="T_cross – Set 1")
    plt.plot(Span[:11], T_bar_1,   'o-', label="T_bar – Set 1")
    plt.plot(Span[:11], T_cross_2, 's--', label="T_cross – Set 2")
    plt.plot(Span[:11], T_bar_2,   's--', label="T_bar – Set 2")

    plt.xlabel("MMI width span")
    plt.ylabel("Transmission")
    plt.title("Transmission vs width (EME solver)")
    plt.legend()
    plt.grid(True)
    plt.show()

    # =========================
    # Ratio plot
    # =========================
    plt.figure()
    plt.plot(Span[:11], ratio_1, 'o-', label="Ratio Set 1")
    plt.plot(Span[:11], ratio_2, 's--', label="Ratio Set 2")
    plt.plot(Span[:11], target_ratio, 'k:', label="Target 15/85")

    plt.xlabel("MMI width span")
    plt.ylabel("T_bar / T_cross")
    plt.title("Output ratio vs width (EME solver)")
    plt.legend()
    plt.grid(True)
    plt.show()



def evaluate_one(filename):
    data = np.load(filename)

    Span = data["Span"]

    # --- Two data sets ---
    T_cross_1 = data["T_cross_values"][0:11]
    T_bar_1   = data["T_bar_values"][0:11]

    T_cross_2 = data["T_cross_values"][11:22]
    T_bar_2   = data["T_bar_values"][11:22]

    # --- Ratios ---
    ratio_1 = T_bar_1 / T_cross_1
    ratio_2 = T_bar_2 / T_cross_2

    # --- Target ratio ---
    ratio_85_15 = 15 / 85
    target_ratio = np.ones_like(Span[:11]) * ratio_85_15

    # --- Metrics function ---
    def compute_metrics(T_cross, ratio, label):
        max_dev = np.max(np.abs((np.max(T_cross) - T_cross))) / np.max(T_cross)
        dev_mean = (np.max(T_cross) - np.mean(T_cross)) / np.max(T_cross)

        max_ratio_dev = np.max(np.abs(ratio - ratio[5])) / ratio[5]

        dev_ratio_mean = np.abs(np.mean(ratio[0:5]) - ratio[5]) / ratio[5]

        print(f"\n--- {label} ---")
        print(f"Max deviation from maximum (%): {max_dev * 100}")
        print(f"Mean deviation from maximum (%): {dev_mean * 100}")
        print(f"Max ratio deviation (%): {max_ratio_dev * 100}")
        print(f"Mean ratio deviation (%): {dev_ratio_mean * 100}")

    compute_metrics(T_cross_1, ratio_1, "Set 1")
    compute_metrics(T_cross_2, ratio_2, "Set 2")

    # =========================
    # Transmission plot
    # =========================
    plt.figure()
    plt.plot(Span[:11], T_cross_1, 'o-', label="T_cross – Set 1")
    plt.plot(Span[:11], T_bar_1,   'o-', label="T_bar – Set 1")
    plt.plot(Span[:11], T_cross_2, 's--', label="T_cross – Set 2")
    plt.plot(Span[:11], T_bar_2,   's--', label="T_bar – Set 2")

    plt.xlabel("MMI width span")
    plt.ylabel("Transmission")
    plt.title("Transmission vs width (EME solver)")
    plt.legend()
    plt.grid(True)
    plt.show()

    # =========================
    # Ratio plot
    # =========================
    plt.figure()
    plt.plot(Span[:11], ratio_1, 'o-', label="Ratio Set 1")
    plt.plot(Span[:11], ratio_2, 's--', label="Ratio Set 2")
    plt.plot(Span[:11], target_ratio, 'k:', label="Target 15/85")

    plt.xlabel("MMI width span")
    plt.ylabel("T_bar / T_cross")
    plt.title("Output ratio vs width (EME solver)")
    plt.legend()
    plt.grid(True)
    plt.show()



def evaluate_one(filename):
    data = np.load(filename)

    Span = data["Span"]

    # --- Two data sets ---
    T_cross_1 = data["T_cross_values"][0:11]
    T_bar_1   = data["T_bar_values"][0:11]

    # --- Ratios ---
    ratio_1 = T_bar_1 / T_cross_1

    # --- Target ratio ---
    ratio_50_50 = 85/15
    target_ratio = np.ones_like(Span[:11]) * ratio_50_50

    # --- Metrics function ---
    def compute_metrics(T_cross, ratio, label):
        max_dev = np.max(np.abs((np.max(T_cross) - T_cross))) / np.max(T_cross)
        dev_mean = (np.max(T_cross) - np.mean(T_cross)) / np.max(T_cross)

        max_ratio_dev = np.max(np.abs(ratio - ratio[5])) / ratio[5]

        dev_ratio_mean = np.abs(np.mean(ratio[0:5]) - ratio[5]) / ratio[5]

        print(f"\n--- {label} ---")
        print(f"Max deviation from maximum (%): {max_dev * 100}")
        print(f"Mean deviation from maximum (%): {dev_mean * 100}")
        print(f"Max ratio deviation (%): {max_ratio_dev * 100}")
        print(f"Mean ratio deviation (%): {dev_ratio_mean * 100}")

    compute_metrics(T_cross_1, ratio_1, "Set 1")


    # =========================
    # Transmission plot
    # =========================
    plt.figure()
    plt.plot(Span, T_cross_1, 'o-', label="T_cross – Set 1")
    plt.plot(Span, T_bar_1,   'o-', label="T_bar – Set 1")


    plt.xlabel("MMI width span")
    plt.ylabel("Transmission")
    plt.title("Transmission vs width (EME solver)")
    plt.legend()
    plt.grid(True)
    plt.show()

    # =========================
    # Ratio plot
    # =========================
    plt.figure()
    plt.plot(Span, ratio_1, 'o-', label="Ratio Set 1")
    plt.plot(Span, target_ratio, 'k:', label="Target 50/50")

    plt.xlabel("MMI width span")
    plt.ylabel("T_bar / T_cross")
    plt.title("Output ratio vs width (EME solver)")
    plt.legend()
    plt.grid(True)
    plt.show()




def get_values():
    filename="mmi_simulations_2x2"
    width_ridge=13e-6
    mmi_length=175*3e-6

    taper_width=width_ridge/2-1.1e-6
    taper_width_in=taper_width
    T_cross_values=[]
    T_bar_values=[]
    

    width_span=np.linspace(width_ridge-0.5e-6,width_ridge+0.5e-6,11)
    for width in width_span:
        dist=width_ridge/2-taper_width
        delta_y=dist/2+taper_width/2-width/4
        # delta_y=0        
        sim=lumapi.MODE(filename)
        eme_solver_prep(sim=sim,filename=filename,width_ridge=width,
                        mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,
                            delta_y=delta_y)
            
        start_len = wg_length  # common start length
        stop_len  = wg_length+1e-6  # common stop length
        # configure EME analysis
        sim.setemeanalysis("override wavelength", 1)
        sim.setemeanalysis("wavelength", wavelength)

        sim.setemeanalysis("propagation sweep", 1)
        sim.setemeanalysis("parameter", "group span 1")
        sim.setemeanalysis("start", start_len)
        sim.setemeanalysis("stop", stop_len)
        sim.setemeanalysis("number of points", 2)

        # run propagation sweep tool
        sim.emesweep()

        # get propagation sweep result
        S = sim.getemesweep("S")

        s41 = S['s41']  # should be a numpy array
        s31 = S['s31']  # should be a numpy array
        T_cross_values.append(np.abs(s41[0])**2)
        T_bar_values.append(np.abs(s31[0])**2)


    # taper_width=width_ridge/2-1.1e-6-1.5e-6
    # taper_width_in=taper_width

    # for width in width_span:
    #     dist=width_ridge/2-taper_width
    #     delta_y=dist/2+taper_width/2-width/4
    #     # delta_y=0        
    #     sim=lumapi.MODE(filename)
    #     eme_solver_prep(sim=sim,filename=filename,width_ridge=width,
    #                     mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,
    #                         delta_y=delta_y)
            
    #     start_len = wg_length  # common start length
    #     stop_len  = wg_length+1e-6  # common stop length
    #     # configure EME analysis
    #     sim.setemeanalysis("override wavelength", 1)
    #     sim.setemeanalysis("wavelength", wavelength)

    #     sim.setemeanalysis("propagation sweep", 1)
    #     sim.setemeanalysis("parameter", "group span 1")
    #     sim.setemeanalysis("start", start_len)
    #     sim.setemeanalysis("stop", stop_len)
    #     sim.setemeanalysis("number of points", 2)

    #     # run propagation sweep tool
    #     sim.emesweep()

    #     # get propagation sweep result
    #     S = sim.getemesweep("S")

    #     s41 = S['s41']  # should be a numpy array
    #     s31 = S['s31']  # should be a numpy array
    #     T_cross_values.append(np.abs(s41[0])**2)
    #     T_bar_values.append(np.abs(s31[0])**2)



    print(T_cross_values)
    print(T_bar_values)

    np.savez("data/eme_width_span_13",
        Span=width_span,
        T_cross_values=T_cross_values,
        T_bar_values=T_bar_values
    )

def delta_sweep():
    
    filename="mmi_simulations_2x2"
    width_ridge=11e-6
    mmi_length=126e-6

    taper_width=width_ridge/2-1.1e-6-0.7e-6
    taper_width_in=taper_width
    T_cross_values=[]
    T_bar_values=[]
    

    delta_span=np.linspace(-0.5e-6,0.5e-6,11)
    for delta in delta_span:
        delta_y=delta
        # delta_y=0        
        sim=lumapi.MODE(filename)
        eme_solver_prep(sim=sim,filename=filename,width_ridge=width_ridge,
                        mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,
                            delta_y=delta_y)
            
        start_len = wg_length  # common start length
        stop_len  = wg_length+1e-6  # common stop length
        # configure EME analysis
        sim.setemeanalysis("override wavelength", 1)
        sim.setemeanalysis("wavelength", wavelength)

        sim.setemeanalysis("propagation sweep", 1)
        sim.setemeanalysis("parameter", "group span 1")
        sim.setemeanalysis("start", start_len)
        sim.setemeanalysis("stop", stop_len)
        sim.setemeanalysis("number of points", 2)

        # run propagation sweep tool
        sim.emesweep()

        # get propagation sweep result
        S = sim.getemesweep("S")

        s41 = S['s41']  # should be a numpy array
        s31 = S['s31']  # should be a numpy array
        T_cross_values.append(np.abs(s41[0])**2)
        T_bar_values.append(np.abs(s31[0])**2)


    # taper_width=width_ridge/2-1.1e-6-1e-6
    # taper_width_in=taper_width



    print(T_cross_values)
    print(T_bar_values)

    np.savez("data/eme_delta_span_9",
        Span=delta_span,
        T_cross_values=T_cross_values,
        T_bar_values=T_bar_values
    )








if __name__=="__main__":
    evaluate_one("data/eme_width_span_13.npz")
    # get_values()
    # delta_sweep()
