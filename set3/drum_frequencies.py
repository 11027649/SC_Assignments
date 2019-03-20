import numpy as np
import scipy as sp
import random
from scipy import linalg
from scipy.sparse import linalg as linalg2

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from Drum import Drum

from mpl_toolkits import mplot3d
import math
import seaborn as sns
sns.set()

def main():
    lengths = [1, 2, 3, 4, 5]
    colors = ["orchid", "mediumspringgreen", "red", "green", "yellow", "blue",\
                "purple", "cyan", "deepskyblue", "lawngreen", "mediumslateblue",\
                "orange", "aqua", "greenyellow"]

    range = np.arange(5, 55, 5)

    # shape can be "Square", "Rectangle" or "Circle"
    shape = "Rectangle"

    L = 1
    disc_steps = [r * L for r in range]

    # f_dependence_on_L(lengths, colors, shape)
    f_dependence_on_N(disc_steps, colors, shape)

def f_dependence_on_L(lengths, colors, shape):
    """ dependence of frequency on length of drum """

    fig = plt.figure()

    for i, L in enumerate(lengths):
        print(i, L)
        # amount of discretization steps
        N = 10 * L

        if shape == "Square":
            width = N
            height = N
            M = make_square_matrix(L, N)
        elif shape == "Rectangle":
            width = N
            height = 2 * N
            M = make_rectangle_matrix(L, N, height)
        elif shape == "Circle":
            width = N
            height = N
            M = make_circle_matrix(L, N)

        # find eigenvalues and eigenvectors of the matrix
        eigenvalues, eigenvectors = find_eigenvalues(M)

        # sort from low to high
        idx = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[idx, :]

        # plot frequencies
        freq = frequencies(eigenvalues)

        for f in freq:
            print(f)
            plt.scatter(L, f, color=colors[i])

    plt.title("Dependency of the frequencies of a drum on it's length\n Shape: " + shape)
    plt.ylabel("Frequency")
    plt.xlabel("Length of drum")
    plt.savefig("results/freq_L_" + shape + ".png")

def f_dependence_on_N(disc_steps, colors, shape):
    """ Dependency of frequency on amount of discretization steps """
    L = 1

    fig = plt.figure()

    ###### dependence of frequencie on length of drum
    for i, N in enumerate(disc_steps):
        print(i, N)
        if shape == "Square":
            width = N
            height = N
            M = make_square_matrix(L, N)
        elif shape == "Rectangle":
            width = N
            height = 2 * N
            M = make_rectangle_matrix(L, N, height)
        elif shape == "Circle":
            width = N
            height = N
            M = make_circle_matrix(L, N)

        # find eigenvalues and eigenvectors of the matrix
        eigenvalues, eigenvectors = find_eigenvalues(M)

        # sort from low to high
        idx = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[idx, :]

        # plot frequencies
        freq = frequencies(eigenvalues)

        for f in freq:
            plt.scatter(N, f, color=colors[i])

    plt.title("Dependency of the frequencies of a drum on the amount of discretization steps\n L = 1, shape: " + shape)
    plt.ylabel("Frequency")
    plt.xlabel("Amount of discretization steps")
    plt.savefig("results/freq_N_" + shape + ".png")

def frequencies(eigenvalues):
    """ Plot all frequencies for the length of a certain drum. """

    frequencies = [math.sqrt(abs(eigenvalue)) for eigenvalue in eigenvalues]

    return frequencies


def find_eigenvalues(M):
    """ Calculate the eigenvalues and corresponding eigenvectors
    of the matrix M. """
    # eigenvalues, eigenvectors = linalg.eig(M)
    # eigenvalues, eigenvectors = linalg2.eigs(M, k=2500)
    # print(eigenvalues, len(eigenvalues))

    eigenvalues, eigenvectors = linalg.eig(M)

    eigenvectors = eigenvectors.T
    eigenvalues = eigenvalues.real

    return eigenvalues, eigenvectors

def find_eigenmodes(eigenvectors, eigenvalues, shape, width, height):
    """ Finds eigenmodes that belong with the smallest eigenvalues. """

    eigenmodes = {}

    for i in range(10):
        # plot first .. frequencies
        eigenvalue = eigenvalues[i]
        eigenvector = eigenvectors[i]

        # matrix = np.reshape(eigenvector.real, (height, width), order='F')
        matrix = np.reshape(eigenvector.real, (height, width))

        eigenmodes[eigenvalue] = matrix

    return eigenmodes

def make_square_matrix(L, N):
    """ This is a function that makes the matrix of a square. """
    dimension = N**2
    M = np.zeros((dimension, dimension))
    dx = (L/N)

    outer_diagonal = N
    inner_diagonal = 1

    for i in range(dimension):
        try:
            M[outer_diagonal, i] = 1 * (1/dx**2)
            M[i, outer_diagonal] = 1 * (1/dx**2)
        except IndexError:
            pass

        try:
            if not inner_diagonal % N == 0:
                M[inner_diagonal, i] = 1 * (1/dx**2)
                M[i, inner_diagonal] = 1 * (1/dx**2)
        except IndexError:
            pass

        outer_diagonal += 1
        inner_diagonal += 1

    np.fill_diagonal(M, -4 * (1/dx**2))

    return M

def make_rectangle_matrix(L, N, height):
    """ This is a function that makes the matrix of a rectangle. """
    dimension = N * height
    M = np.zeros((dimension, dimension))
    dx = (L/N)

    # TODO: This can't be right, there's two L here ... different amount
    # of discretization steps in the two directions (I think?)

    outer_diagonal = N
    inner_diagonal = 1

    for i in range(dimension):
        try:
            M[outer_diagonal, i] = 1 * (1/dx**2)
            M[i, outer_diagonal] = 1 * (1/dx**2)
        except IndexError:
            pass

        try:
            if not inner_diagonal % N == 0:
                M[inner_diagonal, i] = 1 * (1/dx**2)
                M[i, inner_diagonal] = 1 * (1/dx**2)
        except IndexError:
            pass

        outer_diagonal += 1
        inner_diagonal += 1

    np.fill_diagonal(M, -4 * (1/dx**2))

    return M

def make_circle_matrix(L, N):
    """ This is a function that makes the matrix of a circle.
        Grid points within the distance R = L/2 from the center belong to the domain. """
    # N = 5 --> R = 2, dim = 13
    # N = 7 -->

    # Boundary condition for the dimension
    R = round(N/2) #ACTUALLY N = L!?
    dimension = math.ceil(math.pi * R**2)
    print(dimension)
    M = np.zeros((dimension, dimension))
    dx = (L/N)

    outer_diagonal = N
    inner_diagonal = 1

    for i in range(dimension):
        try:
            M[outer_diagonal, i] = 1 * (1/dx**2)
            M[i, outer_diagonal] = 1 * (1/dx**2)
        except IndexError:
            pass

        try:
            if not inner_diagonal % N == 0:
                M[inner_diagonal, i] = 1 * (1/dx**2)
                M[i, inner_diagonal] = 1 * (1/dx**2)
        except IndexError:
            pass

        outer_diagonal += 1
        inner_diagonal += 1

    np.fill_diagonal(M, -4 * (1/dx**2))

    return M

if __name__ == '__main__':
    main()
