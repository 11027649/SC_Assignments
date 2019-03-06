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

        self.total_u = []
        self.total_v = []

        # initial parameters from the assignment
        self.Du = 0.16
        self.Dv = 0.08

        self.dx = 1
        self.dt = 1

        self.f = 0.035
        self.k = 0.060

        self.time = 0

        self.initialize()

    def initialize(self):
        """" Initalize grid """
        self.v_conc = np.zeros((self.width, self.height))
        self.u_conc = np.zeros((self.width, self.height))

        # initailize the whole system with u = 0.5
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

        if self.time % 50 == 0:
            total_u, total_v = self.total_concentrations()
            self.total_u.append(total_u)
            self.total_v.append(total_v)

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
                    self.update_conc(i, j, i - 1, j - 1)
                except IndexError:
                    try:
                        self.update_conc(i, j, self.width - 1, j - 1)

                    except IndexError:
                        self.update_conc(i, j, self.width - 1, self.height - 1)

        self.v_conc = np.copy(self.v_next)
        self.u_conc = np.copy(self.u_next)

    def update_conc(self, i, j, left, left_upper):
        """ Update the concentration of u, v, and p. """

        # diffusion values
        self.u_next[i, j] = self.u_conc[i, j] + (self.dt * self.Du/self.dx**2)\
            * (self.u_conc[(i + 1) % self.width, j] + self.u_conc[left, j]\
            + self.u_conc[i, (j + 1) % self.height] + self.u_conc[i, left_upper] - 4 * self.u_conc[i, j])\
            - self.u_conc[i, j] * (self.v_conc[i , j]**2) + self.f * (1 - self.u_conc[i, j])

        self.v_next[i, j] = self.v_conc[i, j] + (self.dt * self.Dv/self.dx**2)\
            * (self.v_conc[(i + 1) % self.width, j] + self.v_conc[left, j]\
            + self.v_conc[i, (j + 1) % self.height] + self.v_conc[i, left_upper] - 4 * self.v_conc[i, j])\
            + self.u_conc[i, j] * (self.v_conc[i , j]**2)  - (self.f + self.k) * self.v_conc[i, j]

    def total_concentrations(self):
        """ Return total concentrations of u and v in the grid. """
        u = np.sum(self.u_conc)
        v = np.sum(self.v_conc)

        return u, v
