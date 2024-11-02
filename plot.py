import matplotlib.pyplot as plt
import numpy as np

dataL = np.loadtxt('hzL.txt')
dataFr = np.loadtxt('hz.txt')

plt.plot(dataL[:,0], dataL[:,1], "r", label='$\Lambda CDM$')
plt.plot(dataFr[:,0], dataFr[:,1], 'b', label='$f(R)$')
plt.legend()
plt.ylabel('h(z) (km/s/Mpc)')
plt.xlabel('z')
plt.grid(True)
plt.ylim(0, 250)
plt.xlim(0, 2.5)
plt.savefig('hz.pdf')
plt.show()

dataL = np.loadtxt('dtdzL.txt')
dataFR = np.loadtxt('dtdz.txt')

plt.semilogy(dataL[:,1], dataL[:,0], 'r', label='$\Lambda CDM$(Myr)')
plt.semilogy(dataFR[:,1], dataFR[:,0], 'b', label='$f(R)$')
plt.legend()
plt.ylabel('dtdz')
plt.xlabel('z')
plt.xlim(0,2.5)
plt.savefig('dtdz.pdf')
plt.show()
