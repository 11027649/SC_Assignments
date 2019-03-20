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

    M, circle = make_circle_matrix(N)
    beginstate = initial_conditions(N)

def make_circle_matrix(N, L):
    radius = L/2

    circle = np.zeros((N,N))

    # iterate over matrix, check if distance is < radius, if yes, it's a 1
    x, y = math.floor(N/2), math.floor(N/2)

    for i, row in enumerate(circle):
        for j, column in enumerate(row):
            distance = (math.sqrt(abs(i - x)**2 + abs(j - y)**2))/N

            if distance < radius:
                circle[i, j] = 1
    print(circle)
    M = make_square_matrix(L, N)

    # step over matrix, check if it's a one in the circle
    for i in range(len(M)):
        row = math.floor(i/N)
        column = i % N

        # if this point does not belong to the circle, change the values in the matrix row to 0
        if circle[row, column] == 0:
            for j in range(len(M)):
                if not i == j:
                    M[i, j] = 1
    print(M)
    return M, circle

def initial_conditions():
    # start at 6, 12
    conc_matrix = np.zeros((N,N))
    conc_matrix[6, 12] = 1

    return conc_matrix

if __name__ == '__main__':
    main()
