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
import matplotlib.pyplot as plt
import copy
import time


class GrayScott():
    """ This is a class that implements a reaction diffusion system. """

    def __init__(self, gridsize):
        self.height = gridsize
        self.width = gridsize

        # initial parameters from the assignment
        self.Du = 0.16
        self.Dv = 0.08

        self.dx = 1
        self.dt = 1

        self.f = 0.035
        self.k = 0.06

        self.time = 0

        self.initialize()

    def initialize(self):
        """" Initalize grid """
        self.grid = np.array([numpy.array([0.5, 0]) for col in range(self.width)]))
        print(self.grid)
        self.grid = [[[0.5, 0] for col in range(self.width)] for row in range(self.height)]

        # initialize a small center with v = 0.25
        for j in range(20, 30):
            for i in range(20,30):
                self.grid[i][j][1] = 0.25

    def next_step(self):
        """ Compute concentration in each grid point according to the right
            method. """

        self.next_step_time_GS()
        self.time += 1

    def next_step_GS(self):
        """ Compute concentration in each grid point, according to the time dependent
            discretized partial differential equation. """

        current_state = self.grid
        next_state = copy.copy(self.grid)
        #
        # # iterate over grid, first row is always concentration 1, last row always 0
        # for i in range(1, self.height - 1):
        #     # iterate over columsn, first and last are periodic boundaries
        #     for j in range(self.width):
        #         if j == 0:
        #             next_state[i][j] = current_state[i][j]\
        #                                 + (self.dt * self.D)/self.dx**2 * (current_state[i + 1][j]\
        #                                 + current_state[i - 1][j]\
        #                                 + current_state[i][j + 1]\
        #                                 + current_state[i][self.width - 1]\
        #                                 - 4 * current_state[i][j])
        #         elif j == self.width - 1:
        #             next_state[i][j] = current_state[i][j]\
        #                                 + (self.dt * self.D)/self.dx)**2 * (current_state[i + 1][j]\
        #                                 + current_state[i - 1][j]\
        #                                 + current_state[i][0]\
        #                                 + current_state[i][j - 1]\
        #                                 - 4 * current_state[i][j])
        #         else:
        #             next_state[i][j] = current_state[i][j]\
        #                                 + (self.dt * self.D)/self.dx**2 * (current_state[i + 1][j]\
        #                                 + current_state[i - 1][j]\
        #                                 + current_state[i][j + 1]\
        #                                 + current_state[i][j - 1]\
        #                                 - 4 * current_state[i][j])
        #
        # self.grid = copy.copy(next_state)
