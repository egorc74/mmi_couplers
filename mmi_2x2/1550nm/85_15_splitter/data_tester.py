import numpy as np
data=np.load("data/Twist_angle_sweep.npz",allow_pickle=True)
print(data["E_lateral_values"])