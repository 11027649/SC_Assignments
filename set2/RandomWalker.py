# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This file is part of a program that is used to solve some partial differential
# equations. The program has been developed for the course Scientific Computing
# in the master Computational Science at the UvA february/march 2019.
#
# BLAHBLAHBLAH - Nice
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

        # initalize object seed at bottom of grid
        self.grid[self.height - 1][int(self.width / 2)] = 1

        # initialize first walker
        self.place_walker()

    def place_walker(self):
        """ This is a function that places a new random walker at the top of the
            grid.
            TODO: check if there's not already an object there. """

        print(self.step, "placing a walker")

        self.walker_x = random.choice(range(self.width))
        self.walker_y = 0

        # initialize random walker seed with concentration 2 on top of grid
        self.grid[self.walker_y][self.walker_x] = 2

    def remove_walker(self):
        """ This is a function that removes the random walker. """

        self.grid[self.walker_y][self.walker_x] = 0


    def next_step(self):
        # calculate new coordinates
        self.next_coordinates()
        # move there (or not)
        self.move()

        # check
        # # check if it aggregates
        # if #check whether its a neighbour
        #     # add to objects
        #     self.object_grid[x][y] = 1
        #
        #     # remove from candidates
        #     self.candidates.remove(coord)
        # elif #check out of bound: same as self.check_boundaries():??

        self.step += 1

    def move(self):
        """Compute the next step with the Monte Carlo method. """

        print(self.next_walker_x, self.next_walker_y)

        # out of bound top/bottom
        if self.next_walker_y < 0 or self.next_walker_y == self.height:
            print("removing: " , self.grid[self.walker_y][self.walker_x])
            # remove this walker
            self.remove_walker()
            # place a new walker on the top of the grid
            self.place_walker()
        # else move walker
        else:
            # out of bound - periodic boundary
            if self.next_walker_x < 0:
                self.next_walker_x = self.width - 1
            elif self.next_walker_x  == self.width:
                self.next_walker_x = 0

            # remove at old spot
            self.remove_walker()
            # put at new spot
            self.grid[self.next_walker_y][self.next_walker_x] = 2

            # update coordinates
            self.walker_x = self.next_walker_x
            self.walker_y = self.next_walker_y

    def next_coordinates(self):
        """ Calculate next coordinates for the walker. """

        # choose direction
        choose = ["left", "right", "up", "down"]
        direction = random.choice(choose)

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
