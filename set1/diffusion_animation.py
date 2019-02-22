# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This file is part of a program that is used to solve some partial differential
# equations. The program has been developed for the course Scientific Computing
# in the master Computational Science at the UvA february/march 2019.
#
# This part contains the code for the diffusion grid. It's most important
# properties are it's width and height (the diffusion grid is always a square)
# and the diffusion constant. It contains code for all the different methods that
# are used to solve the diffusion equation, including the analytic method.
#
# Run: python diffusion_animation.py
# Romy Meester & Natasja Wezel
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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
    gridsize = 50

    # actual lengths are 1
    len_x = 1
    len_y = 1

    # time stuff
    dt = 0.0001
    tmax = 0.2
    timesteps = math.ceil(tmax/dt)

    # these need to be global for the animation
    global current_state, im

    # initiate image and diffusion grid
    current_state = DiffusionGrid(gridsize, D, "Time_Dependent")
    current_state.set_time(dt, timesteps)

    # set up figure
    fig = plt.figure()
    fig.suptitle("Diffusion over time, time dependent method")

    im =  plt.imshow(current_state.grid, interpolation='bicubic')

    # call the animator, blit = True means only redraw changed part
    anim = animation.FuncAnimation(fig, animate, frames=timesteps, interval=1, blit=True, repeat=False)

    # show animation
    plt.xticks([])
    plt.yticks([])
    plt.colorbar()
    # plt.show()

    anim.save("results/vids_diffusion/diffusion_" + current_state.method + ".mp4", fps=200)
    print("Saved MP4 of the simulation")


def animate(i):
    """ Calculate next state and set that for the animation. """

    current_state.next_step()
    im.set_data(current_state.grid)

    return im,

if __name__ == '__main__':
    main()
