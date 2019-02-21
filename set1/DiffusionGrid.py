import numpy as np
import math
import pandas
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy
import time

import seaborn as sns
sns.set()

from matplotlib import colors

class DiffusionGrid():
    """ This is a class that contains the diffusion coefficient and dimensions for
        the diffusion grid. It also contains the diffusion grid itself."""

    def __init__(self, height, width, D, method):
        self.height = height
        self.width = width
        self.D = D

        self.dx = 1/self.width
        self.time = 0

        self.saved_states = {}
        self.method = method

        # this is needed for the time independent methods
        self.converged = False
        self.convergence = []

        self.initialize()

    def initialize(self):
        """" Initalize grid """
        self.grid = [[0 for col in range(self.width)] for row in range(self.height)]

        # initialize top with concentration 1
        for i in range(0, self.width):
            self.grid[0][i] = 1

        self.object_grid = [[0 for col in range(self.width)] for row in range(self.height)]

    def set_omega(self, w):
        """ Set the weight of omega for the SOR diffusion method. """
        self.w = w

    def set_time(self, dt, timesteps):
        """ Set the time settings for Time Dependent Diffusion. """

        self.dt = dt
        self.timesteps = timesteps

        # save grid at right times for plots later
        # the other methods are time independent so we don't want to save these timesteps
        self.save_times = [0, 10, 100, 1000, 10000]

    def next_step(self):
        """ Compute concentration in each grid point according to the right
            method. """

        # call next step for right method
        if self.method is "Time_Dependent":

            # save info for plots
            if self.time in self.save_times:
                self.saved_states[self.time/10000] =  copy.deepcopy(self)

            self.next_step_time_dependent()
        elif self.method is "Jacobi":
            self.next_step_jacobi()
        elif self.method is "Gauss_Seidel":
            self.next_step_gauss_seidel()
        else:
            self.next_step_sor()

        self.time += 1

        if self.converged and not self.method == "Time_Dependent":
            # use time as amount of steps
            self.saved_states[self.time/10000] = copy.deepcopy(self)

            # calculate y
            y = [np.sum(row) for row in self.grid]
            y = [x/50 for x in y]

            # reverse list for proper plotting
            y.reverse()
            self.dependence_on_y = y


    def next_step_time_dependent(self):
        """ Compute concentration in each grid point, according to the time dependent
            discretized partial differential equation. """

        current_state = self.grid
        next_state = copy.copy(self.grid)

        # iterate over grid, first row is always concentration 1, last row always 0
        for i in range(1, self.height - 1):
            # iterate over columsn, first and last are periodic boundaries
            for j in range(self.width):
                if j == 0:
                    next_state[i][j] = current_state[i][j]\
                                        + (self.dt * self.D)/self.dx**2 * (current_state[i + 1][j]\
                                        + current_state[i - 1][j]\
                                        + current_state[i][j + 1]\
                                        + current_state[i][self.width - 1]\
                                        - 4 * current_state[i][j])
                elif j == self.width - 1:
                    next_state[i][j] = current_state[i][j]\
                                        + (self.dt * self.D)/self.dx**2 * (current_state[i + 1][j]\
                                        + current_state[i - 1][j]\
                                        + current_state[i][0]\
                                        + current_state[i][j - 1]\
                                        - 4 * current_state[i][j])
                else:
                    next_state[i][j] = current_state[i][j]\
                                        + (self.dt * self.D)/self.dx**2 * (current_state[i + 1][j]\
                                        + current_state[i - 1][j]\
                                        + current_state[i][j + 1]\
                                        + current_state[i][j - 1]\
                                        - 4 * current_state[i][j])

        self.grid = copy.copy(next_state)

    def next_step_jacobi(self):
        """ Compute concentration in each grid point with the Jacobi method. """

        current_state = self.grid
        next_state = copy.deepcopy(self.grid)
        # the biggest difference that can happen is 1
        max_delta = 0
        # iterate over grid, first row is always concentration 1, last row always 0
        for i in range(1, self.height - 1):
            # iterate over columsn, first and last are periodic boundaries
            for j in range(self.width):
                if j == 0:
                    next_state[i][j] = 1/4 * (current_state[i + 1][j]\
                                        + current_state[i - 1][j]\
                                        + current_state[i][j + 1]\
                                        + current_state[i][self.width - 1])
                elif j == self.width - 1:
                    next_state[i][j] = 1/4 * (current_state[i + 1][j]\
                                        + current_state[i - 1][j]\
                                        + current_state[i][0]\
                                        + current_state[i][j - 1])
                else:
                    next_state[i][j] = 1/4 * (current_state[i + 1][j]\
                                        + current_state[i - 1][j]\
                                        + current_state[i][j + 1]\
                                        + current_state[i][j - 1])

                delta = next_state[i][j] - current_state[i][j]

                if delta > max_delta:
                    max_delta = delta

        self.grid = copy.deepcopy(next_state)

        self.convergence.append(max_delta)
        # if biggest difference is smaller then epsiolon (given in assignment, it's converged)
        if max_delta < 10**-5:
            self.converged = True

    def next_step_gauss_seidel(self):
        """ Compute concentration in each grid point with the gauss seidel method.
            This is a cool method because we can update the grid in place. """

        # biggest difference that can happen is 1
        max_delta = 0

        # iterate over grid, first row is always concentration 1, last row always 0
        for i in range(1, self.height - 1):
            # iterate over columsn, first and last are periodic boundaries
            for j in range(self.width):
                # save for calculation of delta
                previous = self.grid[i][j]

                if j == 0:
                    self.grid[i][j] = 1/4 *\
                                        (self.grid[i + 1][j]\
                                        + self.grid[i - 1][j]\
                                        + self.grid[i][j + 1]\
                                        + self.grid[i][self.width - 1])
                elif j == self.width - 1:
                    self.grid[i][j] = 1/4 *\
                                        (self.grid[i + 1][j]\
                                        + self.grid[i - 1][j]\
                                        + self.grid[i][0]\
                                        + self.grid[i][j - 1])
                else:
                    self.grid[i][j] = 1/4 *\
                                        (self.grid[i + 1][j]\
                                        + self.grid[i - 1][j]\
                                        + self.grid[i][j + 1]\
                                        + self.grid[i][j - 1])

                delta = self.grid[i][j] - previous

                if delta > max_delta:
                    max_delta = delta

        self.convergence.append(max_delta)

        if max_delta < 10**-5:
            self.converged = True

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

                delta = abs(self.grid[i][j] - previous)

                if delta > max_delta:
                    max_delta = delta

        self.convergence.append(max_delta)

        if max_delta < 10**-5:
            self.converged = True

    def plot_time_frames(self):
        """ Plot the state of the diffusion at different time steps. """

        fig = plt.figure()
        fig.suptitle("Diffusion for: " + self.method + " method")

        for i,key in enumerate(self.saved_states.keys()):
            if len(self.saved_states.keys()) > 1:
                plt.subplot(1,6,i + 1)
            plt.title("t = " + str(key))
            im = plt.imshow(self.saved_states[key].grid, norm=colors.Normalize(vmin=0,vmax=1), interpolation='bicubic')
            plt.xticks([])
            plt.yticks([])

        # TODO fix colorbar
        # plt.subplot(1,6, 6)
        # plt.colorbar()
        plt.show()
        fig.savefig('results/timepoints'+ self.method + "_" + str(time.time()) + '.png', dpi=150)

    def analytic_solution(self):
        """ This function contains a function to calculate the analytic solution
            for the diffusion equation. """

        # what is this M lol
        M = 10
        x = np.linspace(0.,1.,self.width)

        self.analytic_solutions = {}
        for t in self.save_times:
            t = t/10000
            if not t == 0:
                # make a list with zeros
                y = [0]*len(x)

                for j,xj in enumerate(x):
                    for i in range(0,M):
                        # add each time
                        y[j] += math.erfc((1-xj+2*i)/(2*np.sqrt(self.D*t))) - math.erfc((1+xj+2*i)/(2*np.sqrt(self.D*t)))

                self.analytic_solutions[t] = copy.copy(y)

    def compare_to_analytic_solution(self):
        """ Compares the diffusion solution of the numerical and analytic solutions. """

        self.analytic_solution()
        x = np.linspace(0.,1.,self.width)

        fig = plt.figure()
        plt.grid(True)

        for key in self.analytic_solutions.keys():
            plt.plot(x, self.analytic_solutions[key], label=key)

        for key in self.saved_states.keys():
            if not key == 0:
                grid = self.saved_states[key].grid
                # calculate y
                y = [np.sum(row) for row in grid]
                y = [x/50 for x in y]

                # reverse list for proper plotting
                y.reverse()
                self.dependence_on_y = y

                plt.plot(x,y, label=self.method + " " + str(key))

        plt.legend()
        plt.title("Comparison of solutions")
        plt.ylabel("Concentration (y)")
        plt.xlabel("y")

        fig.savefig('results/analytic_vs_'+ self.method + '.png', dpi=150)

    def add_object(self, pos, lenx, leny):
        """ Add objects at the position you want. Can be called several times
            for multiple objects.
            The type can be sink or source. """

        for j in range(pos[1], pos[1] + leny):
            for i in range(pos[0], pos[0] + lenx):
                self.object_grid[j][i] = 1
