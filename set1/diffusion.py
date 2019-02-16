import math
from DiffusionGrid import DiffusionGrid

def main():
    ####### Variables
    # diffusion coefficient
    D = 1

    # divide grid in 100 discrete steps
    height = 50
    width = 50

    # actual lengths are 1
    len_x = 1
    len_y = 1

    # time stuff
    dt = 0.0001
    tmax = 1
    timesteps = math.ceil(tmax/dt) + 1

    methods = ["Time_Dependent", "Jacobi", "Gauss_Seidel", "SOR"]

    for method in methods:
        current_state = DiffusionGrid(height, width, D, dt, timesteps, method)

        # calculate states
        for t in range(timesteps):
            current_state.next_step()

        current_state.plot_time_frames()
        current_state.compare_to_analytic_solution()


if __name__ == '__main__':
    main()
