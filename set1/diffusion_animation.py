import numpy as np
import math

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors

import copy
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
    timesteps = math.ceil(tmax/dt)

    # these need to be global for the animation
    global current_state, im

    # initiate image and diffusion grid
    current_state = DiffusionGrid(height, width, D, dt, timesteps, "Time_Dependent")

    # set up figure
    fig = plt.figure()
    fig.suptitle("Diffusion over time, time dependent method")

    im =  plt.imshow(current_state.grid, interpolation='bicubic', cmap="winter")

    # call the animator, blit = True means only redraw changed part
    anim = animation.FuncAnimation(fig, animate, frames=timesteps, interval=1, blit=True, repeat=False)

    # show animation
    plt.xticks([])
    plt.yticks([])
    plt.colorbar()
    plt.show()

    anim.save("results/vids_diffusion/diffusion_" + current_state.method + ".mp4")
    print("Saved MP4 of the simulation")


def animate(i):
    """ Calculate next state and set that for the animation. """

    current_state.next_step()
    im.set_data(current_state.grid)

    return im,

if __name__ == '__main__':
    main()
