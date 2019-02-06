import numpy as np
import math
import pandas
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy


def main():
    # diffusion coefficient
    D = 0.1

    # divide grid in 100 discrete steps
    height = 100
    width = 102

    # actual lengths are 1
    len_x = 1
    len_y = 1

    # deltas
    dx = len_x/width
    dy = len_y/height
    dt = 0.1

    grid = initialize(height, width)

    # set up the figure, the axis, and the plot element we want to animate
    fig = plt.figure()
    im =  plt.imshow(grid, cmap="winter")
    plt.colorbar()

    next_grid = next(height, width, D, dt, dx, grid)

    anim = animation.FuncAnimation(fig, animate, frames=200, interval=100, blit=True)
    plt.show()


def animate(i):
    im.set_data(next_grid)


def initialize(height, width):
    """" Initalize grid """
    grid = [[0 for col in range(width)] for row in range(height)]

    # initialize top with concentration 1
    for i in range(0, width):
        grid[0][i] = 1

    return grid


def next(height, width, D, dt, dx, current_state):
    """ Compute concentration in each grid point.
        TODO: out of bounds check (now ignoring x,y =0 and x,y =100) """
    next_state = copy.copy(current_state)
    # iterate over grid, first row is always concentration 1, last row always 0
    for i in range(1, height - 1):
        # iterate over columsn, first and last are periodic boundaries
        for j in range(1, width - 1):
            next_state[i][j] = current_state[i][j]\
                                + (dt * D)/dx**2 * (current_state[i+1][j]\
                                + current_state[i - 1][j]\
                                + current_state[i][j + 1]\
                                + current_state[i][j - 1]\
                                - 4 * current_state[i][j])

    return next_state







if __name__ == '__main__':
    main()
