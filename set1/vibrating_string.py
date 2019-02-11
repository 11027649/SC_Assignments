import math

import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np
import copy

def main():
    # variables
    c = 1.0
    dt = 0.001

    # global variables needed for animation
    global current_state, fig, ax1

    # initalize wave, pick 2pi, 5pi or 5pi_constrained_domain
    current_state = Wave("2pi", c, dt)

    # initalize figure
    fig = plt.figure()
    fig.set_dpi(100)
    fig.suptitle("Vibrating String")

    ax1 = fig.add_subplot(1,1,1)

    # animate
    anim = animation.FuncAnimation(fig, animate, frames=500, interval=50)
    anim.save('vibrating_string_'+ current_state.type + '.mp4')

    plt.show()


def animate(i):
    """ Calculate next state and set that for the animation. """
    current_state.next_step()
    ax1.clear()
    plt.plot(current_state.x, current_state.y_current, color="Pink")
    plt.grid(True)

    plt.ylim([-1.5,1.5])
    plt.xlim([0,1])


class Wave():
    def __init__(self, type, c, dt):
        self.type = type
        self.x = np.linspace(0, 1, 100)
        self.dx = 1/len(self.x)

        self.constant = (c * dt/self.dx)**2

        self.y_previous = []
        self.y_current = []

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

        self.y_previous = copy.deepcopy(self.y_current)
        self.y_current = copy.deepcopy(y_next)


if __name__ == '__main__':
    main()
