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
    L = 4
    N = 40

    M, circle = make_circle_matrix(L, N)
    beginstate, vector_b = initial_conditions(N)

    plt.imshow(beginstate, origin='lower')
    plt.grid(False)
    plt.colorbar()
    plt.show()

    # use standing vector
    vector_c = sp.linalg.solve(M, vector_b)

    # reshape vector_c
    end_state = np.reshape(vector_c, (N, N))

    print(end_state)

    # show endstate
    plt.imshow(end_state, origin='lower')
    plt.grid(False)
    plt.colorbar()
    plt.show()

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


def make_circle_matrix(L, N):
    radius = L/2

    circle = np.zeros((N,N))

    # iterate over matrix, check if distance is < radius, if yes, it's a 1
    x, y = math.floor(N/2), math.floor(N/2)

    for i, row in enumerate(circle):
        for j, column in enumerate(row):
            print(i, j, x, y, N)
            distance = (math.sqrt(abs(i - x)**2 + abs(j - y)**2))/N * 4

            print(distance)
            if distance < radius:
                circle[i, j] = 1

    print(circle)
    M = make_square_matrix(L, N)

    # step over matrix, check if it's a one in the circle
    for i in range(len(M)):
        row = math.floor(i/N)
        column = i % N

        # not in the circle
        if circle[row, column] == 0:
            for j in range(len(M)):
                # put a one at the diagonal so it doesn't change from being 0
                if i == j:
                    M[i, j] = 1

    # diagonal source must be 1 because it doesn't diffuse
    M[12, 12] = 1

    print(M)
    return M, circle

def initial_conditions(N):
    # start at 6, 12
    conc_matrix = np.zeros((N,N))
    conc_matrix[12, 12] = 1

    vector_b = conc_matrix.flatten()

    print(vector_b)

    return conc_matrix, vector_b

if __name__ == '__main__':
    main()
