from crpropa import *
import sys
import matplotlib.pyplot as plt
import numpy as np


# Parâmetros passados pelo usuário
energia_injecao = float(input('Digite o valor de energia de injeção aqui:'))  # Energia de injeção fixa em EeV
distancia_sources = float(input('Digite o valor de distância aqui:'))

# Lista de distâncias
distances = np.arange(1, distancia_sources+1, 10)  # Distâncias de 10 a 100 Mpc em intervalos de 10 Mpc
mean_observed_energies = []  # Armazena a energia média observada para cada distância
mean_injected_energies = []  # Armazena a energia média injetada para cada distância
k = 0
# Loop para realizar simulações para cada distância de 10 a 100 Mpc
for distancia_sources in distances:
    print(f'Simulando distância {distancia_sources} Mpc')
    k += 1
    # Configuração da simulação
    sim = ModuleList()
    sim.add(SimplePropagation(1 * kpc, 10 * Mpc))
    sim.add(Redshift())
    sim.add(PhotoPionProduction(CMB()))
    sim.add(PhotoPionProduction(IRB_Gilmore12()))
    sim.add(PhotoDisintegration(CMB()))
    sim.add(PhotoDisintegration(IRB_Gilmore12()))
    sim.add(NuclearDecay())
    sim.add(ElectronPairProduction(CMB()))
    sim.add(ElectronPairProduction(IRB_Gilmore12()))
    sim.add(MinimumEnergy(0.01 * EeV))

    # Observador e saída
    obs = Observer()
    obs.add(Observer1D())
    output = TextOutput(f'testeFR/eventosTestFR/events_{k}FR.txt', Output.Event1D)
    obs.onDetection(output)
    sim.add(obs)

    # Fonte com energia de injeção fixa
    source = Source()
    source.add(SourcePosition(distancia_sources * Mpc))
    source.add(SourceRedshift1D())
    source.add(SourceEnergy(energia_injecao * EeV))  # Energia fixa
    source.add(SourceParticleType(nucleusId(1, 1)))  # Apenas prótons
    
    # Executa a simulação com 100.000 eventos
    sim.setShowProgress(False)
    sim.run(source, 10000, True)
    output.close()

    # Carregar os eventos
    d = np.genfromtxt(f'testeFR/eventosTestFR/events_{k}FR.txt', names=True)

    # Extrair a distância e energia observada e injetada
    R = d['D']      # Distância percorrida
    E = d['E']      # Energia observada
    E_inj = d['E0'] # Energia injetada (5ª coluna)

    # Calcular a energia média observada e injetada para a distância atual
    mean_observed_energy = np.mean(E) if len(E) > 0 else 0
    mean_injected_energy = np.mean(E_inj) if len(E_inj) > 0 else 0
    
    mean_observed_energies.append(mean_observed_energy)
    mean_injected_energies.append(mean_injected_energy)

with open('testeFR/eventosTestFR/energia_mediaFR_p.txt', 'w') as f:
    for i in range(len(distances)):
        f.write(f'{distances[i]} {mean_observed_energies[i]} {mean_injected_energies[i]}\n')
        
# Plotando Energia Observada e Energia Injetada vs Distância
plt.figure(figsize=(10, 7))
plt.plot(distances, mean_observed_energies, color='dodgerblue', marker='o', label='Média da Energia Observada')
plt.plot(distances, mean_injected_energies, color='orange', linestyle='--', marker='x', label='Média da Energia Injetada')
plt.grid()
plt.legend()
plt.xlabel('Distância [Mpc]', fontsize=15)
plt.ylabel('Energia Média [EeV]', fontsize=15)
plt.title('Energia Observada e Energia Injetada vs Distância')
plt.savefig('energia_observada_vs_injetadaFR_teste.png')
plt.show()
