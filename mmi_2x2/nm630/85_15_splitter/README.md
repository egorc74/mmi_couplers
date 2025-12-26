1)for fdtd simulation:
    a)  python fdtd_solver.py  
    b)  open mmi_2x2_fdtd.fsp
    c)  click run

    Change variables to change geometry in fdtd_solver.py:
    y <- bottom length of middle section 
    cut_angle <- cut angle at the end of mmi core section (90 deg for no cut)
    ratio <- power ratio between two outputs  

2)geometry:
    Geometry is defined in geometry.py where phase shift and angle of twist are calculated for the required output ratio

3)mode_solver:
    Calculates neff of launched mode using MODE solver and waveguide with same width as taper width. The neff is parsed into geometry script so the angle of twist can be calculated   

