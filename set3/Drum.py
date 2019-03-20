# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This file is part of a program that is used to solve the wave equations.
# The program has been developed for the course Scientific Computing
# in the master Computational Science at the UvA february/march 2019.
#
# This part contains the class for a Drum. It contains the eigenmodes of drums
# or membranes of either a square, rectangle or circle. 
#
# You can't run this class on its own, but it is used in the drum
# program for making the animation.
# Romy Meester & Natasja Wezel
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import math

import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np
import copy

class Drum():
    def __init__(self, matrix, eigenvalue, shape):

        self.state = np.copy(matrix)
        self.prev_state = np.copy(matrix)

        self.eigenvalue = eigenvalue
        self.timestep = 0

        self.width = len(matrix)
        self.height = len(matrix[0])
        self.shape = shape

        x = np.linspace(-0.5, 0.5, self.width)
        y = np.linspace(-0.5, 0.5, self.height)

        self.X, self.Y = np.meshgrid(x, y)

    def set_circle(self, circle):
        self.circle = circle

    def next_step(self):
        """ Calculate next state of the string. """

        c = 1
        dt = 0.001
        dx = 1 / 20**2

        # copy current state first
        next_state = np.copy(self.state)

        print("next step!!!!!!!!", self.timestep)

        # iterate over matrix
        for i in range(self.width - 1):
            for j in range(self.height - 1):

                if not self.shape == "Circle" or self.circle[i, j] == 1:

                    if j == 0 and i == 0:
                        next_state[i, j] = ((c * dt)/ dx)** 2\
                            * (self.state[i + 1 % self.width, j] + 0\
                            + 0 + self.state[i, j + 1]\
                            - 4 * self.state[i, j])\
                            + 2 * self.state[i, j] - self.prev_state[i , j]
                    elif i == 0:
                        next_state[i, j] = ((c * dt)/ dx)** 2\
                            * (self.state[i + 1, j] + 0\
                            + self.state[i, j - 1] + self.state[i, j + 1 % self.height]\
                            - 4 * self.state[i, j])\
                            + 2 * self.state[i, j] - self.prev_state[i , j]
                    elif j == 0:
                        next_state[i, j] = ((c * dt)/ dx)** 2\
                            * (self.state[i + 1, j] + self.state[i - 1, j]\
                            + 0 + self.state[i, j + 1 % self.height]\
                            - 4 * self.state[i, j])\
                            + 2 * self.state[i, j] - self.prev_state[i , j]
                    elif i == self.width - 1 and j == self.width - 1:
                        next_state[i, j] = ((c * dt)/ dx)** 2\
                            * (0 + self.state[i - 1, j]\
                            + self.state[i, j - 1] + 0\
                            - 4 * self.state[i, j])\
                            + 2 * self.state[i, j] - self.prev_state[i , j]
                    elif i == self.width - 1:
                        next_state[i, j] = ((c * dt)/ dx)** 2\
                            * (0 + self.state[i - 1, j]\
                            + self.state[i, j - 1] + self.state[i, j + 1]\
                            - 4 * self.state[i, j])\
                            + 2 * self.state[i, j] - self.prev_state[i , j]
                    elif j == self.width - 1:
                        next_state[i, j] = ((c * dt)/ dx)** 2\
                            * (self.state[i + 1, j] + self.state[i - 1, j]\
                            + self.state[i, j - 1] + 0\
                            - 4 * self.state[i, j])\
                            + 2 * self.state[i, j] - self.prev_state[i , j]
                    else:
                        next_state[i, j] = ((c * dt)/ dx)** 2\
                            * (self.state[i + 1, j] + self.state[i - 1, j]\
                            + self.state[i, j - 1] + self.state[i, j + 1]\
                            - 4 * self.state[i, j])\
                            + 2 * self.state[i, j] - self.prev_state[i , j]

        self.prev_state = np.copy(self.state)
        self.state = np.copy(next_state)

        self.timestep += 1
