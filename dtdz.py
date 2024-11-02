from crpropa import *
import numpy as np

z = np.linspace(0, 2.5, 100)
dzdt = [(1/((1+i)*hubbleRate(i)))/(60*60*24*365*1e6) for i in z]

with open("dtdz.txt", "w") as f:
    for i in range(len(dzdt)):
        f.write(str(dzdt[i]) + " " + str(z[i]) + "\n")