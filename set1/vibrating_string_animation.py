# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This file is part of a program that is used to solve some partial differential
# equations. The program has been developed for the course Scientific Computing
# in the master Computational Science at the UvA february/march 2019.
#
# This part of the program contains a file that makes and saves the animation
# of the vibrating string.
#
# Run this file by python vibrating_string_animation.py. Comment/uncomment
# the right starting position of the wave. Remember to be patient, saving the
# mp4 of your animation can take a lot of time.
# Romy Meester & Natasja Wezel
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import math

import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np
import copy

from Wave import Wave

def main():
    # variables
    c = 1.0

    # pick your type
    type = "2pi"
    # type = "5pi"
    # type = "5pi_constrained_domain"

    tmax = 1
    dt = 0.005

    timesteps = math.ceil(tmax/dt)

    # global variables needed for animation
    global current_state, fig, ax1

    # initalize wave, pick 2pi, 5pi or 5pi_constrained_domain
    current_state = Wave(type, c, dt)

    # initalize figure
    fig = plt.figure()
    fig.set_dpi(100)
    fig.suptitle("Vibrating String")

    ax1 = fig.add_subplot(1,1,1)

    # animate
    # interval is between frames
    anim = animation.FuncAnimation(fig, animate, frames=timesteps, interval=1) #, blit=True)

    writer = animation.FFMpegWriter(fps=500, extra_args=['-vcodec','libx264'])

    plt.show()

    # save animation
    # anim.save('results/vids_wave/vibrating_string_'+ current_state.type + '.mp4', writer=writer)


def animate(i):
    """ Calculate next state and set that for the animation. """

    current_state.next_step()
    ax1.clear()
    plt.plot(current_state.x, current_state.y_current, color="Pink")
    plt.grid(True)

    plt.ylim([-1.5,1.5])
    plt.xlim([0,1])

if __name__ == '__main__':
    main()
