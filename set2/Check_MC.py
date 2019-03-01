import seaborn as sns
sns.set()

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from RandomWalker import RandomWalker
import time
from matplotlib import colors

def main():
    N = 40
    p_stick = 1

    # create discrete colormap
    cmap = colors.ListedColormap(['navy', 'green', 'red'])
    bounds = [0,0.5,1.5,2]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    mc = RandomWalker(N, p_stick)


    # set up figure
    fig = plt.figure()

    while not mc.highest_object == 0:
        mc.next_step()

    mc.remove_walker()

    fig.suptitle("MC, step: " + str(mc.step))
    im = plt.imshow(mc.grid, cmap = cmap, norm =norm)

    # show animation
    plt.xticks([])
    plt.yticks([])

    plt.savefig("results/randomwalker" + str(time.time()) + ".png")


if __name__ == '__main__':
    main()
