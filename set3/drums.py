import numpy as np
import scipy as sp
from scipy import linalg
from scipy.sparse import linalg as linalg2

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

import seaborn as sns
sns.set()

def main():
    L = 1
    # amount of discretization steps
    N = 50

    # for now the shape is standard a square
    shape = ["Square", "Rectangle", "Circle"]


    M = make_matrix(N,N)

    dx = (L/N)
    M = (1/dx**2) * M

    eigenvalues, eigenvectors = linalg.eig(M)
    eigenvectors = eigenvectors.T
    eigenvalues = abs(eigenvalues.real)

    eigenvalues_sorted = []
    for eigenvalue in eigenvalues:
        eigenvalues_sorted.append(eigenvalue)
    eigenvalues_sorted.sort()

    max_eigenvalue = eigenvalues_sorted[9]

    # make a fancy 3D plot? :-D
    x = np.linspace(-0.5, 0.5, N)
    y = np.linspace(-0.5, 0.5, N)

    X, Y = np.meshgrid(x, y)

    for i in range((len(eigenvalues_sorted))):

        # plot first .. frequencies
        if eigenvalues[i] <= max_eigenvalue:
            plt.figure()
            plt.grid(False)

            eigenvalue = eigenvalues[i]
            eigenvector = eigenvectors[i]

            matrix = np.reshape(eigenvector.real, (N,N))

            plt.title("$\lambda$: " + str(eigenvalue.real))
            plt.imshow(matrix, origin="lower", vmin=-0.5, vmax=0.5, interpolation='bicubic')
            plt.colorbar()
            plt.savefig("results/drum" + str(eigenvalue.real) + ".png", dpi=150)

            fig = plt.figure()
            plt.title("$\lambda$: " + str(eigenvalue.real))
            ax = plt.axes(projection='3d')
            ax.plot_surface(X, Y, matrix, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
            plt.savefig("results/drum" + str(eigenvalue.real) + "_3D.png", dpi=150)

    # eigenvalues, eigenvectors = linalg.eigh(M)
    # print(eigenvalues)

    # eigenvalues, eigenvectors = linalg2.eigs(M)
    # print(eigenvalues)

    # eigenvalues, eigenvectors = linalg2.eigsh(M)
    # print(eigenvalues)

    # get original signal (wave function?)
    # T(t) = A cos(c * lambda * t) + B sin (c * lambda * t)
    # lambda ^2 = -K, lambda > 0

    # do fourier stuff
    # for eigenvector in eigenvecors:
    #     freq = np.fft.fftfreq(eigenvector)
    #     print(eigenvector)

def make_matrix(rows, cols):
    """ This is a function that makes the matrix. """

    s = (rows**2,cols**2)
    M = np.zeros(s)

    outer_diagonal = rows
    inner_diagonal = 1

    for i in range(rows**2):
        try:
            M[outer_diagonal, i] = 1
            M[i, outer_diagonal] = 1
        except IndexError:
            pass

        try:
            if not inner_diagonal % rows == 0:
                M[inner_diagonal, i] = 1
                M[i, inner_diagonal] = 1
        except IndexError:
            pass

        outer_diagonal += 1
        inner_diagonal += 1

    for i in range(rows**2):
        sum = 0
        for j in range(cols**2):
            sum += M[i,j]

        M[i,i] = -sum

    np.fill_diagonal(M, -4)

    return M


if __name__ == '__main__':
    main()
