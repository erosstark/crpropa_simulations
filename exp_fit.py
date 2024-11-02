import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# for i in range(1,21):
#     eventos = np.loadtxt(f'eventosLCDM/events_{i}.txt')
#     media = np.mean(eventos[:, 2])
#     with open('energia_mediaLCDM.txt', 'a') as f:
#         f.write(f'{eventos[0][0]} {media} {eventos[0][4]}\n')

# Leitura dos dados do arquivo .txt
dados = np.loadtxt('energia_mediaFRtest.txt')

# Definição da função exponencial
def func_exponencial(x, a, b):
    return a / (np.exp(b * x))

# Ajuste da curva exponencial
popt, pcov = curve_fit(func_exponencial, dados[:, 0], dados[:, 1], p0=[1000, 0.5])

# Impressão dos parâmetros ajustados
print('Parâmetros ajustados: a = %.2f, b = %.2f' % (popt[0], popt[1]))

plt.figure(figsize=(10, 7))
plt.plot(dados[:,0], dados[:,1], color='dodgerblue', marker='o', label='Média da Energia Observada')
plt.plot(dados[:,0], dados[:,2], color='orange', linestyle='--', marker='x', label='Média da Energia Injetada')
plt.plot(dados[:, 0], func_exponencial(dados[:, 0], *popt), 'r-', label='Curva ajustada')
plt.grid()
plt.legend()
plt.text(0.5, 0.5, 'a = %.2f, b = %.2f' % (popt[0], popt[1]), transform=plt.gca().transAxes)
plt.ylim(bottom=0)
plt.xlabel('Distância [Mpc]', fontsize=15)
plt.ylabel('Energia Média [EeV]', fontsize=15)
plt.title('Energia Observada e Energia Injetada vs Distância')
plt.savefig('energia_observada_vs_injetada test.png')
plt.show()
