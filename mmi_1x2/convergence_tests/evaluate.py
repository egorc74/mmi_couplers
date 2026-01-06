import numpy as np
import matplotlib.pyplot as plt
import time

#finds index where the maximum slope was achieved
def find_max_slope(array):
    indx=0
    slopes=[]
    for ii,value in enumerate(array):
        if ii!=0:
            slopes.append(value-array[ii-1])
        else:
            slopes.append(0)
        
    max_index = max(range(len(slopes)), key=lambda i: slopes[i])
    max_value = slopes[max_index]

    print(f"Found value of greatest leap:{max_value} and its index:{max_index}")
    return max_index,max_value

def check_value(value):
    #checks if change is less than 5%
    if value<=0.5:
        return True

def find_optimal_value(array):
    #first find max slope index
    while len(array)!=1:
        max_slope_index,max_value=find_max_slope(array)
        checked=check_value(array[max_slope_index])
        if checked: print("change is checked and is smaller than 0.5")
        next_vals = array[max_slope_index+1:]
        mu = np.mean(next_vals)
        sigma = np.std(next_vals, ddof=1)
        z = 1  # 66% Gaussian interval
        lower = mu - z * sigma
        upper = mu + z * sigma
        
        checked_inside_first_percentile= lower <= max_value <= upper
        if checked and checked_inside_first_percentile:
            
            return max_slope_index
        time.sleep(1)
        array=array[max_slope_index:]




def evaluate(datafile,theoretical_value=0.5):
    data=np.load(f"{datafile}.npz",allow_pickle=True)
    T_cross_values=np.array([d["T"] for d in data['T_cross_values']])
    T_bar_values=np.array([d["T"] for d in data['T_bar_values']])
    print(T_cross_values)
    Span=data["Span"]
    Stds=[]
    Std_Ns=[]
    Std_Theorys=[]

   
    
    for sp in range(len(T_cross_values)):
        if sp==0:

            numerator=np.sum((T_cross_values[sp]-T_cross_values[len(T_cross_values)-1])**2)
            denominator=np.sum(T_cross_values[sp]**2)
            std_N=np.sqrt(numerator/denominator)
            Std_Ns.append(std_N)

            numerator=np.sum((T_cross_values[sp]-theoretical_value)**2)
            denominator=np.sum(T_cross_values[sp]**2)
            std_Theory=np.sqrt(numerator/denominator)
            Std_Theorys.append(std_Theory)

        else:
            numerator=np.sum((T_cross_values[sp]-T_cross_values[sp-1])**2)
            denominator=np.sum(T_cross_values[sp]**2)
            std=np.sqrt(numerator/denominator)
            Stds.append(std)
            
            numerator=np.sum((T_cross_values[sp]-T_cross_values[len(T_cross_values)-1])**2)
            denominator=np.sum(T_cross_values[sp]**2)
            std_N=np.sqrt(numerator/denominator)
            Std_Ns.append(std_N)


            numerator=np.sum((T_cross_values[sp]-theoretical_value)**2)
            denominator=np.sum(T_cross_values[sp]**2)
            std_Theory=np.sqrt(numerator/denominator)
            Std_Theorys.append(std_Theory)



            
    Stds=np.array(Stds)
    Std_Ns=np.array(Std_Ns)
    Std_Theorys=np.array(Std_Theorys)




    #Start evaluation 
    #   1)At which value


    # print(f"Calculated STDs and STD_Ns: std:{Stds} \n std_N: {Std_Ns} \n std_Theory={Std_Theorys}")

    
    # plt.plot(Span[1:], Stds, label="std")
    # plt.plot(Span, Std_Ns, label="std_N")
    # plt.plot(Span, Std_Theorys, label="std_Theory")

    # plt.xlabel("x")
    # plt.ylabel("%")
    # plt.legend()
    # plt.grid(True)

    # plt.show()

    # print(f"Best value {Span[find_optimal_value(Std_Ns[:-1])]}")

if __name__=="__main__":
    datafile="data/dataset_PML_distance_z_span"
    evaluate(datafile=datafile)