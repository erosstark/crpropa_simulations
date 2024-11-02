import matplotlib.pyplot as plt
import numpy as np

# # Leitura dos dados do arquivo .txt
# dadosFR = np.loadtxt('testeFR/eventosTestFR/energia_mediaFR_p.txt')
# dadosLCDM = np.loadtxt('eventosLCDM/eventos_p/energia_media.txt')

# # Calcula a razão entre as energias medias
# razao = dadosFR[:, 1]/dadosLCDM[:, 1]

# # Salva a razão em um arquivo .txt  
# with open('razao.txt', 'w') as f:
#     for i in range(len(razao)):
#         f.write(f'{dadosFR[i, 0]} {razao[i]}\n')

        
# # Plotando a razão entre as energias medias
# plt.figure(figsize=(10, 7))
# plt.plot(dadosFR[:, 0], razao, color='dodgerblue', marker='o', label='Razão entre as Energias')
# plt.grid()
# plt.legend()
# plt.xlabel('Distância [Mpc]', fontsize=15)
# plt.ylabel('Energia Média  FR/LCDM', fontsize=15)
# plt.title('Razão entre as Energias Médias dos Modelos f(R) e LCDM')
# plt.savefig('razao_distancia_p.png')
# plt.show()

razao = np.loadtxt('razao.txt')
slop, intercept = np.polyfit(razao[:, 0], razao[:, 1], 1)
print(slop, intercept)

y_fit = slop * razao[:, 0] + intercept
plt.figure(figsize=(10, 7))
plt.plot(razao[:, 0], razao[:, 1], color='dodgerblue', marker='o', label='Razão entre as Energias')
plt.plot(razao[:, 0], y_fit, color='orange', linestyle='--', marker='x', label='fit Razão entre as Energias')
plt.grid()
plt.text(0.8, 0.8, 'a = %.7f \nb = %.7f' % (slop, intercept), transform=plt.gca().transAxes)
plt.legend()
plt.ylim(0,2)
plt.xlabel('Distância [Mpc]', fontsize=15)
plt.ylabel('Energia Média  FR/LCDM', fontsize=15)
plt.title('Razão entre as Energias')
plt.savefig('fit_razao_distancia_p.png')
plt.show()