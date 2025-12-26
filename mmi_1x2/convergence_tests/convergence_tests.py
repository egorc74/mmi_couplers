
import sys
sys.path.append("..")
# from nm1550.fdtd_solver import fdtd_solver
from nm1550.variables import *
from nm1550.fdtd_solver_convergence import fdtd_solver

class Parameter:
    def __init__(self,sim, sweep_name, name, parameter,type,start,stop,units):
        self.sweep_name=sweep_name
        sim.deletesweep(sweep_name)
        sim.addsweep(0)
        sim.setsweep("sweep", "name", f"{sweep_name}")
        sim.setsweep(f"{sweep_name}", "type", "Ranges")
        sim.setsweep(f"{sweep_name}", "number of points", 10);         
        self.Name = name
        self.Parameter = parameter
        self.Type=type
        self.Start = start
        self.Stop = stop
        self.Units = units
        self.par={"Name":name,
                    "Parameter":parameter,
                    "Type":type,
                    "Start": start,
                    "Stop": stop,
                    "Units":units}
    def addtosweep(self,sim):
        sim.addsweepparameter(self.sweep_name, self.par);  



def setup(sim):
    sweep_name="pml_distance"
    name="z span"
    parameter="model::FDTD::z span"
    Type = "Length"
    Start = 0.05e-6
    Stop = 0.15e-6
    Units = "microns"
    
    para=Parameter(sim=sim,sweep_name=sweep_name,name=name,parameter=parameter,type=Type,start=Start,stop=Stop,units=Units)
    para.addtosweep(sim)
    input("Enter ...")

def PML_distance_z_span(sim,filename,z_span_linspace):
    log = setup_logger("pml_distance_z_span", "logging/pml_distance_z_span.log")
    filename="mmi_1x2_fdtd"
    wg_length=opt_wg_length
    wg_width=1.6e-6
    width_ridge=opt_width_ridge
    mmi_length=opt_mmi_length
    taper_width=opt_taper_width
    taper_width_in=taper_width
    delta_y=0
    mesh_accuracy=3
    T_cross_values=[]
    T_bar_values=[]
    for span in z_span_linspace:
        T_cross,T_bar,E_lateral=fdtd_solver(sim=sim,filename=filename,width_ridge=width_ridge,
                mmi_length=mmi_length,taper_width=taper_width,taper_width_in=taper_width_in,mesh_accuracy=mesh_accuracy,delta_y=delta_y,FDTD_z_span=span)
        T_cross_values.append(T_cross)
        T_bar_values.append(T_bar)
        log.info(f"T_cross: {T_cross}, T_bar: {T_bar}")
        
          



if __name__=="__main__":
    filename="../nm1550/mmi_1x2_fdtd"
    z_span=np.linspace(1.5e-6,4e-6,10)
    PML_distance_z_span(sim=lumapi.FDTD(filename),filename=filename,z_span_linspace=z_span)