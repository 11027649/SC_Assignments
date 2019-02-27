import seaborn as sns
sns.set()

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from DiffusionGrid import DiffusionGrid

from matplotlib import colors

def main():
    N = 100
    # eta<1, compact objects, eta = 0 Eden Cluster, =1 normal DLA cluster
    # eta > 1 more open cluster
    eta = 1.5

    # best omega from previous assignment
    omega = 1.914

    # # create discrete colormap
    # cmap = colors.ListedColormap(['navy', 'pink'])
    # bounds = [0,1,2]
    # norm = colors.BoundaryNorm(bounds, cmap.N)

    global fig, im, dla

    dla = DiffusionGrid(N, eta)
    dla.set_omega(omega)

    # set up figure
    fig = plt.figure()
    fig.suptitle("DLA, step: " + str(dla.step))

    # first let it converge
    while not dla.converged:
        dla.next_step()

    im =  plt.imshow(dla.grid)

    # call the animator, blit = True means only redraw changed part
    anim = animation.FuncAnimation(fig, animate, frames=100000, interval=1, blit=False, repeat=False)

    show animation
    plt.xticks([])
    plt.yticks([])
    plt.show()

def animate(i):
    """ Calculate next state and set that for the animation. """

    if not dla.converged:
        dla.next_step()
    # else:
    #     print("aggregating")
    #     dla.aggregation()
    #     dla.check_boundaries()

    fig.suptitle("Diffusion limited aggregation\n step: " + str(dla.step))
    im.set_data(dla.grid)

    return im,


if __name__ == '__main__':
    main()
