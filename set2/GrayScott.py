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
        self.v_conc = np.zeros((self.width + 2, self.height + 2))
        self.u_conc = np.zeros((self.width + 2, self.height + 2))

        for j in range(0, self.width + 2):
            for i in range(0, self.height + 2):
                self.u_conc[i,j] = 0.5

        print(self.u_conc)

        # initialize a small center with v = 0.25
        for j in range(22, 32):
            for i in range(22,32):
                self.v_conc[i,j] = 0.25

        print(self.v_conc)


    def next_step(self):
        """ Compute concentration in each grid point according to the right
            method. """

        self.next_step_GS()
        self.time += 1

    def next_step_GS(self):
        """ Compute concentration in each grid point, according to the time dependent
            discretized partial differential equation. """

        self.v_next = np.zeros((self.width + 2, self.height + 2))
        self.u_next = np.zeros((self.width + 2, self.height + 2))

        # iterate over grid, first row is always concentration 1, last row always 0
        for i in range(1, self.height - 2):
            # iterate over columsn, first and last are periodic boundaries
            for j in range(1, self.width - 2):
                self.u_next[i, j] = self.u_conc[i,j] + (self.dt * self.Du/self.dx**2)\
                                * (self.u_conc[i + 1, j] + self.u_conc[i - 1, j]\
                                + self.u_conc[i, j + 1] + self.u_conc[i, j - 1] - 4 * self.u_conc[i, j])\
                                - self.u_conc[i, j]*self.v_conc[i, j]**2 + self.f*(1 - self.u_conc[i, j])

                self.v_next[i, j] = self.v_conc[i , j] + (self.dt * self.Dv/self.dt**2)\
                                * (self.v_conc[i + 1, j] + self.v_conc[i - 1, j]\
                                + self.v_conc[i, j + 1] + self.v_conc[i, j - 1] - 4 * self.v_conc[i, j])\
                                - self.u_conc[i, j]*self.v_conc[i, j]**2 - (self.f + self.k)* self.v_conc[i, j]


        # stuff with pbc
        for i in range(self.width):
            self.u_next[0, i] = self.u_next[self.width, i]
            self.u_next[self.width + 1, i] = self.u_next[1, i]

            self.u_next[i, 0] = self.u_next[i, self.height]
            self.u_next[i, self.height + 1] = self.u_next[i, 1]

            self.v_next[0, i] = self.v_next[self.width, i]
            self.v_next[self.width + 1, i] = self.v_next[1, i]

            self.v_next[i, 0] = self.v_next[i, self.height]
            self.v_next[i, self.height + 1] = self.v_next[i, 1]

        self.v_conc = np.copy(self.v_next)
        self.u_conc = np.copy(self.u_next)
