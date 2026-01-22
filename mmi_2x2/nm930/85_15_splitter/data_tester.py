import numpy as np
data=np.load("data/twist_angle_sweep.npz",allow_pickle=True)
values1=data["E_lateral_values"]
values2=data["T_cross_values"]
values3=data["T_bar_values"]

print(len(values1))
print(len(values2))
print(len(values3))
