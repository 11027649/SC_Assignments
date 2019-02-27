# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This file is part of a program that is used to solve some partial differential
# equations. The program has been developed for the course Scientific Computing
# in the master Computational Science at the UvA february/march 2019.
#
# This part contains the code for the diffusion grid. It's most important
# properties are it's width and height (the diffusion grid is always a square)
# and the diffusion constant. It contains code for all the different methods that
# are used to solve the diffusion equation, including the analytic method.
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

# from numba import jitclass

import seaborn as sns
sns.set()

from matplotlib import colors

class DiffusionGrid():
    """ This is a class that contains the diffusion coefficient and dimensions for
        the diffusion grid. It also contains the diffusion grid itself."""

    def __init__(self, gridsize, eta):
        self.height = gridsize
        self.width = gridsize
        self.eta = eta

        self.step = 0

        self.saved_states = {}

        self.reached_boundaries = False
        self.candidates = []

        self.initialize()

    def initialize(self):
        """" Initalize grid """
        self.grid = [[0 for col in range(self.width)] for row in range(self.height)]

        self.object_grid = [[0 for col in range(self.width)] for row in range(self.height)]

        # initialize top with concentration 1
        for i in range(0, self.width):
            self.grid[0][i] = 1

        # initalize object_grid with a seed
        self.object_grid[self.height -1][int(self.width / 2)] = 1

        # initialize candidate list
        self.candidates.extend([(int(self.width / 2), self.height - 2),\
                                (int(self.width / 2) - 1, self.height - 1),\
                                (int(self.width / 2) + 1, self.height - 1)])

    def set_omega(self, w):
        """ Set the weight of omega for the SOR diffusion method. """
        self.w = w

    def next_step(self):
        """ Compute concentration in each grid point according to the right
            method. """

        # call next step for right method
        self.next_step_sor()

        self.step += 1

    def next_step_sor(self):
        """ Compute concentration in each grid point with the succesive over
            relaxation method. This method converges only if the weight is between
            zero and two. For weight smaller then 1, the method is called under
            relaxation. For w = 1 we recover the Gauss-Seidel iteration.
            The updates can be performed in place. """

        # biggest difference that can happen is 1
        max_delta = 0

        # iterate over grid, first row is always concentration 1, last row always 0
        for i in range(1, self.height - 1):
            # iterate over columns, first and last are periodic boundaries
            for j in range(self.width):
                previous = self.grid[i][j]

                # check if there's an object at this grid point
                if not self.object_grid[i][j] == 1:
                    if j == 0:
                        self.grid[i][j] = self.w/4 *\
                                            (self.grid[i + 1][j]\
                                            + self.grid[i - 1][j]\
                                            + self.grid[i][j + 1]\
                                            + self.grid[i][self.width - 1])\
                                            + (1 - self.w) * self.grid[i][j]
                    elif j == self.width - 1:
                        self.grid[i][j] = self.w/4 *\
                                            (self.grid[i + 1][j]\
                                            + self.grid[i - 1][j]\
                                            + self.grid[i][0]\
                                            + self.grid[i][j - 1])\
                                            + (1 - self.w) * self.grid[i][j]
                    else:
                        self.grid[i][j] = self.w/4 *\
                                            (self.grid[i + 1][j]\
                                            + self.grid[i - 1][j]\
                                            + self.grid[i][j + 1]\
                                            + self.grid[i][j - 1])\
                                            + (1 - self.w) * self.grid[i][j]

        # calculate total concentration of candidates
        denominator = self.candidates_concentration()

        for coord in self.candidates:
            x = coord[0]
            y = coord[1]

            concentration = self.grid[y][x]

            # check if it aggregates
            if not denominator == 0 and np.random.random() <= concentration**self.eta/denominator:
                # add to object
                self.object_grid[y][x] = 1
                # remove from candidates
                self.candidates.remove(coord)

                # add new candidates if not at boundaries and if not already in there
                new_candidates = [(x + 1,y),(x - 1, y),(x, y + 1),(x, y - 1)]
                for new_coord in new_candidates:
                    if not new_coord in self.candidates\
                            and new_coord[0] <= self.width - 1\
                            and new_coord[0] >= 0\
                            and new_coord[1] <= self.height -1\
                            and new_coord[1] >= 0:

                        self.candidates.append(new_coord)

        # check if diffusion has reached boundaries
        self.check_boundaries()

    def next_step_MC(self):
        """Compute the next step with the Monte Carlo method. """
        #NEXT STEP
        for i in range(self.height):
            for j in range(self.width):
                return self.grid[i][j]
        #SOR AANPASSEN ZONDER SINK EN SOURCE?

        # calculate total concentration of candidates
        denominator = self.candidates_concentration()
        print(denominator)
        for coord in self.candidates:
            x = coord[0]
            y = coord[1]

            concentration = self.grid[x][y]

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

    def candidates_concentration(self):
        """ Calculates total concentration of all candidates together. """

        concentration = 0

        for coord in self.candidates:
            concentration = concentration + self.grid[coord[1]][coord[0]] ** self.eta

        return concentration

    def plot_time_frames(self):
        """ Plot the state of the diffusion at different time steps. """

        fig = plt.figure()
        fig.suptitle("Diffusion for: " + self.method + " method")

        for i,key in enumerate(self.saved_states.keys()):
            if len(self.saved_states.keys()) > 1:
                plt.subplot(2,3,i + 1)
            plt.title("t = " + str(key))
            im = plt.imshow(self.saved_states[key].grid, norm=colors.Normalize(vmin=0,vmax=1), interpolation='bicubic')
            plt.xticks([])
            plt.yticks([])

        # TODO fix colorbar
        plt.colorbar()
        plt.show()
        fig.savefig('results/timepoints'+ self.method + "_" + str(time.time()) + '.png', dpi=150)
