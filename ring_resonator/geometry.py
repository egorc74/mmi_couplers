from variables import *
def geometry(sim,filename,cladding=None):
    try:
        log = setup_logger("geometry", "logging/geometry.log")


        #draw wg for bending losses calculations
        sim.switchtolayout()
        sim.deleteall()


        Xmin = -3e-6  
        Xmax = 3e-6 
        Zmin = -height_margin  
        Zmax = thick_Si3N4 + height_margin
        Y_span = 2*width_margin + wg_width
        Ymin = -Y_span/2
        Ymax = -Ymin

        # draw cladding
        if cladding!=None:
            sim.addrect()
            sim.set("name", "Clad")
            sim.set("material", material_Clad)
            sim.set("y", 0)
            sim.set("y span", Y_span + 1e-6)
            sim.set("z min", 0)
            sim.set("z max", thick_Clad)
            sim.set("x min", Xmin)
            sim.set("x max", Xmax)
            sim.set("override mesh order from material database", 1)
            sim.set("mesh order", 3)  # send to back
            sim.set("alpha", 0.05)

        # draw buried oxide
        sim.addrect()
        sim.set("name", "BOX")
        sim.set("material", material_BOX)
        sim.set("x min", Xmin)
        sim.set("x max", Xmax)
        sim.set("z min", -thick_BOX)
        sim.set("z max", 0)
        sim.set("y", 0)
        sim.set("y span", Y_span + 1e-6)
        sim.set("alpha", 0.05)

        # draw silicon wafer
        sim.addrect()
        sim.set("name", "Wafer")
        sim.set("material", material_Si)
        sim.set("x min", Xmin)
        sim.set("x max", Xmax)
        sim.set("z max", -thick_BOX)
        sim.set("z min", -thick_BOX - 2e-6)
        sim.set("y", 0)
        sim.set("y span", Y_span + 1e-6)
        sim.set("alpha", 0.1)

        # draw waveguide
        sim.addrect()
        sim.set("name", "waveguide")
        sim.set("material", material_Si3N4)
        sim.set("y", 0)
        sim.set("y span", wg_width)
        sim.set("z min", 0)
        sim.set("z max", thick_Si3N4)
        sim.set("x min", Xmin)
        sim.set("x max", Xmax)
    except Exception as e:
        log.error(e)



if __name__=="__main__":
    filename="bend_calculations"
    geometry(sim=lumapi.MODE(),filename=filename)





    