from crpropa import *
import numpy as np

z = np.linspace(0, 2.5, 100)

Hz = [hubbleRate(i) for i in z]
Hz = np.array(Hz)*3.085677581491367E19

with open("hzL.txt", "w") as f:
    for i in range(len(z)):
        f.write(str(z[i]) + " " + str(Hz[i]) + "\n")
