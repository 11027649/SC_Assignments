import math

from DiffusionGrid import DiffusionGrid
import matplotlib.pyplot as plt
import numpy as np

import time
import csv

import seaborn as sns
sns.set()

def main():
    D = 1
    gridsize = 50

    gridsizes = np.arange(75, 150, 5)

    omegas = np.arange(1.700, 1.999, 0.001)

    optimum_omegas = []

    for gridsize in gridsizes:
        steps = []
        for omega in omegas:
            print("omega", omega)
            current_state = DiffusionGrid(gridsize, gridsize, D, "SOR")
            current_state.set_omega(omega)

            while not current_state.converged:
                current_state.next_step()

            with open("omega_results.csv", 'a') as resultsfile:
                csvwriter = csv.writer(resultsfile, delimiter=',')
                csvwriter.writerow([gridsize, omega, current_state.time])

if __name__ == '__main__':
    main()
