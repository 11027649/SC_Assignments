# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This file is part of a program that is used to solve the partial differential
# equations.
# The program has been developed for the course Scientific Computing
# in the master Computational Science at the UvA february/march 2019.
#
# This part contains a direct method to solve the diffusion equation, on a circular
# disk with a single source.
#
# Run it by exectuing ```python diffusion.py``` in a terminal
# Romy Meester & Natasja Wezel
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# to solve eigenvalue problems
import numpy as np
import scipy as sp
import math

# because withouth this my computer starts being weird
from scipy import linalg

# for plotting
import matplotlib.pyplot as plt

# for 3D plotting
from mpl_toolkits import mplot3d

# to make our plots pretty
import seaborn as sns
sns.set()

import matplotlib.ticker as tkr     # has classes for tick-locating and -formatting
import pylab

def make_object_matrix(L, N, diffusion_start):
    """ Make a matrix that contains the circular object. """
    radius = L/2

    circle = np.zeros((N,N))

    # iterate over matrix, check if distance is < radius, if yes, it's a 1
    x, y = math.floor(N/2), math.floor(N/2)

    for i, row in enumerate(circle):
        for j, column in enumerate(row):

            distance = (math.sqrt(abs(i - x)**2 + abs(j - y)**2))/N * L

            if distance < radius:
                circle[i, j] = 1

    # save start of the diffusion as a different number, to use it later
    circle[diffusion_start[0], diffusion_start[1]] = 2

    return circle

def make_diffusion_matrix(L, N, circle):
    """ Make a matrix that contains the connections of the grid. """

    dimension = N**2
    M = np.zeros((dimension, dimension))
    dx = (L/N)

    # start with placing 1's at the right places
    outer_diagonal = N
    inner_diagonal = 1

    for i in range(dimension):
        try:
            M[outer_diagonal, i] = 1
            M[i, outer_diagonal] = 1
        except IndexError:
            pass

        try:
            if not inner_diagonal % N == 0:
                M[inner_diagonal, i] = 1
                M[i, inner_diagonal] = 1
        except IndexError:
            pass

        outer_diagonal += 1
        inner_diagonal += 1

    # all grid points are connected to 4 other points, fill this in at the diagonal
    np.fill_diagonal(M, -4)

    # multiply with constant
    M = (1/dx**2) * M

    # step over matrix, check if it's a one in the circle
    for i in range(len(M)):
        row = math.floor(i/N)
        column = i % N

        # not in the circle or the source
        if circle[row, column] == 0 or circle[row, column] == 2:
            for j in range(len(M)):
                # put a one at the diagonal so it doesn't change from being 0
                if i == j:
                    M[i, j] = 1
                else:
                    M[i, j] = 0

    return M

def initial_conditions(N, diffusion_start):
    """ Create the starting vector, with the source at the right place."""

    conc_matrix = np.zeros((N,N))

    # set the source
    conc_matrix[diffusion_start[0], diffusion_start[1]] = 1

    # flatten the matrix, because we need the vector
    vector_b = conc_matrix.flatten()

    return vector_b

def numfmt(x, pos):
    """ This function takes an ax and returns the formatted values for this ax."""

    # show the final step as a 2.0 because it's pretty
    if x == 39:
        s = 2.0
    else:
        s = '{}'.format((x - 20.0)/10)

    return s

if __name__ == '__main__':
    L = 4
    N = 40

    # this is hardcoded to be at place (0.6, 1.2)
    diffusion_start = (26, 32)

    # make a grid that contains what points belong to the circle and what points not
    circle = make_object_matrix(L, N, diffusion_start)

    # initialize the matrix that contains the connections
    M = make_diffusion_matrix(L, N, circle)

    # get the initial vector
    vector_b = initial_conditions(N, diffusion_start)

    # solve
    vector_c = sp.linalg.solve(M, vector_b)

    # reshape vector_c
    end_state = np.reshape(vector_c, (N, N))

    # plot the endstate
    fig, ax = plt.subplots()

    # show endstate
    plt.title("Diffusion in a disc shaped domain\n 40 discretization steps")

    # stupid ax formatting
    ax.set_xticks([0,5,10,15,20,25,30,35,39])
    ax.set_yticks([0,5,10,15,20,25,30,35,39])

    yfmt = tkr.FuncFormatter(numfmt)    # create your custom formatter function
    pylab.gca().yaxis.set_major_formatter(yfmt)
    pylab.gca().xaxis.set_major_formatter(yfmt)

    # show the diffusion
    plt.imshow(end_state, origin='lower')
    plt.grid(False)
    plt.colorbar()
    plt.xlabel("x coordinate")
    plt.ylabel("y coordinate")
    plt.savefig("results/diffusion/diffusion.png")
