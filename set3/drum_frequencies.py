# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This file is part of a program that is used to solve the partial differential
# equations.
# The program has been developed for the course Scientific Computing
# in the master Computational Science at the UvA february/march 2019.
#
# This part contains methods to find out the dependency of the frequencies
# of drums (with different shapes) on the size of the drum, and the Amount
# of discretization steps we take into account when solving the eigenvalue
# problem.
#
# Run it by exectuing ```python drum_frequencies.py``` in a terminal
# Romy Meester & Natasja Wezel
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import numpy as np
import scipy as sp
import random
from scipy import linalg

import time

import matplotlib.pyplot as plt

import math
import seaborn as sns
sns.set()

def f_dependence_on_L(lengths, colors, shape):
    """ dependence of frequency on length of drum """

    fig = plt.figure()

    for i, L in enumerate(lengths):
        print(i, L)
        # amount of discretization steps
        N = 10 * L

        if shape == "square":
            width = N
            height = N
            M = make_square_matrix(L, N)
        elif shape == "rectangle":
            width = N
            height = 2 * N
            M = make_rectangle_matrix(L, N, height)
        elif shape == "circle":
            width = N
            height = N
            M, circle = make_circle_matrix(L, N)

        # find eigenvalues and eigenvectors of the matrix
        eigenvalues, eigenvectors = find_eigenvalues(M)

        # sort from low to high
        idx = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[idx, :]

        # plot frequencies
        freq = frequencies(eigenvalues)

        for f in freq:
            plt.scatter(L, f, color=colors[i])

    plt.title("Dependency of the frequencies of a drum on it's length\n Shape: " + shape)
    plt.ylabel("Frequency")
    plt.xlabel("Length of drum")
    plt.savefig("results/drums/freq_L_" + shape + ".png")

def f_dependence_on_N(disc_steps, colors, shape):
    """ Dependency of frequency on amount of discretization steps """
    L = 1

    fig = plt.figure()

    ###### dependence of frequencie on length of drum
    for i, N in enumerate(disc_steps):
        print(i, N)
        time1 = time.time()

        if shape == "square":
            width = N
            height = N
            M = make_square_matrix(L, N)
        elif shape == "rectangle":
            width = N
            height = 2 * N
            M = make_rectangle_matrix(L, N, height)
        elif shape == "circle":
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

        spended_time = time.time() - time1
        print(spended_time)

        for f in freq:
            plt.scatter(N, f, color=colors[i])

    plt.title("Dependency of the frequencies of a drum on the amount of discretization steps\n L = 1, shape: " + shape)
    plt.ylabel("Frequency")
    plt.xlabel("Amount of discretization steps")
    plt.savefig("results/drums/freq_N_" + shape + ".png")

def frequencies(eigenvalues):
    """ Plot all frequencies for the length of a certain drum. """

    frequencies = [math.sqrt(abs(eigenvalue)) for eigenvalue in eigenvalues[:20]]

    return frequencies

def find_eigenvalues(M):
    """ Calculate the eigenvalues and corresponding eigenvectors
    of the matrix M. """

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

        matrix = np.reshape(eigenvector.real, (height, width))

        eigenmodes[eigenvalue] = matrix

    return eigenmodes

def make_square_matrix(L, N):
    """ This is a function that makes the matrix of a square. """

    dimension = N**2
    M = np.zeros((dimension, dimension))
    dx = L/N

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

    np.fill_diagonal(M, -4)

    M = (1/dx**2) * M

    return M

def make_rectangle_matrix(L, N, height):
    """ This is a function that makes the matrix of a rectangle. """

    dimension = N * height
    M = np.zeros((dimension, dimension))
    dx = (L/N)

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

    np.fill_diagonal(M, -4)

    M = (1/dx**2) * M

    return M

def make_circle_matrix(L,N):
    """ This is a function that makes a matrix for the circle. """
    R = N/2
    radius = L/2

    circle = np.zeros((N,N))

    # middle point of circle
    x, y = math.floor(N/2), math.floor(N/2)

    # iterate over matrix, check if distance is < radius, if yes, it's a 1
    for i in range(len(circle)):
        for j in range(len(circle[0])):

            distance = (math.sqrt(abs(i - x)**2 + abs(j - y)**2))/N

            if distance < radius:
                circle[i, j] = 1

    M = make_square_matrix(L, N)

    # step over matrix, check if it's a one in the circle
    for i in range(len(M)):
        row = math.floor(i/N)
        column = i % N

        # if this point does not belong to the circle, change the values in the matrix row to 0
        if circle[row, column] == 0:
            for j in range(len(M)):
                if not i == j:
                    M[i, j] = 0

    return M, circle

if __name__ == '__main__':
    colors = ["orchid", "mediumspringgreen", "yellow", "blue",\
                "purple", "cyan", "deepskyblue", "lawngreen", "mediumslateblue",\
                "orange", "aqua", "greenyellow"]

    # shape can be "square", "rectangle" or "circle"
    shapes = ["rectangle", "square", "circle"]

    for shape in shapes:
        print(shape)
        # amounts of discretization steps, for size of drum = 1
        L = 1

        dom = np.arange(5, 65, 5)
        disc_steps = [r * L for r in dom]

        print(disc_steps)

        # lengths to test for the drums
        lengths = [1, 2, 3, 4, 5]

        f_dependence_on_N(disc_steps, colors, shape)
        # f_dependence_on_L(lengths, colors, shape)
