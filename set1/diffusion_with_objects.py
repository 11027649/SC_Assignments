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

    current_state = DiffusionGrid(height, width, D, dt, timesteps, "Time_Dependent")
    current_state.add_object((20, 10), 15, 5)
    # calculate states
    for t in range(timesteps):
        current_state.next_step()

    current_state.plot_time_frames()


if __name__ == '__main__':
    main()
