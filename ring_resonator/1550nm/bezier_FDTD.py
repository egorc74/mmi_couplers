from variables import *
def radial_fdtd(sim,radii):
    
    sim.addfdtd();
    sim.set('x min', Xmin);
    sim.set('x max', Xmax);
    sim.set('y min', Ymin); 
    sim.set('y max', Ymax);

    sim.set('z min', Zmin);  sim.sim.set('z max', Zmax);
    sim.set('mesh accuracy', Mesh_level);

    sim.addmode;
    sim.set('injection axis', 'y-axis');
    sim.set('direction', 'forward');
    sim.set('y', Ymin+100e-9); 
    sim.set('x', 0); sim.set('x span', width_ridge+width_margin);
    sim.set('z min', Zmin); sim.set('z max', Zmax);
    sim.set('sim.set wavelength',1);
    sim.set('wavelength start', wavelength); 
    sim.set('wavelength stop',wavelength); 
    sim.set('mode selection', Mode_Selection);
    sim.updatesourcemode; 

    sim.adddft()
    sim.set('name', 'transmission');
    sim.set('monitor type', '2D X-normal');
    sim.set('y', length_input+bend_radius); 
    sim.set('y span', width_ridge +width_margin);
    sim.set('z min', Zmin); sim.set('z max', Zmax);
    sim.set('x', Xmax-0.5e-6);

    sim.addmodeexpansion()
    sim.set('name', 'expansion');
    sim.set('monitor type', '2D X-normal');
    sim.set('y', length_input+bend_radius); 
    sim.set('y span', width_ridge +width_margin);
    sim.set('z min', Zmin); sim.set('z max', Zmax);
    sim.set('x', Xmax-0.3e-6);
    sim.set('frequency points',10);
    sim.set('mode selection', Mode_Selection);
    sim.setexpansion('T','transmission');

    sim.adddft()
    sim.set('name', 'input');
    sim.set('monitor type', '2D Y-normal');
    sim.set('y', Ymin+500e-9);  sim.set('x', 0);
    sim.set('x span', width_ridge+width_margin);
    sim.set('z min', Zmin);  sim.set('z max', Zmax);


    