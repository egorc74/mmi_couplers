import numpy as np
import matplotlib.pyplot as plt
from variables import *
import h5py
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re

def find_deviation_from_max(transmission_matrix, uu, length_point, maximum, span):
    log = setup_logger("evaluation", "logging/evaluation.log")
    """
    Translate MATLAB function [deviation, xx, yy, x_local, y_local] = find_deviation_from_max(...)

    Parameters
    ----------
    data : object with attribute `transmission_matrix`
           Shape expected: (sweeps, num_points, 2), where [:,:,0] = x, [:,:,1] = y.
    uu : int
         Sweep index.
    length_point : int
         Index of central length (0 means auto-select at max(y)).
    maximum : float
         Reference maximum transmission value.
    span : float
         Half-span for integration window.

    Returns
    -------
    deviation : float
    xx, yy : arrays
        Smoothed polynomial curve fit (x, y).
    x_local, y_local : arrays
        Local window of raw data used for fitting.
    """

    # Extract x and y
    x = transmission_matrix[uu, :, 0]
    y = transmission_matrix[uu, :, 1]
    log.info(f"in find_deviation_from_matrix() with shape {x.shape}"
                 f"and y with shape {y.shape}")


    if y.size == 0:
        raise ValueError("Vector y is empty, cannot find maximum.")

    # Step 1: Find max in raw data if length_point is undefined
    if length_point == 0:
        length_point = int(np.argmax(y))

    # Step 2: Window around length_point
    window = 10
    idx_start = max(0, length_point - window)
    idx_stop = min(len(x), length_point + window + 1)
    idx_range = np.arange(idx_start, idx_stop)

    x_local = x[idx_range]
    y_local = y[idx_range]

    # Step 3: Fit polynomial
    degree = 6
    p = np.polyfit(x_local, y_local, degree)

    # Step 4: Smooth fit curve (evaluate with high precision)
    xx = np.linspace(np.min(x_local), np.max(x_local), 200)
    yy = np.polyval(p, xx)

    # Step 5: Central x and y
    x_central = x[length_point]

    # Step 6: Integrate around central
    x1 = x_central - span
    x2 = x_central + span

    # Antiderivative
    P_int = np.polyint(p)

    # Definite integral
    int_p = np.polyval(P_int, x2) - np.polyval(P_int, x1)

    # Deviation
    deviation = maximum - int_p / (span * 2)
    log.info(f"for index {uu} deviation was found {deviation}")

    return deviation, xx, yy, x_local, y_local





# ============================
# Load data
# ============================



