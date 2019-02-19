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

    # actual lengths are 1
    len_x = 1
    len_y = 1

    # time stuff
    dt = 0.0001
    tmax = 1
    timesteps = math.ceil(tmax/dt) + 1

    methods = ["Gauss_Seidel", "SOR", "Jacobi", "Time_Dependent"]

    for method in methods:
        print("method" + method)
        current_state = DiffusionGrid(height, width, D, dt, timesteps, method)

        # calculate states
        if method == "Time_Dependent":
            for t in range(timesteps):
                print(t)
                current_state.next_step()

            current_state.compare_to_analytic_solution()
        elif method == "SOR":
            current_state.set_omega(1.85)
            # for the time independent solutions, calculate next states until converged
            converged = False
            while not converged:
                print(str(current_state.time) + str(converged))
        else:
            # for the time independent solutions, calculate next states until converged
            converged = False
            while not converged:
                print(str(current_state.time) + str(converged))

        current_state.plot_time_frames()



if __name__ == '__main__':
    main()
