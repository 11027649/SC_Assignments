# SOR is most efficient solver, so use that for the diffusion with objects

import math
from DiffusionGrid import DiffusionGrid

import seaborn as sns
sns.set()

def main():
    ####### Variables
    # diffusion coefficient
    D = 1

    # divide grid in 100 discrete steps
    height = 50
    width = 50

    current_state = DiffusionGrid(height, width, D, "SOR")
    current_state.set_omega(1.91)

    ## OBJECTS 1
    current_state.add_object((20, 10), 15, 5)

    ## OBJECTS 2
    # current_state.add_object((10, 5), 10, 5)
    # current_state.add_object((30, 5), 10, 5)

    ## OBJECTS 3
    # current_state.add_object((25, 10), 5, 30)

    ## OBJECTS 4
    # current_state.add_object((10, 10), 5, 5)
    # current_state.add_object((35, 10), 5, 5)

    #### ADD A triangle
    # for i in range(1, 15):
    #     current_state.add_object((25, 5 + i), i, 1)

    # for i in range(1, 21, 2):
    #     current_state.add_object((25 - math.ceil(i / 2), 5 + i), i, 1)

    # calculate states
    while not current_state.converged:
        current_state.next_step()

    current_state.plot_time_frames()


if __name__ == '__main__':
    main()
