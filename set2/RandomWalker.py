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
    """ This is a class that contains the random walker aka
        the Monte Carlo simulation.
        Grid = 0, Object = 1, Random walker = 2. """

    def __init__(self, gridsize, p_stick):
        self.height = gridsize
        self.width = gridsize

        self.step = 0

        # sticking probability
        self.p_stick = p_stick

        # walker didn't stick on the neighbour of the object
        self.not_neighbour = ()

        self.initialize()

    def initialize(self):
        """" Initalize grid """

        self.grid = np.zeros((self.width, self.height))

        # initalize object seed at bottom of grid
        self.grid[0][int(self.width / 2)] = 1

        # place the walker near the object to speed up the simulation
        self.highest_object = 0

        # initialize first walker
        self.place_walker()

    def place_walker(self):
        """ This is a function that places a new random walker at the top of the
            grid. """

        self.walker_x = random.choice(range(self.width))

        # place walker near the object
        if self.highest_object + 3 <= self.height - 1:
            self.walker_y = self.highest_object + 3
        else:
            self.walker_y = self.height - 1

        # check if there's an object at this grid point
        if self.grid[self.walker_y][self.walker_x] == 1:
            self.place_walker()
        else:
            # initialize random walker on top of grid
            self.grid[self.walker_y][self.walker_x] = 2

    def remove_walker(self):
        """ This is a function that removes the random walker. """

        # if the grid contains a walker at this point, remove it (sanity check)
        if self.grid[self.walker_y][self.walker_x] == 2:
            self.grid[self.walker_y][self.walker_x] = 0

    def get_neighbours(self):
        """ This function defines the neighbours of the random walker. """
        neighbours = []

        # check out of bound (down, up, left, right), and when not, append neighbour
        if not self.walker_y == 0:
            neighbours.append((self.walker_x, self.walker_y - 1))

        if not self.walker_y == self.height - 1:
            neighbours.append((self.walker_x, self.walker_y + 1))

        if not self.walker_x == 0:
            neighbours.append((self.walker_x - 1, self.walker_y))

        if not self.walker_x == self.width - 1:
            neighbours.append((self.walker_x + 1, self.walker_y))

        return neighbours


    def next_step(self):
        """ The next step of the animation. """

        print(self.step, self.highest_object)

        # whether a random walker is added to the object depends on the sticking probability
        added = False
        moved = False

        while not added and not moved:
            # calculate new coordinates
            next_walker_x, next_walker_y = self.next_coordinates()

            # move there (or not)
            moved = self.move(next_walker_x, next_walker_y)

            # check if walker aggregates by checking the neighbours
            neighbours = self.get_neighbours()

            # check neighbours of walker and stick probability
            for neighbour in neighbours:
                # neighbour is an object and probability holds to stick
                if self.grid[neighbour[1]][neighbour[0]] == 1 and np.random.random() <= self.p_stick:
                    # walker becomes part of the object
                    self.grid[self.walker_y][self.walker_x] = 1

                    # update highest object
                    if self.walker_y > self.highest_object:
                        self.highest_object = self.walker_y

                    added = True

                    # place a new walker on the top of the grid
                    self.place_walker()
                    break

        self.step += 1

    def move(self, next_walker_x, next_walker_y):
        """Compute the next step with the Monte Carlo method. """

        # out of bound at top/bottom
        if next_walker_y < 0 or next_walker_y > self.height - 1:
            # remove this walker
            self.remove_walker()
            # place a new walker on the top of the grid
            self.place_walker()
            return True
        # else move walker
        else:
            # out of bound for periodic boundary
            if next_walker_x < 0:
                next_walker_x = self.width - 1
            elif next_walker_x  == self.width:
                next_walker_x = 0

            # if not walking into an object, move there
            if not self.grid[next_walker_y][next_walker_x] == 1:
                # remove at old spot
                self.remove_walker()
                # put at new spot
                self.grid[next_walker_y][next_walker_x] = 2

                # update coordinates
                self.walker_x = next_walker_x
                self.walker_y = next_walker_y
                return True
            # if next position is object, stay where you are
            else:
                return False

    def next_coordinates(self):
        """ Calculate next coordinates for the walker. """

        # choose direction
        choose = ["left", "right", "up", "down"]
        direction = random.choice(choose)

        next_walker_x = self.walker_x
        next_walker_y = self.walker_y

        # make next step
        if direction is "left":
            next_walker_x = self.walker_x - 1
        elif direction is "right":
            next_walker_x = self.walker_x + 1
        elif direction is "up":
            next_walker_y = self.walker_y + 1
        else:
            next_walker_y = self.walker_y - 1

        return next_walker_x, next_walker_y
