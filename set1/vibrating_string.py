import math

import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np
import copy

from Wave import Wave

def main():
    # variables
    c = 1.0
    dt = 0.0001
    tmax = 1 #2
    timesteps = math.ceil(tmax/dt)

    # global variables needed for animation
    global current_state, fig, ax1

    # initalize wave, pick 2pi, 5pi or 5pi_constrained_domain
    current_state = Wave("5pi_constrained_domain", c, dt)

    # ask user what to do
    print("Do you want to see the animation of the wave? Yes/No", end=" ")
    visualization = input()

    if visualization == "no":
        for t in range(timesteps):
            current_state.next_step()

        current_state.plot_time_frames()
    elif visualization == "yes":
        #### ANIMATION
        # initalize figure
        fig = plt.figure()
        fig.set_dpi(100)
        fig.suptitle("Vibrating String")

        ax1 = fig.add_subplot(1,1,1)

        # animate
        # interval is between frames
        anim = animation.FuncAnimation(fig, animate, frames=timesteps, interval=1) #, blit=True)

        writer = animation.FFMpegWriter(fps=100, extra_args=['-vcodec','libx264'])

        plt.show()
        print("animation done")
        # save animation
        anim.save('results/vids_wave/vibrating_string_'+ current_state.type + '.mp4', writer=writer)
        print("animation is saved")

def animate(i):
    """ Calculate next state and set that for the animation. """
    current_state.next_step()
    ax1.clear()
    plt.plot(current_state.x, current_state.y_current, color="Pink")
    plt.grid(True)

    plt.ylim([-1.5,1.5])
    plt.xlim([0,1])

if __name__ == '__main__':
    main()
