from variables import *
def _calculate_fdtd_dim(radii,theta):
    #Use cosine to calculate x_span (theta is in degrees)
    x_span=np.sqrt(2*radii**2 - 2 * np.cos(theta/180*np.pi) * radii**2)
    print(x_span)
    z=np.sqrt(2*radii**2 - 2 * np.cos(theta/2/180*np.pi) * radii**2)
    y_span=np.sqrt(z**2-(x_span/2)**2)+5e-6
    print(y_span+5e-6)

    return x_span,y_span

def radial_geometry(sim,radii):
    sim.switchtolayout()
    sim.deleteall()


    """Add ring"""
    theta=10 #degrees
    sim.addring()
    sim.set("name",f"radial_bend") 
    sim.set("material",material_Si3N4)
    sim.set("y",0)  
    outer_radius=radii+wg_width/2
    inner_radius=radii-wg_width/2
    sim.set("outer radius",outer_radius)
    sim.set("inner radius",inner_radius)
    sim.set("theta start",0)
    sim.set("theta stop",theta)
    sim.set("z",0)     
    sim.set("z span", thick_Si3N4)
    sim.set("x",0)  
    x_span,y_span=_calculate_fdtd_dim(radii=radii,theta=theta)
    
    """Add fdtd"""
    sim.addfdtd();
    sim.set('x',0);
    sim.set('x span', x_span);
    sim.set('y', 0); 
    sim.set('y span', y_span);

    sim.set('z min', -height_margin); 
    sim.set('z max', height_margin+thick_Si3N4/2);

    """Add wafer and Box"""


    X_span=150e-6
    Y_span = 150e-6



    """Add BOX"""
    sim.addrect()
    sim.set("name", "BOX")
    sim.set("material", material_BOX)
    sim.set("x", X_span/2)
    sim.set("x span", X_span)
    sim.set("z min", -thick_BOX-thick_Si3N4/2)
    sim.set("z max", -thick_Si3N4/2)
    sim.set("y", Y_span/2)
    sim.set("y span", Y_span)
    sim.set("alpha", 0.05)

    """Add Wafer"""
    sim.addrect()
    sim.set("name", "Wafer")
    sim.set("material", material_Si)
    sim.set("x", X_span/2)
    sim.set("x span", X_span)
    sim.set("z max", -thick_BOX-thick_Si3N4/2)
    sim.set("z min", -thick_BOX -thick_Si3N4/2- 2e-6)
    sim.set("y", Y_span/2)
    sim.set("y span", Y_span)
    sim.set("alpha", 0.1)
    input("press enter")

if __name__=="__main__":
    radial_geometry(sim=lumapi.FDTD(),radii=100e-6)
