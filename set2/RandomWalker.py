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

    def __init__(self, gridsize):
        self.height = gridsize
        self.width = gridsize

        self.step = 0

        self.initialize()

    def initialize(self):
        """" Initalize grid """
        self.grid = [[0 for col in range(self.width)] for row in range(self.height)]

        # initalize object seed at bottom of grid
        self.grid[self.height - 1][int(self.width / 2)] = 1

        # KLADD
        for i in range(10,int(self.width /2)):
            for j in range(10, int(self.height /2)):
                self.grid[j][i] = 1

        # initialize first walker
        self.place_walker()

    def place_walker(self):
        """ This is a function that places a new random walker at the top of the
            grid. """
            #TO DO check: # check if there's an object at this grid point -- bug?

        print(self.step, "placing a walker")

        self.walker_x = random.choice(range(self.width))
        self.walker_y = 0

        # check if there's an object at this grid point
        if self.grid[self.walker_y][self.walker_x] == 1:
            self.place_walker()

        # initialize random walker seed with concentration 2 on top of grid
        self.grid[self.walker_y][self.walker_x] = 2


    def remove_walker(self):
        """ This is a function that removes the random walker. """

        self.grid[self.walker_y][self.walker_x] = 0

    def define_neighbours(self):
        """ This function defines the neighbours of the random walker. """
        self.neighbours = []

        # check out of bound (down, up, left, right), and when not, append neighbour
        #MAAR DE HOEKPUNTEN KLOPPEN ZO VOLGENS MIJ HIER OOK WEER NIET...
        if not self.walker_y < 0:  #down
            self.neighbours.append(self.grid[self.walker_y - 1][self.walker_x])
        elif not self.walker_y == self.height: #up
            self.neighbours.append(self.grid[self.walker_y + 1][self.walker_x])
        elif not self.walker_x < 0: #left
            self.neighbours.append(self.grid[self.walker_y][self.walker_x - 1])
        elif not self.walker_x == self.width: #right
            self.neighbours.append(self.grid[self.walker_y][self.walker_x + 1])

    def next_step(self):
        """ The next step of the animation. """
        #To Do: append statement to only create a next step when the
        # random walker has been added to the object. --
        # HAS BEEN ADDED IN COMMENTS

        # calculate new coordinates
        self.next_coordinates()
        # move there (or not)
        self.move()

        # check if walker aggregates by checking the neighbours
        self.define_neighbours()
        for neighbour in self.neighbours:
            if neighbour == 1:
                # walker becomes part of the object
                self.grid[self.walker_y][self.walker_x] == 1

                # remove this walker
                self.remove_walker()
                # place a new walker on the top of the grid
                self.place_walker()

                # next step of the animation when random walker is aggregated
                # self.step += 1

        self.step += 1

    def move(self):
        """Compute the next step with the Monte Carlo method. """

        print(self.next_walker_x, self.next_walker_y)

        # out of bound at top/bottom
        if self.next_walker_y < 0 or self.next_walker_y == self.height:
            print("removing: " , self.grid[self.walker_y][self.walker_x])
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
