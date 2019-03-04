import seaborn as sns
sns.set()

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors

from GrayScott import GrayScott

def main():

    # these need to be global for the animation
    global gs, im, fig

    # initiate image and diffusion grid
    gs = GrayScott(50)

    # set up figure
    fig = plt.figure()
    fig.suptitle("Fluid Dynamics, Gray-Scott Model\n step:" + str(gs.time))

    im =  plt.imshow(gs.u_conc)

    # call the animator, blit = True means only redraw changed part
    anim = animation.FuncAnimation(fig, animate, frames=100, interval=1, repeat=False)

    for row in gs.u_conc:
        print(row)

    print(gs.v_conc)


    # show animation
    plt.xticks([])
    plt.yticks([])
    plt.colorbar()
    plt.show()


def animate(i):
    """ Calculate next state and set that for the animation. """

    gs.next_step()
    fig.suptitle("Fluid Dynamics, Gray-Scott Model\n step:" + str(gs.time))
    im.set_data(gs.u_conc)

    return im,


if __name__ == '__main__':
    main()
