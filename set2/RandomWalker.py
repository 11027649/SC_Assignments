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
        self.not_sticked = False

        self.initialize()

    def initialize(self):
        """" Initalize grid """
        self.grid = [[0 for col in range(self.width)] for row in range(self.height)]

        # initalize object seed at bottom of grid
        self.grid[self.height - 1][int(self.width / 2)] = 1

        # place the walker near the object to speed up the simulation
        self.highest_object = self.height - 1

        # initialize first walker
        self.place_walker()

    def place_walker(self):
        """ This is a function that places a new random walker at the top of the
            grid. """

        self.walker_x = random.choice(range(self.width))

        # place walker near the object
        if self.highest_object - 5 >= 0:
            self.walker_y = self.highest_object - 5
        else:
            self.walker_y = 0

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

    def define_neighbours(self):
        """ This function defines the neighbours of the random walker. """
        self.neighbours = []

        # check out of bound (down, up, left, right), and when not, append neighbour
        if not self.walker_y == 0:
            self.neighbours.append((self.walker_x, self.walker_y - 1))

        if not self.walker_y == self.height - 1:
            self.neighbours.append((self.walker_x, self.walker_y + 1))

        if not self.walker_x == 0:
            self.neighbours.append((self.walker_x - 1, self.walker_y))

        if not self.walker_x == self.width - 1:
            self.neighbours.append((self.walker_x + 1, self.walker_y))

    def next_step(self):
        """ The next step of the animation. """
        #To Do: append statement to only create a next step when the
        # random walker has been added to the object. --

        # whether a random walker is added to the object
        # depends on the sticking probability
        self.added = False

        while not self.added:
            # calculate new coordinates
            self.next_coordinates()
            # move there (or not)
            self.move()

            # check if walker aggregates by checking the neighbours
            self.define_neighbours()

            # check neighbours of walker and stick probability
            for neighbour in self.neighbours:
                # neighbour is an object and probability holds to stick
                if self.grid[neighbour[1]][neighbour[0]] == 1 and np.random.random() <= self.p_stick:
                    print('PART OF OBJECT')
                    # walker becomes part of the object
                    self.grid[self.walker_y][self.walker_x] = 1

                    # update highest object
                    if self.walker_y < self.highest_object:
                        self.highest_object = self.walker_y

                    self.added = True
                    self.not_sticked = False

                    # place a new walker on the top of the grid
                    self.place_walker()
                    break

                # neighbour is an object but probability doesn't hold to stick
                elif self.grid[neighbour[1]][neighbour[0]] == 1:
                    self.not_neighbour = neighbour
                    self.not_sticked = True
                    # print(self.not_neighbour)
                    print('NOT PART OF OBJECT')
                    self.next_step()


        self.step += 1

    def move(self):
        """Compute the next step with the Monte Carlo method. """

        # out of bound at top/bottom
        if self.next_walker_y < 0 or self.next_walker_y == self.height - 1:
            # remove this walker
            self.remove_walker()
            # place a new walker on the top of the grid
            self.place_walker()
        # else move walker
        else:
            # out of bound for periodic boundary
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
        # TO do: check that the random walker doesnt go to the no neighbour
        # and remove the no_neighbour after the walker has moved!

        # choose direction
        choose = ["left", "right", "up", "down"]
        direction = random.choice(choose)

        self.next_walker_x = self.walker_x
        self.next_walker_y = self.walker_y

        # make next step
        if direction is "left":
            self.next_walker_x = self.walker_x - 1
        elif direction is "right":
            self.next_walker_x = self.walker_x + 1
        elif direction is "up":
            self.next_walker_y = self.walker_y + 1
        else:
            self.next_walker_y = self.walker_y - 1


        # check if the random walker doesn't go to the no_neighbour of the object
        if self.not_sticked:
            print(self.not_neighbour, self.next_walker_x, self.next_walker_y)
            # print(self.not_neighbour[1], self.next_walker_x)

# HIER ZIT DE BUG!
            if self.not_neighbour[0] == self.next_walker_x and self.not_neighbour[1] == self.next_walker_y:
                print('coordinates', self.next_walker_x, self.next_walker_y)
                self.next_coordinates()
