# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This file is part of a program that is used to solve some partial differential
# equations. The program has been developed for the course Scientific Computing
# in the master Computational Science at the UvA february/march 2019.
#
# This part contains the code to calculate the omegas for the SOR method, and
# creates a file with results called omega_results.csv.
# This can be plotted with the functions in the plot omega file. Together
# they are the answer to exercise J.
#
# Run it by: python diffusion_optimum_omega_sor.py
# Romy Meester & Natasja Wezel
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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

    # run for multiple gridsizes
    gridsizes = np.arange(80, 100, 5)

    # try all omegas between 1.700 and 1.999
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

            # write down all omegas and the amount of steps it takes with that omega
            with open("omega_results.csv", 'a') as resultsfile:
                csvwriter = csv.writer(resultsfile, delimiter=',')
                csvwriter.writerow([gridsize, omega, current_state.time])

if __name__ == '__main__':
    main()
