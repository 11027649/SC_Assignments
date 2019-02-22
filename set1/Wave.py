# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This file is part of a program that is used to solve some partial differential
# equations. The program has been developed for the course Scientific Computing
# in the master Computational Science at the UvA february/march 2019.
#
# This part contains the class for a Wave. It contains the three different
# starting positions and the next step function. It also contains some code
# that can be used for plotting the wave at different timesteps.
#
# You can't run this class on its own, but it is used in the vibrating string
# program.
# Romy Meester & Natasja Wezel
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import math

import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np
import copy

class Wave():
    def __init__(self, type, c, dt):
        self.type = type
        self.x = np.linspace(0, 1, 100)
        self.dx = 1/len(self.x)
        self.dt = dt

        self.constant = (c * dt/self.dx)**2

        self.y_previous = []
        self.y_current = []

        self.timeframes = {}
        self.timestep = 0

        self.initialize()

    def initialize(self):
        """ Calculate string in rest state and a previous state. """

        for timestep in self.x:
            self.y_previous.append(self.equation(timestep))
            self.y_current.append(self.equation(timestep))

        self.y_previous[0] = 0
        self.y_current[0] = 0
        self.y_previous[99] = 0
        self.y_current[99] = 0

    def equation(self, x):
        """ Return equation for right assignment. """
        if self.type is "2pi":
            return np.sin(2 * math.pi * x)
        elif self.type is "5pi":
            return np.sin(5 * math.pi * x)
        elif self.type is "5pi_constrained_domain":
            if x > 1/5 and x < 2/5:
                return np.sin(5 * math.pi * x)
            else:
                return 0

    def next_step(self):
        """ Calculate next state of the string. """

        y_next = []
        y_next.append(0)
        for i in range(1, len(self.x) - 1):
            x = self.x[i]

            y = self.constant* (self.y_current[i + 1] + self.y_current[i - 1] - 2 * self.y_current[i])\
                + 2 * self.y_current[i] - self.y_previous[i]

            y_next.append(y)

        y_next.append(0)

        self.y_previous = copy.copy(self.y_current)
        self.y_current = copy.copy(y_next)

        if self.timestep % 10000 is 0:
            self.timeframes[self.timestep] = copy.copy(self.y_current)

        self.timestep += 1


    def plot_time_frames(self):
        """ Make a plot with the wave at different time points. """

        fig = plt.figure()
        plt.grid(True)

        plt.ylim([-1.5,1.5])
        plt.xlim([0,1])

        for key in self.timeframes.keys():
            if key == 0:
                plt.plot(self.x, self.timeframes[key], label="time: " + str(round(key*self.dt, 3)), linewidth=5)
            else:
                plt.plot(self.x, self.timeframes[key], label="time: " + str(round(key*self.dt, 3)))

        plt.title("Wave at different times")
        plt.legend(loc="upper right")
        plt.show()

        fig.savefig('results/pics_wave/vibrating_string_'+ self.type + '.png', dpi=150)
