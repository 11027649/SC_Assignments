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
    N = 100
    p_stick = 0.7

    # create discrete colormap
    cmap = colors.ListedColormap(['navy', 'white', 'red'])
    bounds = [0,0.5,1.5,2]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    mc = RandomWalker(N, p_stick)

    # set up figure
    fig, ax = plt.subplots()

    # hide gridlines
    ax.grid(False)
    ax.set_xticks([0,0.2, 0.4, 0.6, 0.8, 1])
    ax.set_yticks([0,0.2, 0.4, 0.6, 0.8, 1])

    while not mc.highest_object == N - 1:
        print(mc.highest_object)
        mc.next_step()

    mc.remove_walker()
    plt.ylabel("y-coordinate")
    plt.xlabel("x-coordinate")

    fig.suptitle("MC, step: " + str(mc.step) + " p-stick: " + str(p_stick), fontsize='large')
    im = plt.imshow(mc.grid, cmap = cmap, norm =norm, origin='lower')

    plt.savefig("results/randomwalker/mc_pstick_" + str(p_stick) + "_" + str(time.time()) + ".png")


if __name__ == '__main__':
    main()
