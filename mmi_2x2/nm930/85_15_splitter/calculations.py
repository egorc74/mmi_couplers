from pyomo.environ import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Create model
model = ConcreteModel("One-variable optimization")

# Define variable (width)
model.W = Var(bounds=(5, 20), domain=Reals)

# Weight parameter (will be looped over)
model.w = Param(initialize=1.0, mutable=True)

# Constants
wavelength = 1.55
width_min = 5
width_max = 20

# Define helper functions
def f_length(width):
    return 4 * width**2 / 3 / wavelength*3/4

def f_coeff(width):
    return 1/3 - 1.1 / width

# Normalization constants
max_k = max(f_coeff(width_min), f_coeff(width_max))
min_k = min(f_coeff(width_min), f_coeff(width_max))
max_l = max(f_length(width_min), f_length(width_max))
min_l = min(f_length(width_min), f_length(width_max))

# Define normalized expressions for Pyomo
def obj_expression(model):
    norm_length = ((4 * model.W**2 / 3 / wavelength)*3/4 - min_l) / (max_l - min_l)
    norm_coeff  = ((1/3 - 1.1 / model.W) - min_k) / (max_k - min_k)
    # minimize weighted length, maximize coeff (via subtraction)
    return model.w * norm_length - (1 - model.w) * norm_coeff

model.obj = Objective(rule=obj_expression, sense=minimize)

# Prepare lists for results
solutions = []
f_len = []
f_coeffs = []
weights = np.linspace(0, 1, 100)

# Solve for different weights
for w in weights:
    model.w = w
    SolverFactory('ipopt').solve(model, tee=False)
    W_opt = value(model.W)
    solutions.append(W_opt)
    f_len.append(f_length(W_opt))
    f_coeffs.append(f_coeff(W_opt))

# Create dataframe
results = pd.DataFrame({
    'w': weights,
    'W_opt': solutions,
    'Length': f_len,
    'Coeff': f_coeffs
})
target_length = 150
closest_idx = (results['Length'] - target_length).abs().idxmin()

# Get corresponding row
row = results.loc[closest_idx]

print(row)
print (f_length(11))



# Display few results
print(results)

# Plot Pareto-like tradeoff
plt.figure(figsize=(6,5))
plt.plot(f_len, f_coeffs, marker='o', label="Tradeoff curve")
plt.xlabel("Length")
plt.ylabel("Coefficient")
plt.title("Pareto Frontier (Length vs Coefficient)")
plt.legend()
plt.grid(True)
plt.show()
