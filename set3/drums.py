import numpy as np
import scipy as sp
from scipy import linalg
from scipy.sparse import linalg as linalg2

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import math
import seaborn as sns
sns.set()

def main():
    L = 1
    # amount of discretization steps
    N = 5

    # for now the shape is standard a square
    shapes = ["Square", "Rectangle", "Circle"]
    shapes = ["Circle"]

    for shape in shapes:
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


        print(M)
        # find eigenvalues and eigenvectors of the matrix
        eigenvalues, eigenvectors = find_eigenvalues(M)

        # get the eigenvalue of the 10th mode
        max_eigenvalue = get_max_eigenvalue(eigenvalues)
        print(max_eigenvalue)

        # plot the 10 first modes
        graph_surfaces(eigenvectors, eigenvalues, max_eigenvalue, shape, width, height)




def find_eigenvalues(M):
    """ Calculate the eigenvalues and corresponding eigenvectors
    of the matrix M. """
    # eigenvalues, eigenvectors = linalg.eig(M)
    # eigenvalues, eigenvectors = linalg2.eigs(M, k=2500)
    # print(eigenvalues, len(eigenvalues))

    eigenvalues, eigenvectors = linalg.eig(M)
    print(eigenvalues, len(eigenvalues))

    eigenvectors = eigenvectors.T
    eigenvalues = abs(eigenvalues.real)

    return eigenvalues, eigenvectors

def get_max_eigenvalue(eigenvalues):
    """ Return the maximum eigenvalue of the eigenvalues. """
    eigenvalues_sorted = []

    for eigenvalue in eigenvalues:
        eigenvalues_sorted.append(eigenvalue)
    eigenvalues_sorted.sort()

    try:
        max_eigenvalue = eigenvalues_sorted[9]
    except IndexError:
        max_eigenvalue = math.inf

    return max_eigenvalue

def graph_surfaces(eigenvectors, eigenvalues, max_eigenvalue, shape, width, height):
    """ Makes an 2D and 3D plot of the drum. """
    x = np.linspace(-0.5, 0.5, width)
    y = np.linspace(-0.5, 0.5, height)

    X, Y = np.meshgrid(x, y)

    for i in range(len(eigenvectors)):
        # plot first .. frequencies
        if eigenvalues[i] <= max_eigenvalue:

            plt.figure()
            plt.grid(False)

            eigenvalue = eigenvalues[i]
            eigenvector = eigenvectors[i]

            matrix = np.reshape(eigenvector.real, (width, height))

            plt.title("$\lambda$: " + str(eigenvalue.real))
            plt.imshow(matrix, cmap='viridis', origin="lower", vmin=-0.05, vmax=0.05, interpolation='bicubic')
            plt.colorbar()
            plt.savefig("results/drum" + str(eigenvalue.real) + "_" + str(i) + ".png", dpi=150)
            plt.close()

            fig = plt.figure()
            plt.title("$\lambda$: " + str(eigenvalue.real))
            ax = plt.axes(projection='3d')
            ax.plot_surface(X, Y, matrix, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
            plt.savefig("results/drum" + str(eigenvalue.real) + "_" + str(i) + "_3D.png", dpi=150)
            plt.close()



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

    for i in range(dimension): #range(N**2):
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