def core_evaluation(transmission_matrix,width_span,taper_width,plot=None):
    try:
        log = setup_logger("evaluation", "logging/evaluation.log")
        data = transmission_matrix
        log.info(f"starting core_evaluation with transmision matrix shape{transmission_matrix[:3]} "
                    f"and width span: {width_span}")


        output_delta = 0
        span = 0.5  # span of manufacturing deviations for length (um)

        # Convert lengths to µm and round
        data[:, :, 0] = np.round(data[:, :, 0] * 1e6, 1)
        log.info(f"converting lengths {data.shape} ")
        

        # ============================
        # Changing width with changing length
        # ============================

        # Step 1: define constants
        mmi_core_width = np.round(width_span * 1e6, decimals=1) 
        delta_step = 0.1   # width deviation step
        delta_width = 0.5  # span of manufacturing deviations for width (um)

        deviation_width_matrix = np.zeros((len(mmi_core_width), 1))
        max_transmission_matrix = np.zeros((len(mmi_core_width), 1))

        # Step 2: for loop for each width in mmi_core_width
        for aa in range(len(mmi_core_width)):
            # Extract data for this width
            x = data[aa, :, 0]   # lengths
            y = data[aa, :, 1]   # transmissions

            # Step 2.1: For current width find optimal length
            idx_max = np.argmax(y)
            maximum_transmission = y[idx_max]

            max_transmission_matrix[aa, 0] = maximum_transmission
            length_point = idx_max
            central_width = mmi_core_width[aa]
           

            # Step 2.2: Make a +-delta_width width span for the current width
            min_w = max(central_width - delta_width, mmi_core_width[0])
            max_w = min(central_width + delta_width, mmi_core_width[-1])
       
            number_of_p = int(np.ceil(1 + (max_w - min_w) / 0.1))
            delta_width_span = np.round(np.linspace(min_w, max_w, number_of_p), 1)
            # Step 2.3: For every width in the span calculate deviation
            total = 0
            missing_points = int(delta_width * 10 * 2 + 1 - len(delta_width_span))
           
            for ll in range(len(delta_width_span)):
                indices = np.where(np.isclose(mmi_core_width, delta_width_span[ll]))[0]
                if indices.size > 0:
                    indx = indices[0]
                else:
                    log.error(f"No index match for {delta_width_span[ll]}")
                dev, _, _, _, _ = find_deviation_from_max(
                    data, indx, length_point, maximum_transmission, span
                )

                if indx == aa:  # save central deviation
                    central_v = dev

                # Edge conditions
                if missing_points != 0 and aa < 10 and ll > len(delta_width_span) - missing_points - 1:
                    total += 2 * dev
                elif missing_points != 0 and aa > len(mmi_core_width) - 10 and ll < missing_points:
                    total += 2 * dev
                else:
                    total += dev

            # find average of sum
            average = total / (number_of_p + missing_points)
            deviation_width_matrix[aa, 0] = average

        optimal_curve=max_transmission_matrix - deviation_width_matrix
        log.info(f"found optimal curve for core_evaluation {optimal_curve}")

        # ============================
        # Plot results
        # ============================
        if plot!=None:
                    
            # Create subplot with secondary y-axis
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            # Scatter (points) for deviation
            fig.add_trace(
                go.Scatter(x=mmi_core_width, y=deviation_width_matrix[:,0],
                        mode="markers", name="Deviation"),
                secondary_y=False,
            )

            # Line for transmission
            fig.add_trace(
                go.Scatter(x=mmi_core_width, y=max_transmission_matrix[:,0],
                        mode="lines", name="Transmission", line=dict(color="red")),
                secondary_y=True,
            )

            # Dashed line for transmission - deviation
            fig.add_trace(
                go.Scatter(x=mmi_core_width, y=optimal_curve[:,0],
                        mode="lines", name="Transmission - Deviation",
                        line=dict(color="green", dash="dash")),
                secondary_y=True,
            )

            # Set axis labels
            fig.update_xaxes(title_text="MMI width (µm)")
            fig.update_yaxes(title_text="Deviation", secondary_y=False)
            fig.update_yaxes(title_text="Transmission", secondary_y=True)

            # Add title
            fig.update_layout(
                title=f"Deviation from desired transmission for {wavelength}nm. "
                    f"Taper width {taper_width:.1f}, +- (Weff/4 + {output_delta:.1f} µm) "
                    f"output location, +- {delta_width:.1f} deviation",
                legend=dict(x=0.02, y=0.98),
                hovermode="x unified"
            )

            fig.show()
        return optimal_curve
    except Exception as e:
        log.error(f"in core _evaluation() error occured {e}")

