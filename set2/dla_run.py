import seaborn as sns
sns.set()

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from DiffusionGrid import DiffusionGrid
import time
from matplotlib import colors
import matplotlib.ticker as tkr     # has classes for tick-locating and -formatting
import pylab

def main():
    N = 100
    # eta<1, compact objects, eta = 0 Eden Cluster, =1 normal DLA cluster
    # eta > 1 more open cluster
    etas = [0.5, 1.0, 1.5]

    # best omega from previous assignment
    omega = 1.95
    for eta in etas:
        dla = DiffusionGrid(N, eta)
        dla.set_omega(omega)

        while not dla.reached_boundaries:
            dla.next_step()

        t = time.time()

        cmap = colors.ListedColormap(['navy', 'white', 'red'])
        bounds = [0,0.5,1.5,2]
        norm = colors.BoundaryNorm(bounds, cmap.N)

        # set up figure
        fig, ax = plt.subplots()
        fig.suptitle("Diffusion limited aggregation\nsteps: " + str(dla.step) + ", eta: " + str(eta), fontsize='large')
        plt.imshow(dla.object_grid, cmap = cmap, norm =norm, origin='lower')

        ax.grid(False)
        ax.set_xticks([0,20,40,60,80,100])
        ax.set_yticks([0,20,40,60,80,100])
        ax.set_xlabel("x-coordinate")
        ax.set_ylabel("y-coordinate")

        yfmt = tkr.FuncFormatter(numfmt)    # create your custom formatter function
        pylab.gca().yaxis.set_major_formatter(yfmt)
        pylab.gca().xaxis.set_major_formatter(yfmt)

        plt.savefig("results/diffusion/diff_" + str(t) + "_object_eta_" + str(eta) + ".png", dpi=150)
        # plt.show()

        fig, ax = plt.subplots()
        fig.suptitle("Diffusion limited aggregation\nsteps: " + str(dla.step) + ", eta: " +str(eta), fontsize='large')
        plt.imshow(dla.grid, origin='lower', interpolation='bicubic')
        plt.colorbar()
        ax.grid(False)
        ax.set_xticks([0,20,40,60,80,100])
        ax.set_yticks([0,20,40,60,80,100])
        ax.set_xlabel("x-coordinate")
        ax.set_ylabel("y-coordinate")

        yfmt = tkr.FuncFormatter(numfmt)    # create your custom formatter function
        pylab.gca().yaxis.set_major_formatter(yfmt)
        pylab.gca().xaxis.set_major_formatter(yfmt)
        plt.savefig("results/diffusion/diff_" + str(t) + "_eta_" + str(eta) + ".png", dpi=150)
        # plt.show()


def numfmt(x, pos): # your custom formatter function: divide by 100.0
    s = '{}'.format(x / 100.0)
    return s

if __name__ == '__main__':
    main()
