# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This file is part of a program that is used to solve some partial differential
# equations. The program has been developed for the course Scientific Computing
# in the master Computational Science at the UvA february/march 2019.
#
# BLAHBLAHBLAH ---------
#
# You can't run this class on its own, but it is used in all the other diffusion
# files.
# Romy Meester & Natasja Wezel
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import numpy as np
import math
import pandas
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy
import time
import random

class GrayScott():
    """ This is a class that implements the Reaction-diffusion,
    based on the time dependent diffusion equation. """

    def __init__(self, gridsize, D, method):
        self.height = gridsize
        self.width = gridsize
        self.D = D

        self.dx = 1/self.width
        self.time = 0

        self.saved_states = {}
        self.method = method

        # this is needed for the time independent methods
        self.converged = False
        self.convergence = []

        self.initialize()

    def initialize(self):
        """" Initalize grid """
        self.grid = [[0 for col in range(self.width)] for row in range(self.height)]

        # initialize top with concentration 1
        for i in range(0, self.width):
            self.grid[0][i] = 1

        self.object_grid = [[0 for col in range(self.width)] for row in range(self.height)]

    def set_time(self, dt, timesteps):
        """ Set the time settings for Time Dependent Diffusion. """

        self.dt = dt
        self.timesteps = timesteps

        # save grid at right times for plots later (right times for timesteps of
        # 0.00001)
        # the other methods are time independent so we don't want to save these timesteps
        self.save_times = [0, 100, 1000, 10000, 100000]

    def next_step(self):
        """ Compute concentration in each grid point according to the right
            method. """

        # save info for plots
        if self.time in self.save_times:
            self.saved_states[self.time/100000] =  copy.deepcopy(self)

        self.next_step_time_GS()
        self.time += 1

    def next_step_GS(self):
        """ Compute concentration in each grid point, according to the time dependent
            discretized partial differential equation. """

        current_state = self.grid
        next_state = copy.copy(self.grid)

        # iterate over grid, first row is always concentration 1, last row always 0
        for i in range(1, self.height - 1):
            # iterate over columsn, first and last are periodic boundaries
            for j in range(self.width):
                if j == 0:
                    next_state[i][j] = current_state[i][j]\
                                        + (self.dt * self.D)/self.dx**2 * (current_state[i + 1][j]\
                                        + current_state[i - 1][j]\
                                        + current_state[i][j + 1]\
                                        + current_state[i][self.width - 1]\
                                        - 4 * current_state[i][j])
                elif j == self.width - 1:
                    next_state[i][j] = current_state[i][j]\
                                        + (self.dt * self.D)/self.dx)**2 * (current_state[i + 1][j]\
                                        + current_state[i - 1][j]\
                                        + current_state[i][0]\
                                        + current_state[i][j - 1]\
                                        - 4 * current_state[i][j])
                else:
                    next_state[i][j] = current_state[i][j]\
                                        + (self.dt * self.D)/self.dx**2 * (current_state[i + 1][j]\
                                        + current_state[i - 1][j]\
                                        + current_state[i][j + 1]\
                                        + current_state[i][j - 1]\
                                        - 4 * current_state[i][j])

        self.grid = copy.copy(next_state)
