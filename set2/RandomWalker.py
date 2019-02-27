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
import random

class RandomWalker():
    """ This is a class that contains the RandomWalker aka Monte Carlo simulation."""

    def __init__(self, gridsize):
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

        self.walker_x = random.choice(range(self.width))
        self.walker_y = 0

        # initialize random walker seed with concentration 2 on top of grid
        self.grid[self.walker_y][self.walker_x] = 2

        # initalize object seed at bottom of grid
        self.grid[self.height -1][int(self.width / 2)] = 1


    def next_step_random(self):
        """Compute the next step with the Monte Carlo method. """
        self.step += 1

        self.define_next_walker()
        # out of bound - periodic boundary
        if self.next_walker_x < 0:
            self.next_walker_x = self.width - 1
        elif self.next_walker_x  == self.width:
            self.next_walker_x = 0

        # out of bound
        elif self.next_walker_y < 0 or self.next_walker_y == self.height:
            # new next walker

    def define_next_walker(self):
        # choose direction
        choose = ["left", "right", "up", "down"]
        direction = random.choice(choose)
        print(direction)

        self.next_walker_x = self.walker_x
        self.next_walker_y = self.walker_y

        # decide next step
        if direction is "left":
            self.next_walker_x = self.walker_x - 1
        elif direction is "right":
            self.next_walker_x = self.walker_x + 1
        elif direction is "up":
            self.next_walker_y = self.walker_y + 1
        else:
            self.next_walker_y = self.walker_y - 1



# check if move is possible -- boundary or object
            # # check if there's an object at this grid point
            # if not self.grid[i][j] == 1:
                # check out of bound
                # check periodic boundaries
                # if next_step =

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
