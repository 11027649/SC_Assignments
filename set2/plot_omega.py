# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This file is part of a program that is used to solve some partial differential
# equations. The program has been developed for the course Scientific Computing
# in the master Computational Science at the UvA february/march 2019.
#
# This part contains the code to plot the results from the search for the optimum
# omega. This is for exercise A from set 2.
#
# Run it by: python diffusion_plot_opt_omega.py
# Romy Meester & Natasja Wezel
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pandas as pd
import matplotlib.pyplot as plt
import math
import copy
import seaborn as sns
sns.set()

def main():
    df = pd.read_csv('omega_results.csv', sep=',', names = ["ObjectSize", "Eta", "Omega", "Steps"])
    print(df)

    df = df[df["ObjectSize"] == "100"]

    y = df[(df["ObjectSize"] == 26) & (df["Eta"] == 1.0)]["Steps"]

    fig = plt.figure()
    plt.plot(df["Omega"], df["Steps"])

    # plt.xlim(1.5,2)
    # plt.ylim(0,1000)

    plt.title("Omega versus the amount of steps\n Search for optimal omega")
    plt.ylabel("Amount of Steps")
    plt.xlabel("Value for omega")
    #
    # best_omegas = []
    #
    # for i in range(10, 100, 5):
    #     # find minimum amount of steps
    #     minimum = min(df[df["Gridsize"] == i]["Steps"])
    #
    #     # find omega belonging with this minimum
    #     omega = copy.deepcopy()
    #
    #     for w in omega:
    #         plt.scatter(i, w)
    #
    #     omega = omega.iloc[math.floor(len(omega) / 2)]
    #     best_omegas.append(omega)
    #
    # plt.plot(range(10,100,5), best_omegas)

    plt.show()
    # fig.savefig("results/optimum_omega.png", dpi=150)


if __name__ == '__main__':
    main()
