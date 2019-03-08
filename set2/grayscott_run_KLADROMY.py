import seaborn as sns
sns.set()

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors

from GrayScott import GrayScott

import matplotlib.ticker as tkr
import pylab
import time

def main():
    N = 100

    # these need to be global for the animation
    global gs, im, fig

    # initiate image and diffusion grid
    gs = GrayScott(N)

    # set up figure
    fig, ax = plt.subplots()

    ax.grid(False)

    ax.set_xticks([0,20,40,60,80,99])
    ax.set_yticks([0,20,40,60,80,99])
    ax.set_xlabel("x-coordinate")
    ax.set_ylabel("y-coordinate")


    yfmt = tkr.FuncFormatter(numfmt)    # create your custom formatter function
    pylab.gca().yaxis.set_major_formatter(yfmt)
    pylab.gca().xaxis.set_major_formatter(yfmt)


    fig.suptitle("Reaction Diffusion, Gray-Scott Model\n step:" + str(gs.time))
    gs.time = 0
    im =  plt.imshow(gs.u_conc, origin='lower', vmin=0, vmax=1, interpolation='bicubic')
    plt.colorbar()

    t = time.time()
    gs.next_step()

    for i in range(5000):
        print("preperation,", i)
        gs.next_step()

# https://mrob.com/pub/comp/xmorphia/pearson-classes.html
# # object 1 Type eta (η)?? = (gs.u_conc) / (gs.u_conc + gs.v_conc)) with
#     self.f = 0.035
#     self.k = 0.060

# object 2 Type xi (ξ) = gs.u_conc with
# self.f = 0.010
# self.k = 0.041

# self.f = 0.04
# self.k = 0.06
        if i % 50 == 0:
            fig.suptitle("Reaction Diffusion, Gray-Scott Model\n step:" + str(gs.time))
            im.set_data(gs.u_conc)
            plt.savefig("results/grayscott/Grayscott/object4_time_" + str(i) + "_" + str(t) + ".png", dpi=500)

    np.savetxt("results/grayscott/Grayscott/object4_conc_u.txt", gs.total_u)
    np.savetxt("results/grayscott/Grayscott/object4_conc_v.txt", gs.total_v)


    plt.figure()

    plt.plot([i * 50 for i in range(len(gs.total_u))], gs.total_u, label="Total concentration of u")
    plt.plot([i * 50 for i in range(len(gs.total_v))], gs.total_v, label="Total concentration of v")
    plt.title("Total concentrations of reactants trough time")
    plt.xlabel("Time")
    plt.ylabel("Concentration")
    plt.legend()
    plt.savefig("results/grayscott/Grayscott/object4_totalconcentrations_" +str(t) + ".png", dpi=500 )

    # call the animator, blit = True means only redraw changed part
    # anim = animation.FuncAnimation(fig, animate, frames=1, interval=1, repeat=False)
    #
    # # show animation
    # plt.colorbar()
    # plt.show()


def animate(i):
    """ Calculate next state and set that for the animation. """

    gs.next_step()
    fig.suptitle("Fluid Dynamics, Gray-Scott Model\n step:" + str(gs.time))
    im.set_data(gs.u_conc)

    return im,

def numfmt(x, pos): # your custom formatter function: divide by 100.0
    s = '{}'.format(x / 100.0)
    if x == 99:
        s = 1.0
    return s

if __name__ == '__main__':
    main()
