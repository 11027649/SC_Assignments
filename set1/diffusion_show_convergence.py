import math
from DiffusionGrid import DiffusionGrid
import time
import numpy as np
import matplotlib.pyplot as plt
import copy
import seaborn as sns
sns.set()

def main():
    ####### Variables
    # diffusion coefficient
    D = 1

    # divide grid in 50 discrete steps
    height = 50
    width = 50

    # actual lengths are 1
    len_x = 1
    len_y = 1

    methods = ["Jacobi", "Gauss_Seidel", "SOR"]
    omegas = [1.7, 1.8, 1.9, 1.914]

    linear_dependence = {}
    convergence_per_iteration = {}

    for method in methods:

        current_state = DiffusionGrid(height, width, D, method)

        if method == "SOR":
            for omega in omegas:
                current_state = DiffusionGrid(height, width, D, method)
                # for the values of omega
                current_state.set_omega(omega)
                # for the time independent solutions, calculate next states until converged
                while not current_state.converged:
                    current_state.next_step()

                    print(method + str(omega) + str(current_state.time))

                linear_dependence[method + str(omega)] = current_state.dependence_on_y
                convergence_per_iteration[method + str(omega)] = current_state.convergence

        else:
            # for the time independent solutions, calculate next states until converged
            while not current_state.converged:
                current_state.next_step()

                print(method + str(current_state.time))

            linear_dependence[method] = current_state.dependence_on_y
            convergence_per_iteration[method] = current_state.convergence

    linear_dependence["Analytic"] = analytic_solution(D, width)
    print(linear_dependence)

    x = np.linspace(0.,1.,width)

    ###### Plot linear dependence on y
    fig = plt.figure()
    plt.title("Linear dependence on y")
    plt.ylabel("Concentration")
    plt.xlabel("Y coordinate diffusion grid")
    for key in linear_dependence.keys():
        plt.plot(x, linear_dependence[key], label=key)

    plt.legend()
    plt.show()
    fig.savefig('results/linear_dependence'+ str(time.time()) + '.png', dpi=150)


    ######3 PLOT
    fig = plt.figure()
    plt.title("Linear dependence on y\n Diffence between Analytic and Time-Independent methods")
    plt.ylabel("Difference in concentration")
    plt.xlabel("Y coordinate diffusion grid")

    for key in linear_dependence.keys():
        list = [linear_dependence[key][i] - linear_dependence["Analytic"][i] for i in range(len(linear_dependence["Analytic"]))]
        plt.plot(x, list, label=key)

    plt.legend()
    plt.show()
    fig.savefig('results/difference_linear_dependence' + str(time.time()) + '.png', dpi=150)


    ####### Plot convergence per iteration
    fig = plt.figure()
    plt.title("Convergence per iteration")
    plt.ylabel("Convergence (max_delta)")
    plt.xlabel("Iteration")

    for key in convergence_per_iteration.keys():
        plt.semilogy(range(len(convergence_per_iteration[key])), convergence_per_iteration[key], label=key)

    plt.legend()
    plt.show()
    fig.savefig('results/convergence_per_iteration' + str(time.time()) + '.png', dpi=150)

def analytic_solution(D, width):
    M = 10
    x = np.linspace(0.,1.,width)

    # we're only interested in the end state right now
    t = 1

    # make a list with zeros
    y = [0]*len(x)

    for j,xj in enumerate(x):
        for i in range(0,M):
            # add each time
            y[j] += math.erfc((1-xj+2*i)/(2*np.sqrt(D*t))) - math.erfc((1+xj+2*i)/(2*np.sqrt(D*t)))
    return y

if __name__ == '__main__':
    main()
