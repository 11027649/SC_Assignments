import numpy as np
import math
import pandas
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy
import tkinter as tk

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
    # current_state = DiffusionGrid(height, width, D, dt, dx, "Jacobi")
    # current_state = DiffusionGrid(height, width, D, dt, dx, "Gauss_Seidel")
    # current_state = DiffusionGrid(height, width, D, dt, "SOR")

    # ask user what to do
    print("Do you want to see the animation of the diffusion? Yes/No", end=" ")
    visualization = input()

    if visualization == "no":
        for t in range(timesteps + 1):
            current_state.next_step()

        current_state.plot_time_frames()
    elif visualization == "yes":
        im =  plt.imshow(current_state.grid, norm=colors.Normalize(vmin=0,vmax=1))

        # call the animator, blit = True means only redraw changed part
        anim = animation.FuncAnimation(fig, animate, frames=timesteps, interval=1, blit=True)

        # show animation
        plt.xticks([])
        plt.yticks([])
        plt.colorbar()
        plt.show()

        anim.save("results/Diffusion.mp4")
        print("Saved MP4 of the simulation")


def animate(i):
    """ Calculate next state and set that for the animation. """

    current_state.next_step()
    im.set_data(current_state.grid)

    return im,

if __name__ == '__main__':
    main()
