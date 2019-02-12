import numpy as np
import math
import pandas
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy

from matplotlib import colors

def main():
    # set up figure
    fig = plt.figure()
    fig.suptitle("Time dependent diffusion")

    ####### Variables
    # diffusion coefficient
    D = 1

    # divide grid in 100 discrete steps
    height = 50
    width = 10

    # actual lengths are 1
    len_x = 1
    len_y = 1

    # deltas and time stuff
    dx = len_x/width
    dy = len_y/height
    dt = 0.001
    tmax = 1
    timesteps = math.ceil(tmax/dt)

    # these need to be global for the animation
    global current_state, im

    # initiate image and diffusion grid
    current_state = DiffusionGrid(height, width, D, dt, dx)
    im =  plt.imshow(current_state.grid, norm=colors.Normalize(vmin=0,vmax=1))

    # call the animator, blit = True means only redraw changed part
    anim = animation.FuncAnimation(fig, animate, frames=timesteps, interval=50, blit=True)

    # show animation
    plt.colorbar()
    plt.show()
    print("done!")
    anim.save("results/Diffusion.mp4", fps=30, extra_args=['-vcodec', 'libx264'])


def animate(i):
    """ Calculate next state and set that for the animation. """
    current_state.next_step()
    im.set_data(current_state.grid)

    return im,


class DiffusionGrid():
    """ This is a class that contains the diffusion coefficient and dimensions for
        the diffusion grid. It also contains the diffusion grid itself."""

    def __init__(self, height, width, D, dt, dx):
        self.height = height
        self.width = width
        self.D = D
        self.dt = dt
        self.dx = dx

        self.initialize()

    def initialize(self):
        """" Initalize grid """
        self.grid = [[0 for col in range(self.width)] for row in range(self.height)]

        # initialize top with concentration 1
        for i in range(0, self.width):
            self.grid[0][i] = 1

    def next_step(self):
        """ Compute concentration in each grid point. """

        current_state = self.grid
        next_state = copy.copy(self.grid)

        # iterate over grid, first row is always concentration 1, last row always 0
        for i in range(1, self.height - 1):
            # iterate over columsn, first and last are periodic boundaries
            for j in range(1, self.width - 1):
                next_state[i][j] = current_state[i][j]\
                                    + (self.dt * self.D)/self.dx**2 * (current_state[i+1][j]\
                                    + current_state[i - 1][j]\
                                    + current_state[i][j + 1]\
                                    + current_state[i][j - 1]\
                                    - 4 * current_state[i][j])

            # copy for periodic boundaries
            next_state[i][0] = next_state[i][self.width - 2]
            next_state[i][self.width - 1] = next_state[i][1]

        self.grid = copy.copy(next_state)



if __name__ == '__main__':
    main()
