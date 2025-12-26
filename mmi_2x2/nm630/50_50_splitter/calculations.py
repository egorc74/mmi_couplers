from pyomo.environ import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar
import mplcursors



# Constants
wavelength = 1.55
n_core=1.9963
propagation_loss=0.2  #DB/mm
def calculate_loss(propagation_loss,length):
    loss=10**(-propagation_loss/1000/10*length)
    return 1-loss




#### FIRST MAKE FUNCTION FOR ESTIMATED DEVIATION ####

#numerical invert function (find x for known f(x)) 
def num_invert(f, y, bracket):
    """Return x such that f(x) = y"""
    sol = root_scalar(lambda x: f(x) - y, bracket=bracket)
    return sol.root



# Example usage

def Z(T):
    exp=((4-5*T**2)+ np.sqrt((4-5*T**2)**2-16*T**2*(T**2-1)))/8/T**2
    return np.sqrt(exp)

#for NXN a=1
N=2
M=1
a=1
fabrication_error=0.3
def calculate_Z_for_given_K(K,Width):
    z=fabrication_error*(16*M)/(np.pi*a*N*Width*K**2)
    return z


# Define helper functions
def f_length(width):
    return 4 * n_core*width**2 / 3 / wavelength*3/8

def f_coeff(width):
    return 1/3 - 1.1 / width

def max_width_calculation(max_length):
    max_length=max_length-200
    max_width=np.sqrt(max_length*wavelength/n_core*2)
    return max_width
width_min = 5
length_max=1000
width_max = max_width_calculation(length_max)


# Create model
model = ConcreteModel("One-variable optimization")

# Define variable (width)
model.W = Var(bounds=(width_min, width_max), domain=Reals)

# Weight parameter (will be looped over)
model.w = Param(initialize=1.0, mutable=True)



# Normalization constants
max_k = max(f_coeff(width_min), f_coeff(width_max))
min_k = min(f_coeff(width_min), f_coeff(width_max))
max_l = max(f_length(width_min), f_length(width_max))
min_l = min(f_length(width_min), f_length(width_max))
# Define normalized expressions for Pyomo
def obj_expression(model):
    norm_length = ((4 * model.W**2 * n_core/ 3 / wavelength)*3/8 - min_l) / (max_l - min_l)
    norm_coeff  = ((1/3 - 1.1 / model.W) - min_k) / (max_k - min_k)
    # minimize weighted length, maximize coeff (via subtraction)
    return (1 - model.w)* norm_length - model.w * norm_coeff

model.obj = Objective(rule=obj_expression, sense=minimize)

# Prepare lists for resultss
solutions = []
f_len = []
f_coeffs = []
weights = np.linspace(0, 1, 100)

transmissions=[]

# Solve for different weights
for w in weights:
    model.w = w
    SolverFactory('ipopt').solve(model, tee=False)
    W_opt = value(model.W)
    solutions.append(W_opt)
    Len=f_length(W_opt)
    f_len.append(Len)
    coeff=f_coeff(W_opt)
    f_coeffs.append(coeff)
    #estimate transmission
 
    calculated_Z=calculate_Z_for_given_K(K=coeff,Width=W_opt)
    T=num_invert(Z, calculated_Z , bracket=[0.0001,1])
    loss=calculate_loss(propagation_loss=propagation_loss,length=Len)
    transmissions.append(T-loss)
    



# Create dataframe
results = pd.DataFrame({
    'w': weights,
    'W_opt': solutions,
    'Length': f_len,
    'Coeff': f_coeffs,
    'Transm': transmissions
    
})
target_length = 500
closest_idx = (results['Length'] - target_length).abs().idxmin()

# Get corresponding row
row = results.loc[closest_idx]

print(row)
print (f_length(row["W_opt"]))






plt.figure(figsize=(8, 6))

# First curve: Tradeoff
plt.plot(
    f_len,
    f_coeffs,
    marker='o',
    label="Tradeoff curve (Taper_width/MMI_width) vs Length"
)

# Second curve: Transmission
plt.plot(
    f_len,
    transmissions,
    marker='o',
    label=f"Estimated transmission curve (Transmission with {fabrication_error}µm deviations in width) vs Length"
)

# Labels and title
plt.xlabel("K")
plt.ylabel("W")
plt.title(f"Pareto Frontier (Length vs Coefficient) for wavelength: {wavelength}")
plt.grid(True)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=1)

# --- Enable interactive cursors ---
# 'multiple=True' lets you select multiple data points and keep them visible
cursor = mplcursors.cursor(multiple=True)

# Customize annotation text
@cursor.connect("add")
def on_add(sel):
    x, y = sel.target
    sel.annotation.set_text(f"Length={x:.3f}\nTransmission={y:.3f}")
    sel.annotation.get_bbox_patch().set(fc="white", alpha=0.8)

plt.tight_layout()
plt.show()