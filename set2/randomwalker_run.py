import seaborn as sns
sns.set()

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from RandomWalker import RandomWalker
import time
from matplotlib import colors

import matplotlib.ticker as tkr     # has classes for tick-locating and -formatting
import pylab

def main():
    N = 100
    p_stick = [1.0, 1.0, 1.0]
    # p_stick = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]

    # create discrete colormap
    cmap = colors.ListedColormap(['navy', 'white', 'red'])
    bounds = [0,0.5,1.5,2]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    for p in p_stick:
        print("RandomWalker with sticking probability: ", p)
        mc = RandomWalker(N, p)

        # set up figure
        fig, ax = plt.subplots()

        # hide gridlines
        ax.grid(False)
        ax.set_xticks([0,20,40,60,80,99])
        ax.set_yticks([0,20,40,60,80,99])
        ax.set_xlabel("x-coordinate")
        ax.set_ylabel("y-coordinate")

        yfmt = tkr.FuncFormatter(numfmt)    # create your custom formatter function
        pylab.gca().yaxis.set_major_formatter(yfmt)
        pylab.gca().xaxis.set_major_formatter(yfmt)

        while not mc.highest_object == N - 1:
            mc.next_step()

        mc.remove_walker()
        plt.ylabel("y-coordinate")
        plt.xlabel("x-coordinate")

        fig.suptitle("Monte Carlo method\nsteps: " + str(mc.step) + ", p-stick: " + str(p), fontsize='large')
        im = plt.imshow(mc.grid, cmap = cmap, norm =norm, origin='lower', interpolation='nearest')

        plt.savefig("results/randomwalker/mc_pstick_" + str(p) + "_" + str(time.time()) + ".png")

def numfmt(x, pos): # your custom formatter function: divide by 100.0
    s = '{}'.format(x / 100.0)
    if x == 99:
        s = 1.0
    return s


if __name__ == '__main__':
    main()
