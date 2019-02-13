import numpy as np
import math
import pandas
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy

class DiffusionGrid():
    """ This is a class that contains the diffusion coefficient and dimensions for
        the diffusion grid. It also contains the diffusion grid itself."""

    def __init__(self, height, width, D, dt, timesteps, method):
        self.height = height
        self.width = width
        self.D = D
        self.dt = dt
        self.dx = 1/self.width

        # save grid at right times for plots later
        self.timesteps = timesteps
        self.time = 0
        self.save_times = [0, 10, 100, 1000, 10000]
        self.saved_states = []

        # weight for SOR between 0 and 2
        self.w = 1

        self.method = method

        self.initialize()

    def initialize(self):
        """" Initalize grid """
        self.grid = [[0 for col in range(self.width)] for row in range(self.height)]

        # initialize top with concentration 1
        for i in range(0, self.width):
            self.grid[0][i] = 1

    def next_step(self):
        """ Compute concentration in each grid point according to the right
            method. """

        # save info for plots
        if self.time in self.save_times:
            self.saved_states.append(copy.copy(self))

        # call next step for right method
        if self.method is "Time_Dependent":
            self.next_step_time_dependent()
        elif self.method is "Gauss_Seidel":
            self.next_step_gauss_seidel()
        elif self.method is "Jacobi":
            self.next_step_jacobi()
        else:
            self.next_step_sor()

        self.time += 1




    def next_step_time_dependent(self):
        """ Compute concentration in each grid point, according to the time dependent
            discretized partial differential equation. """

        current_state = self.grid
        next_state = copy.copy(self.grid)

        # iterate over grid, first row is always concentration 1, last row always 0
        for i in range(1, self.height - 1):
            # iterate over columsn, first and last are periodic boundaries
            for j in range(1, self.width - 1):
                next_state[i][j] = current_state[i][j]\
                                    + (self.dt * self.D)/self.dx**2 * (current_state[i+1][j]\
                                    + current_state[i - 1][j]\
                                    + current_state[i][j + 1]\
                                    + current_state[i][j - 1]\
                                    - 4 * current_state[i][j])

            # copy for periodic boundaries
            next_state[i][0] = next_state[i][self.width - 2]
            next_state[i][self.width - 1] = next_state[i][1]

        self.grid = copy.copy(next_state)

    def next_step_jacobi(self):
        """ Compute concentration in each grid point with the Jacobi method. """

        current_state = self.grid
        next_state = copy.copy(self.grid)

        # iterate over grid, first row is always concentration 1, last row always 0
        for i in range(1, self.height - 1):
            # iterate over columsn, first and last are periodic boundaries
            for j in range(1, self.width - 1):
                next_state[i][j] = 1./4 * (current_state[i+1][j]\
                                    + current_state[i-1][j]\
                                    + current_state[i][j+1]\
                                    + current_state[i][j-1])

            # copy for periodic boundaries
            next_state[i][0] = next_state[i][self.width - 2]
            next_state[i][self.width - 1] = next_state[i][1]

        self.grid = copy.copy(next_state)

    def next_step_gauss_seidel(self):
        """ Compute concentration in each grid point with the gauss seidel method.
            This is a cool method because we can update the grid in place. """

        # iterate over grid, first row is always concentration 1, last row always 0
        for i in range(1, self.height - 1):
            # iterate over columsn, first and last are periodic boundaries
            for j in range(1, self.width - 1):
                self.grid[i][j] = 1/4 *\
                                    (self.grid[i + 1][j]\
                                    + self.grid[i - 1][j]\
                                    + self.grid[i][j + 1]\
                                    + self.grid[i][j - 1])

            # copy for periodic boundaries
            self.grid[i][0] = self.grid[i][self.width - 2]
            self.grid[i][self.width - 1] = self.grid[i][1]

    def next_step_sor(self):
        """ Compute concentration in each grid point with the succesive over
            relaxation method. This method converges only if the weight is between
            zero and two. For weight smaller then 1, the method is called under
            relaxation. For w = 1 we recover the Gauss-Seidel iteration. """

        current_state = self.grid
        next_state = copy.copy(self.grid)

        # iterate over grid, first row is always concentration 1, last row always 0
        for i in range(1, self.height - 1):
            # iterate over columsn, first and last are periodic boundaries
            for j in range(1, self.width - 1):
                next_state[i][j] = self.w/4 *\
                                    (current_state[i + 1][j]\
                                    + next_state[i - 1][j]\
                                    + current_state[i][j + 1]\
                                    + next_state[i][j - 1])\
                                    + (1 - self.w) * current_state[i][j]

            # copy for periodic boundaries
            next_state[i][0] = next_state[i][self.width - 2]
            next_state[i][self.width - 1] = next_state[i][1]

        self.grid = copy.copy(next_state)
