import numpy as np
import matplotlib.pyplot as plt
from variables import *

log = setup_logger("speedio", "logging/speedio.log")


def data_analysis(dataset,measurement):
    #Load data
    try:
        data=np.load(f"{dataset}.npz",allow_pickle=True)
        T_cross_values= np.array([d["T"][0] for d in data['T_cross_values']])
        T_bar_values= np.array([d["T"][0] for d in data['T_bar_values']])

        
        if (measurement=="max_transmission"):
            span=data["Span"]
            max_val = T_cross_values.max()
            max_idx = T_cross_values.argmax()
            value=span[max_idx]
            log.info(f"Max transmission {max_val} is obtained at index {max_idx} and value in span {value}")
            return value
        
        if measurement == "optimal_angle":
            span = data["Span"]
            targets = np.array([0.50, 0.50])

            # ---- CROSS ----
            diffs_cross = np.abs(T_cross_values[:, None] - targets)
            diff_cross = diffs_cross.min(axis=1)
            best_idx_cross = np.argmin(diff_cross)
            best_ratio_cross = T_cross_values[best_idx_cross]
            best_diff_cross = diff_cross[best_idx_cross]
            closest_target_cross = targets[np.argmin(diffs_cross[best_idx_cross])]

            # ---- BAR ----
            diffs_bar = np.abs(T_bar_values[:, None] - targets)
            diff_bar = diffs_bar.min(axis=1)
            best_idx_bar = np.argmin(diff_bar)
            best_ratio_bar = T_bar_values[best_idx_bar]
            best_diff_bar = diff_bar[best_idx_bar]
            closest_target_bar = targets[np.argmin(diffs_bar[best_idx_bar])]

            # ---- COMPARE BEST MATCHES ----
            if best_diff_cross < best_diff_bar:
                value = span[best_idx_cross]
                log.info(   f"Closest value was found:"
                            f"CROSS is closer: |T - {closest_target_cross}| = {best_diff_cross}, "
                            f"T = {best_ratio_cross}, span = {value}")
                return value
            else:
                value = span[best_idx_bar]
                log.info(   f"Closest value was found:"
                            f"BAR is closer: |T - {closest_target_bar}| = {best_diff_bar}, "
                            f"T = {best_ratio_bar}, span = {value}"
                )
                return value
    
    except Exception as e:
        log.error(f"An error has occured in data analyser {e} \n returning defauult values")
        return None


def generate_test_data(
    filename,
    n_points=50,
    span_min=155e-6,
    span_max=160e-6,
    cross_target=0.15,
    bar_target=0.85,
    noise=0.02,
    seed=41
):
    """
    Generates synthetic data compatible with data_analysis()

    T_cross_values ~ 0.85
    T_bar_values   ~ 0.15
    """
    if (filename=="data/y_sweep"):
        span_min=0
        span_max=10e-6
    if (filename=="data/lenght_sweep"):
        span_min=153e-6
        span_max=163e-6
    if (filename=="data/twist_angle_sweep"):
        span_min=opt_twist_angle-0.0005
        span_max=opt_twist_angle+0.0005

    rng = np.random.default_rng(seed)

    # Span (e.g. angles)
    Span = np.linspace(span_min, span_max, n_points)

    # Generate noisy values around targets
    T_cross_vals = np.clip(
        cross_target + noise * rng.standard_normal(n_points),
        0, 1
    )
    T_bar_vals = np.clip(
        bar_target + noise * rng.standard_normal(n_points),
        0, 1
    )

    # Wrap values into dict structure expected by your code
    T_cross_values = np.array(
        [{"T": np.array([v])} for v in T_cross_vals],
        dtype=object
    )
    T_bar_values = np.array(
        [{"T": np.array([v])} for v in T_bar_vals],
        dtype=object
    )

    # Save dataset
    np.savez(
        f"{filename}.npz",
        T_cross_values=T_cross_values,
        T_bar_values=T_bar_values,
        Span=Span
    )

         


if __name__=="__main__":
    pass
    