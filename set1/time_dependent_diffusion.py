import numpy as np
import math
import pandas
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy

frames = []
im = []
k = 0

def main():
    global frames, im
    # diffusion coefficient
    D = 0.1

    # divide grid in 100 discrete steps
    height = 50
    width = 100

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
    fig.set_dpi(100)
    ax1 = fig.add_subplot(1,1,1)

    # list of arrays
    #https://stackoverflow.com/questions/39472017/how-to-animate-the-colorbar-in-matplotlib

    for i in range(10):
        next_grid = next(height, width, D, dt, dx, grid)
        frames.append(next_grid)

    grid = frames[0]
    im = ax1.imshow(grid, cmap="winter") #plt
    cb = fig.colorbar(im) #plt
    # tx = ax1.set_title('Frame 0')

    #JUST FOR CHECKING
    # next_grid = next(height, width, D, dt, dx, grid)
    # print('new')
    # print(next_grid)

    anim = animation.FuncAnimation(fig, animate, frames=200) #, interval=100, blit=True)
    # plt.ylim(0, height)
    plt.show()


def animate(i):
    global frames, im, k
    arr = frames[i]
    im.set_data(arr) #im.set_data(next_grid)
    # tx.set_text('Frame {0}'.format(i))
    k += 1


def initialize(height, width):
    """" Initalize grid """
    grid = [[0 for col in range(width)] for row in range(height)]

    # initialize top with concentration 1
    for j in range(width):
        grid[0][j] = 1

    return grid


def next(height, width, D, dt, dx, current_state):
    """ Compute concentration in each grid point.
        TODO: out of bounds check (now ignoring x,y =0 and x,y =100) """
    next_state = copy.copy(current_state)
    # iterate over grid, first row is always concentration 1, last row always 0
    for i in range(height): #range(1, height - 1):
        # iterate over columns, first and last are periodic boundaries
        for j in range(width):
            # print('i', i)
            # print('j', j)

            # when the state is at the first or last row
            if current_state[0][j] or current_state[-1][j]:
                next_state[i][j] = current_state[i][j]

            # when the state is out of bound on left side grid
            elif current_state[i][0]:
                next_state[i][j] = current_state[i][j]\
                                    + (dt * D)/dx**2 * (current_state[i+1][j]\
                                    + current_state[-1][j]\
                                    + current_state[i][j + 1]\
                                    + current_state[i][j - 1]\
                                    - 4 * current_state[i][j])

            # when the state is out of bound on right side grid
            elif current_state[i][-1]:
                next_state[i][j] = current_state[i][j]\
                                    + (dt * D)/dx**2 * (current_state[0][j]\
                                    + current_state[i - 1][j]\
                                    + current_state[i][j + 1]\
                                    + current_state[i][j - 1]\
                                    - 4 * current_state[i][j])

            # when the state is not in any boundary
            else:
                next_state[i][j] = current_state[i][j]\
                                    + (dt * D)/dx**2 * (current_state[i+1][j]\
                                    + current_state[i - 1][j]\
                                    + current_state[i][j + 1]\
                                    + current_state[i][j - 1]\
                                    - 4 * current_state[i][j])
    return next_state

if __name__ == '__main__':
    main()
