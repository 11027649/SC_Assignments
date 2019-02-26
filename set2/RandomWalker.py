# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This file is part of a program that is used to solve some partial differential
# equations. The program has been developed for the course Scientific Computing
# in the master Computational Science at the UvA february/march 2019.
#
# BLAHBLAHBLAH
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

class RandomWalker():
    """ This is a class that contains the RandomWalker aka Monte Carlo simulation."""

    def __init__(self, gridsize, eta):
        self.height = gridsize
        self.width = gridsize

        self.step = 0

        self.saved_states = {}

        self.reached_boundaries = False
        self.candidates = []

        self.initialize()

    def initialize(self):
        """" Initalize grid """
        self.grid = [[0 for col in range(self.width)] for row in range(self.height)]

        self.object_grid = [[0 for col in range(self.width)] for row in range(self.height)]

        # initialize random walker seed with concentration 2 on top of grid
        for i in range(0, self.width):
            self.grid[0][random.random(i, self.width)] = 2

        # initalize object_grid with a seed
        self.object_grid[self.height -1][int(self.width / 2)] = 1

        # initialize candidate list
        self.candidates.extend([(int(self.width / 2), self.height - 2),\
                                (int(self.width / 2) - 1, self.height - 1),\
                                (int(self.width / 2) + 1, self.height - 1)])

    def next_step(self):
        """ Compute concentration in each grid point according to the right
            method. """

        # call next step for right method
        self.next_step_random()

        self.step += 1

    def next_step_random(self):
        """Compute the next step with the Monte Carlo method. """

        # choose direction
        choose = ["left", "right", "up", "down"]
        direction = random.choice(choose)
        print(direction)

        # iterate over grid, first row is always concentration 1
        for i in range(self.height - 1):
            for j in range(self.width):

                # check if there's an object at this grid point
                if not self.object_grid[i][j] == 1:
                    if direction is "left":
                        next_step = self.grid[i-1][j]
                    elif direction is "right":
                        next_step = self.grid[i+1][j]
                    elif direction is "up":
                        next_step = self.grid[i][j+1]
                    else:
                        next_step = self.grid[i][j-1]

            # # check if it aggregates
            # if #check whether its a neighbour
            #     # add to objects
            #     self.object_grid[x][y] = 1
            #
            #     # remove from candidates
            #     self.candidates.remove(coord)
            # elif #check out of bound: same as self.check_boundaries():??

    def check_boundaries(self):
        """ A method to check if the diffusion has reached the boundaries of the
            grid. """

        for i in range(self.width):
            if not self.grid[0][i] == 0 or not self.grid[i][0] == 0 or not\
                    self.grid[self.width - 1][i] == 0 or not self.grid[i][self.width - 1] == 0:

                self.reached_boundaries = True
