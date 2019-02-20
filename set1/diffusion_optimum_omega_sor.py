import math
from DiffusionGrid import DiffusionGrid

import seaborn as sns
sns.set()

def main():
    ####### Variables
    # diffusion coefficient
    D = 1

    # divide grid in 50 discrete steps
    height = 50
    width = 50

    # actual lengths are 1
    len_x = 1
    len_y = 1

    # time stuff
    dt = 0.0001
    tmax = 1

    current_state = DiffusionGrid(height, width, D, dt, timesteps, "SOR")

    # set weight
    current_state.set_omega(1.85)

    # calculate until converged
    while not current_state.converged:
        print(str(current_state.time) + str(current_state.converged))

if __name__ == '__main__':
    main()
