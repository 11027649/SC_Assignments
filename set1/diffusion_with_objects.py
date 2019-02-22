# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This file is part of a program that is used to solve some partial differential
# equations. The program has been developed for the course Scientific Computing
# in the master Computational Science at the UvA february/march 2019.
#
# This part contains the code to put other sinks in the diffusion grid for
# exercise K. Since we found that SOR is the most efficient for solving diffusion
# we use that for the diffusion with objects.
#
# Run it by: python diffusion_with_objects.py and comment/uncomment the objects
# you want to place in the grid (or design your own :-)!)
# Romy Meester & Natasja Wezel
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import math
from DiffusionGrid import DiffusionGrid

import seaborn as sns
sns.set()

def main():
    ####### Variables
    # diffusion coefficient
    D = 1

    # divide grid in 50 discrete steps
    gridsize = 50

    current_state = DiffusionGrid(gridsize, D, "SOR")

    # take best omega, calculated in previous exercise
    current_state.set_omega(1.91)

    ## OBJECTS: one big square
    current_state.add_object((10, 10), 30, 5)

    ## OBJECTS: two small squares
    # current_state.add_object((10, 10), 5, 5)
    # current_state.add_object((35, 10), 5, 5)

    #### OBJECTS: triangle
    # for i in range(1, 15):
    #     current_state.add_object((25, 5 + i), i, 1)

    #### OBJECTS: a symmetric triangle
    # for i in range(1, 21, 2):
    #     current_state.add_object((25 - math.ceil(i / 2), 5 + i), i, 1)

    # calculate states
    while not current_state.converged:
        current_state.next_step()

    # see what it looks like
    current_state.plot_time_frames()



if __name__ == '__main__':
    main()
