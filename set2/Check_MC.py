import seaborn as sns
sns.set()

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from RandomWalker import RandomWalker

from matplotlib import colors

def main():
    N = 100

    # create discrete colormap
    cmap = colors.ListedColormap(['navy', 'green', 'red'])
    bounds = [0,0.5,1.5,2]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    global fig, im, mc

    mc = RandomWalker(N)


    # set up figure
    fig = plt.figure()
    fig.suptitle("MC, step: " + str(mc.step))

    im = plt.imshow(mc.grid, cmap = cmap, norm =norm)

    # call the animator, blit = True means only redraw changed part
    anim = animation.FuncAnimation(fig, animate, frames=1000, interval=1, blit=False, repeat=False)

    # show animation
    plt.xticks([])
    plt.yticks([])
    plt.show()

def animate(i):
    """ Calculate next state and set that for the animation. """

    mc.next_step()
    fig.suptitle("Diffusion limited aggregation\n step: " + str(mc.step))
    im.set_data(mc.grid)

    return im,


if __name__ == '__main__':
    main()
