import numpy as np
import scipy as sp
from scipy import linalg
from scipy.sparse import linalg as linalg2

def main():
    L = 3

    # for now the shape is standard a square
    shape = ["Square", "Rectangle", "Circle"]

    M = make_matrix(L,L)
    print(M)

    eigenvalues, eigenvectors = linalg.eig(M)
    print(eigenvalues.real)
    print(eigenvectors)

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

    return M


if __name__ == '__main__':
    main()
