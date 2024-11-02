from crpropa import *
import sys
import matplotlib.pyplot as plt
import numpy as np

# Input Parameters from the User
energia_injecao = float(input('Digite o valor de energia de injeção (EeV): '))  
max_distance = float(input('Digite a distância máxima da fonte (Mpc): '))

# List of distances from 10 to max_distance with 10 Mpc steps
distances = np.arange(100, max_distance + 1, 10) * Mpc  

# Arrays to store mean observed and injected energies
mean_observed_energies = []
mean_injected_energies = []

# Simulation Loop for Each Distance
for i, dist in enumerate(distances):
    print(f"Running simulation for distance {dist / Mpc:.1f} Mpc...")

    # Configure the Simulation
    sim = ModuleList()
    sim.add(SimplePropagation(1 * kpc, 10 * Mpc))  # 1D propagation
    sim.add(Redshift())  # Energy loss due to redshift
    sim.add(PhotoPionProduction(CMB()))  # Interaction with CMB
    sim.add(PhotoPionProduction(IRB_Gilmore12()))  # Interaction with IRB
    sim.add(PhotoDisintegration(CMB()))  # Photodisintegration with CMB
    sim.add(PhotoDisintegration(IRB_Gilmore12()))  # Photodisintegration with IRB
    sim.add(NuclearDecay())  # Handle nuclear decay
    sim.add(ElectronPairProduction(CMB()))  # Pair production with CMB
    sim.add(ElectronPairProduction(IRB_Gilmore12()))  # Pair production with IRB
    sim.add(MinimumEnergy(0.01 * EeV))  # Stop simulation if energy drops below threshold

    # Set up the Observer for the 1D simulation
    
    obs = Observer()
    obs.add(Observer1D())  # Add the 1D observer to the observer module

    # Output configuration
    output = TextOutput(f'eventosFR/events_{i + 1}FR.txt', Output.Event1D)
    obs.onDetection(output)  # Save events to file
    sim.add(obs)

    # Set up the Source at the Origin with Fixed Injection Energy
    source = Source()
    source.add(SourcePosition(dist))  # Source at origin
    source.add(SourceRedshift1D())  # Include redshift effects
    source.add(SourceEnergy(energia_injecao * EeV))  # Fixed injection energy
    source.add(SourceParticleType(nucleusId(1, 1)))  # Proton source

    # Run the Simulation with 10,000 Events (Reduce for Testing)
    sim.setShowProgress()  # Disable progress for stability in headless mode
    sim.run(source, 100, True)  # Run with 10,000 events

    output.close()  # Close the output file

    # Load the Simulation Results Safely
    try:
        data = np.genfromtxt(f'eventosFR/events_{i + 1}FR.txt', names=True)
        R = data['D']  # Distance traveled
        E = data['E']  # Observed energy
        E_inj = data['E0']  # Injected energy
    except Exception as e:
        print(f"Error loading data for distance {dist / Mpc:.1f} Mpc: {e}")
        mean_observed_energies.append(0)
        mean_injected_energies.append(0)
        continue

    # Compute Mean Energies if Data is Available
    mean_observed_energies.append(np.mean(E) if len(E) > 0 else 0)
    mean_injected_energies.append(np.mean(E_inj) if len(E_inj) > 0 else 0)

# Save the Results to a File
with open('energia_mediaFR.txt', 'w') as f:
    for i, dist in enumerate(distances):
        f.write(f"{dist / Mpc} {mean_observed_energies[i]} {mean_injected_energies[i]}\n")

# Plotting the Results
plt.figure(figsize=(10, 7))
plt.plot(distances / Mpc, mean_observed_energies, color='dodgerblue', marker='o', label='Média da Energia Observada')
plt.plot(distances / Mpc, mean_injected_energies, color='orange', linestyle='--', marker='x', label='Média da Energia Injetada')
plt.grid()
plt.legend()
plt.xlabel('Distância [Mpc]', fontsize=15)
plt.ylabel('Energia Média [EeV]', fontsize=15)
plt.title('Energia Observada e Energia Injetada vs Distância')
plt.savefig('energia_observada_vs_injetadaFR.png')
plt.show()
