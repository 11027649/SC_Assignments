import numpy as np
from DiffusionGrid import DiffusionGrid
import csv
import matplotlib.pyplot as plt

## load object
object = "object_0"
object_grid = np.loadtxt("results/diffusion/" + object + ".txt")

## perform SOR with different omegas

omegas = np.arange(1.70, 1.99, 0.01)
eta = 2.0
gridsize = 100

steps = []
for omega in omegas:
    print("omega", omega)
    current_state = DiffusionGrid(gridsize, eta)
    current_state.set_omega(omega)
    current_state.object_grid = object_grid
    current_state.add_object()

    while not current_state.converged:
        current_state.next_step()

    # write down all omegas and the amount of steps it takes with that omega
    with open("omega_results.csv", 'a') as resultsfile:
        csvwriter = csv.writer(resultsfile, delimiter=',')
        csvwriter.writerow([omega, current_state.step])

## save steps
