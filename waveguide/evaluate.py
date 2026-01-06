from convergence_tests import *
import matplotlib.pyplot as plt

def evaluate(datafile,theoretical_value=None):
    data=np.load(f"{datafile}.npz",allow_pickle=True)
    neff_values=np.array(data['neff_values'])
    print(neff_values)
    Span=data["Span"]
    Stds=[]
    Std_Ns=[]
    Std_Theorys=[]
    for sp in range(len(neff_values)):
        if sp==0:

            numerator=np.sum((neff_values[sp]-neff_values[len(neff_values)-1])**2)
            denominator=np.sum(neff_values[sp]**2)
            std_N=np.sqrt(numerator/denominator)
            Std_Ns.append(std_N)

            if(theoretical_value):
                numerator=np.sum((neff_values[sp]-theoretical_value)**2)
                denominator=np.sum(neff_values[sp]**2)
                std_Theory=np.sqrt(numerator/denominator)
                Std_Theorys.append(std_Theory)

        else:
            numerator=np.sum((neff_values[sp]-neff_values[sp-1])**2)
            denominator=np.sum(neff_values[sp]**2)
            std=np.sqrt(numerator/denominator)
            Stds.append(std)
            
            numerator=np.sum((neff_values[sp]-neff_values[len(neff_values)-1])**2)
            denominator=np.sum(neff_values[sp]**2)
            std_N=np.sqrt(numerator/denominator)
            Std_Ns.append(std_N)

            if(theoretical_value):
                numerator=np.sum((neff_values[sp]-theoretical_value)**2)
                denominator=np.sum(neff_values[sp]**2)
                std_Theory=np.sqrt(numerator/denominator)
                Std_Theorys.append(std_Theory)

    Stds=np.array(Stds)*100
    Std_Ns=np.array(Std_Ns)*100
    Std_Theorys=np.array(Std_Theorys)*100

    print(f"Calculated STDs and STD_Ns: std:{Stds} \n std_N: {Std_Ns} \n std_Theory={Std_Theorys}")
    plt.plot(Span[1:], Stds, label="std")
    plt.plot(Span, Std_Ns, label="std_N")
    if(theoretical_value):
        plt.plot(Span, Std_Theorys, label="std_Theory")

    plt.xlabel("x")
    plt.ylabel("%")
    plt.legend()
    plt.grid(True)

    plt.show()
if __name__=="__main__":
    datafile="data/FDE_y_span"
    datafile="data/FDE_z_span"
    datafile="data/Mesh_accuracy_z"

    evaluate(datafile=datafile)