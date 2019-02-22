# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This file is part of a program that is used to solve some partial differential
# equations. The program has been developed for the course Scientific Computing
# in the master Computational Science at the UvA february/march 2019.
#
# This part of the program contains a file that calculates and plots a wave at
# different timepoints.
#
# Run this file by python vibrating_string.py and comment/uncomment the begin
# position you want to see.
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
    dt = 0.001
    tmax = 100
    timesteps = math.ceil(tmax/dt)

    # pick your type
    # type = "2pi"
    type = "5pi"
    # type = "5pi_constrained_domain"

    # global variables needed for animation
    global current_state, fig, ax1

    # initalize wave, pick 2pi, 5pi or 5pi_constrained_domain
    current_state = Wave(type, c, dt)

    for t in range(timesteps):
        current_state.next_step()

    current_state.plot_time_frames()

if __name__ == '__main__':
    main()
