# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This file is part of a program that is used to solve some partial differential
# equations. The program has been developed for the course Scientific Computing
# in the master Computational Science at the UvA february/march 2019.
#
# This part contains the code to solve the diffusion equation with the time
# dependent approach for exercises E and F. This solution is compared to the
# analytic solution at different timesteps by comparing its linear dependence on
# y and the state of this grid is also shown in a plot at all these timesteps.
#
# Run it by: python diffusion_time_dependent.py
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

    # actual lengths are 1
    len_x = 1
    len_y = 1

    # time stuff
    dt = 0.00001
    tmax = 1
    timesteps = math.ceil(tmax/dt) + 1

    current_state = DiffusionGrid(gridsize, D, "Time_Dependent")
    current_state.set_time(dt, timesteps)

    # solve
    for t in range(timesteps):
        print(t)
        current_state.next_step()

    # show plots
    current_state.compare_to_analytic_solution()
    current_state.plot_time_frames()


if __name__ == '__main__':
    main()
