# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This file is part of a program that is used to solve some partial differential
# equations. The program has been developed for the course Scientific Computing
# in the master Computational Science at the UvA february/march 2019.
#
# This part contains the code to calculate the omegas for grids with objects in it.
#
# Run it by: python diffusion_omega_objects.py
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
    gridsize = 50

    omegas = np.arange(1.870, 1.930, 0.001)

    best_omega = math.inf
    best_timestep = math.inf

    for omega in omegas:
        print("omega", omega)
        current_state = DiffusionGrid(gridsize, D, "SOR")
        current_state.set_omega(omega)

        ## OBJECTS: one big square
        current_state.add_object((10, 10), 30, 5)

        ## OBJECTS: two small squares
        # current_state.add_object((10, 10), 5, 5)
        # current_state.add_object((35, 10), 5, 5)

        while not current_state.converged:
            current_state.next_step()

        if current_state.time < best_timestep:
            best_timestep = current_state.time
            best_omega = omega

        print("best omega", best_omega, best_timestep)


if __name__ == '__main__':
    main()