def colormap_evaluation(transmission_matrix,colormap_taper_span,colormap_width_span,plot=None):
    try:
        # ---------------------------
        # Example data setup
        # ---------------------------
        # Replace this with your actual data loading
        # e.g. data = scipy.io.loadmat("file.mat")
        # Define axes
        x = colormap_taper_span
        y= colormap_width_span   # y-axis
    
        log = setup_logger("evaluation", "evaluation.log")

        log.info(f"starting colormap_evaluation() with transmision matrix shape{transmission_matrix.shape} "
                    f", colormap_taper_span: {colormap_taper_span[:3]} ... {colormap_taper_span[-3:]}"
                    f", colormap_width_span: {colormap_width_span[:3]} ... {colormap_width_span[-3:]}")


        # Compute deviation matrix
        deviation_taper_width_matrix = np.zeros((len(y), 2))
        ##first collumn taper   second collumn width ridge. for every taper calculate its t at [ii,5] 
        
        for ii in range(len(x)):
            max_val = transmission_matrix[ii, 5]   # MATLAB's Z(ii,6) → Python is 0-based
            avg_all = np.mean(max_val - transmission_matrix[ii, :])
            deviation_taper_width_matrix[ii, 0] = max_val - avg_all
            deviation_taper_width_matrix[ii, 1] = avg_all
        col = deviation_taper_width_matrix[:,0]
        log.info(f"found optimal curve (first 3...last 3) {col[:3]} ... {col[-3:]}")
        # ---------------------------
        # Plot heatmap (color-coded map)
        # ---------------------------
        if plot!=None:
            fig1 = px.imshow(
                transmission_matrix,
                x=y,   # horizontal axis
                y=x,   # vertical axis
                origin="lower",
                aspect="auto",
                color_continuous_scale="jet",
                labels={"x": "W mmi", "y": "W taper", "color": "Transmission"},
                title=f"Color-coded map of Transmission (x,y) for wavelength:{wavelength},"
                f"Taper:{np.round(x[5]*1e6,1)} and width ridge: {np.round(y[5]*1e6,1)}"
            )
            fig1.show()
            # ---------------------------
            # Comparison plot
            # ---------------------------
            fig2 = make_subplots(specs=[[{"secondary_y": True}]])

            # Taper width deviation (left axis)
            fig2.add_trace(
                go.Scatter(
                    x=x, y=deviation_taper_width_matrix[:, 1],
                    mode="lines+markers", name="Deviation"
                ),
                secondary_y=False,
            )

            # Transmission column 6 (right axis)
            fig2.add_trace(
                go.Scatter(
                    x=x, y=transmission_matrix[:, 5],
                    mode="lines", line=dict(color="red"),
                    name="Maximum Transmission"
                ),
                secondary_y=True,
            )

            # Delta width deviation (right axis)
            fig2.add_trace(
                go.Scatter(
                    x=x, y=deviation_taper_width_matrix[:, 0],
                    mode="lines", line=dict(color="green"),
                    name="Maximum-Deviation"
                ),
                secondary_y=True,
            )

            # Axis labels
            fig2.update_xaxes(title_text="W input (m)")
            fig2.update_yaxes(title_text="Deviation", secondary_y=False)
            fig2.update_yaxes(title_text="Transmission", secondary_y=True)

            # Title & layout
            fig2.update_layout(
                title=f"Comparison of deviation metrics for wavelength:{wavelength},"
                f"Taper:{np.round(x[5]*1e6,1)} and width ridge: {np.round(y[5]*1e6,1)}",
                legend=dict(x=0.02, y=0.98),
                hovermode="x unified"
            )

            fig2.show()
           
        return deviation_taper_width_matrix[:,0]
    except Exception as e:
        log.error(f"in colormap_evaluation() error occured {e}")
if __name__=="__main__":
    filename="mmi_simulations_1x2"
 
    # transmission_matrix = np.load("core_sweep_from_5756nm_to_7642nm_with_taper_2000nm.npy", allow_pickle=True)
    # mmi_width_span=np.linspace(5.8,7.6,19)*1e-6

    # optimal_curve=core_evaluation(transmission_matrix=transmission_matrix,width_span=mmi_width_span,plot=1)
    

    # data_filename="core_sweep_from_6900nm_to_9428nm_with_taper_2500nm.npy"
    # transmission_matrix = np.load(data_filename, allow_pickle=True)
    
    # match = re.search(r"taper_(\d+)nm", data_filename)
    # if match:
    #     taper_width_val = float(match.group(1))
    #     print(taper_width_val)  # 2500.0


    # trimmed=transmission_matrix[:-8]
    # mmi_width_span=np.linspace(6.9,8.6,18)*1e-6

    # optimal_curve=core_evaluation(transmission_matrix=transmission_matrix,width_span=mmi_width_span,taper_width=taper_width_val,plot=1)
    
    




    data_filename="data/taper_width_colormap_3500_9500nm.npy"
    transmission_matrix = np.load(data_filename, allow_pickle=True)
    

    width_span=np.linspace(9,10,11)*1e-6
    taper_span=np.linspace(3,4,11)*1e-6
    colormap_evaluation(transmission_matrix=transmission_matrix,colormap_taper_span=taper_span,colormap_width_span=width_span,plot=1)
    
