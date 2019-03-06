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
    etas = [1.5, 2.0]

    # best omega from previous assignment
    omega = 1.95

    for eta in etas:
        print("eta:", eta)

        dla = DiffusionGrid(N, eta)
        dla.set_omega(omega)

        while dla.object_size <= 200:
            # if dla.object_size % 25 == 0:
            #     np.savetxt("results/diffusion/object_" + str(dla.object_size) + "_step_" + str(dla.step) + ".txt", dla.object_grid)

            dla.next_step()

        t = time.time()

        fig, ax = plt.subplots()
        fig.suptitle("Diffusion limited aggregation\nsteps: " + str(dla.step) + ", eta: " +str(eta), fontsize='large')

        plt.imshow(dla.grid, origin='lower', interpolation='bicubic')
        plt.colorbar()

        ax.grid(False)
        ax.set_xticks([0,20,40,60,80,100])
        ax.set_yticks([0,20,40,60,80,100])
        ax.set_xlabel("x-coordinate")
        ax.set_ylabel("y-coordinate")
        ax.set_xlim(0,100)
        ax.set_ylim(0,100)

        for y, row in enumerate(dla.object_grid):
            for x, object in enumerate(row):
                if object == 1:
                    plt.scatter(x, y, s=5, color='white', marker="s")

        yfmt = tkr.FuncFormatter(numfmt)    # create your custom formatter function
        pylab.gca().yaxis.set_major_formatter(yfmt)
        pylab.gca().xaxis.set_major_formatter(yfmt)
        plt.savefig("results/diffusion/diff_eta_" + str(eta) + "_" + str(t) + ".png", dpi=150)
        # plt.show()


def numfmt(x, pos): # your custom formatter function: divide by 100.0
    s = '{}'.format(x / 100.0)
    return s

if __name__ == '__main__':
    main()
