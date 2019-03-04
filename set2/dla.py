import seaborn as sns
sns.set()

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from DiffusionGrid import DiffusionGrid
import time
from matplotlib import colors

def main():
    N = 100
    # eta<1, compact objects, eta = 0 Eden Cluster, =1 normal DLA cluster
    # eta > 1 more open cluster
    eta = 1

    # best omega from previous assignment
    omega = 1.95

    dla = DiffusionGrid(N, eta)
    dla.set_omega(omega)

    while not dla.reached_boundaries:
        dla.next_step()

    t = time.time()

    cmap = colors.ListedColormap(['navy', 'white', 'red'])
    bounds = [0,0.5,1.5,2]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    # set up figure
    fig = plt.figure()
    fig.suptitle("DLA, step: " + str(dla.step) + "eta: " + str(eta))
    plt.xticks([])
    plt.yticks([])
    plt.imshow(dla.object_grid, cmap = cmap, norm =norm)
    plt.savefig("results/diff_" + str(t) + "_eta_" + str(eta) + ".png", dpi=150)
    # plt.show()

    fig = plt.figure()
    fig.suptitle("DLA, step: " + str(dla.step) + "eta: " +str(eta))
    plt.imshow(dla.grid)
    plt.xticks([])
    plt.yticks([])
    plt.savefig("results/diff_" + str(t) + "_object_eta_" + str(eta) + ".png", dpi=150)
    # plt.show()


if __name__ == '__main__':
    main()
