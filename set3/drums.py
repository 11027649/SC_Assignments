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
    N = 50

    # for now the shape is standard a square
    shape = ["Square", "Rectangle", "Circle"]

    # test speed difference 
    for i in range(10):
        print(i)
        M = make_square_matrix(L,N)

        eigenvalues, eigenvectors = find_eigenvalues(M)

        max_eigenvalue = get_max_eigenvalue(eigenvalues)
        print(max_eigenvalue)
        # graph_surfaces(eigenvectors, eigenvalues, max_eigenvalue, N)




def find_eigenvalues(M):
    eigenvalues, eigenvectors = linalg.eig(M)
    eigenvectors = eigenvectors.T
    eigenvalues = abs(eigenvalues.real)

    return eigenvalues, eigenvectors

def get_max_eigenvalue(eigenvalues):
    eigenvalues_sorted = []
    
    for eigenvalue in eigenvalues:
        eigenvalues_sorted.append(eigenvalue)
    eigenvalues_sorted.sort()

    # bins = np.linspace(math.ceil(eigenvalues_sorted[0]), math.floor(eigenvalues_sorted[len(eigenvalues) - 1]), 100)
    # plt.hist(eigenvalues_sorted, bins=bins)
    # plt.show()

    max_eigenvalue = eigenvalues_sorted[9]

    return max_eigenvalue

def graph_surfaces(eigenvectors, eigenvalues, max_eigenvalue, N):
    # make a fancy 3D plot? :-D
    x = np.linspace(-0.5, 0.5, N)
    y = np.linspace(-0.5, 0.5, N)

    X, Y = np.meshgrid(x, y)

    for i in range((len(eigenvectors))):
        # plot first .. frequencies
        if eigenvalues[i] <= max_eigenvalue:

            plt.figure()
            plt.grid(False)

            eigenvalue = eigenvalues[i]
            eigenvector = eigenvectors[i]

            matrix = np.reshape(eigenvector.real, (N,N))

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
    """ This is a function that makes the matrix. """
   
    M = np.zeros((N**2, N**2))
    dx = (L/N)

    outer_diagonal = N
    inner_diagonal = 1

    for i in range(N**2):
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
