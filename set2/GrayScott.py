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
        self.v_conc = np.zeros((self.width, self.height))
        self.u_conc = np.zeros((self.width, self.height))

        for j in range(self.width):
            for i in range(self.height):
                self.u_conc[i,j] = 0.5

        print(self.u_conc)

        # initialize a small center with v = 0.25
        for j in range(40, 55):
            for i in range(40,55):
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

        self.v_next = np.zeros((self.width, self.height))
        self.u_next = np.zeros((self.width, self.height))

        # iterate over grid, first row is always concentration 1, last row always 0
        for i in range(self.height):
            # iterate over columsn, first and last are periodic boundaries
            for j in range(self.width):
                try:
                    self.u_next[i, j] = (self.dt * self.Du/self.dx**2)\
                        * (self.u_conc[(i + 1) % self.width, j] + self.u_conc[i - 1, j]\
                        + self.u_conc[i, (j + 1) % self.height] + self.u_conc[i, j - 1] - 4 * self.u_conc[i, j])\
                        - self.dt * self.u_conc[i, j] * (self.v_conc[i , j]**2 + self.f)\
                        + self.dt * self.f

                    self.v_next[i, j] = (self.dt * self.Dv/self.dt**2)\
                                    * (self.v_conc[(i + 1) % self.width, j] + self.v_conc[i - 1, j]\
                                    + self.v_conc[i, (j + 1) % self.height] + self.v_conc[i, j - 1] - 4 * self.v_conc[i, j])\
                                    + self.dt * self.v_conc[i, j] * (self.u_conc[i, j] * self.v_conc[i, j] - (self.f + self.k))

                except IndexError:
                    try:
                        self.u_next[i, j] = (self.dt * self.Du/self.dx**2)\
                            * (self.u_conc[(i + 1) % self.width, j] + self.u_conc[self.width - 1, j]\
                            + self.u_conc[i, (j + 1) % self.height] + self.u_conc[i, j - 1] - 4 * self.u_conc[i, j])\
                            - self.dt * self.u_conc[i, j] * (self.v_conc[i , j]**2 + self.f)\
                            + self.dt * self.f

                        self.v_next[i, j] = (self.dt * self.Dv/self.dt**2)\
                                        * (self.v_conc[(i + 1) % self.width, j] + self.v_conc[self.width - 1, j]\
                                        + self.v_conc[i, (j + 1) % self.height] + self.v_conc[i, j - 1] - 4 * self.v_conc[i, j])\
                                        + self.dt * self.v_conc[i, j] * (self.u_conc[i, j] * self.v_conc[i, j] - (self.f + self.k))

                    except IndexError:
                        self.u_next[i, j] = (self.dt * self.Du/self.dx**2)\
                            * (self.u_conc[(i + 1) % self.width, j] + self.u_conc[self.width - 1, j]\
                            + self.u_conc[i, (j + 1) % self.height] + self.u_conc[i, self.height - 1] - 4 * self.u_conc[i, j])\
                            - self.dt * self.u_conc[i, j] * (self.v_conc[i , j]**2 + self.f)\
                            + self.dt * self.f

                        self.v_next[i, j] = (self.dt * self.Dv/self.dt**2)\
                                        * (self.v_conc[(i + 1) % self.width, j] + self.v_conc[self.width - 1, j]\
                                        + self.v_conc[i, (j + 1) % self.height] + self.v_conc[i, self.height - 1] - 4 * self.v_conc[i, j])\
                                        + self.dt * self.v_conc[i, j] * (self.u_conc[i, j] * self.v_conc[i, j] - (self.f + self.k))

        self.v_conc = np.copy(self.v_next)
        self.u_conc = np.copy(self.u_next)
