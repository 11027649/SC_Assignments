import numpy as np
import math
import pandas
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy

class DiffusionGrid():
    """ This is a class that contains the diffusion coefficient and dimensions for
        the diffusion grid. It also contains the diffusion grid itself."""

    def __init__(self, height, width, D, dt, dx, method):
        self.height = height
        self.width = width
        self.D = D
        self.dt = dt
        self.dx = dx

        self.method = method

        self.initialize()

    def initialize(self):
        """" Initalize grid """
        self.grid = [[0 for col in range(self.width)] for row in range(self.height)]

        # initialize top with concentration 1
        for i in range(0, self.width):
            self.grid[0][i] = 1

    def next_step(self):
        """ Compute concentration in each grid point. """

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

    def next_step_gauss_seidel(self):
        """ Compute concentration in each grid point. """

        current_state = self.grid
        next_state = copy.copy(self.grid)

        # iterate over grid, first row is always concentration 1, last row always 0
        for i in range(1, self.height - 1):
            # iterate over columsn, first and last are periodic boundaries
            for j in range(1, self.width - 1):


            # copy for periodic boundaries
            next_state[i][0] = next_state[i][self.width - 2]
            next_state[i][self.width - 1] = next_state[i][1]

        self.grid = copy.copy(next_state)
