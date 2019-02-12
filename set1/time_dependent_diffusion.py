import numpy as np
import math
import pandas
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy

from DiffusionGrid import DiffusionGrid

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

if __name__ == '__main__':
    main()
