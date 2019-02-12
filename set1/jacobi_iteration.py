
def next_step_jacobi(self):
    """ Compute concentration in each grid point. """

    current_state = self.grid
    next_state = copy.copy(self.grid)

    # iterate over grid, first row is always concentration 1, last row always 0
    for i in range(1, self.height - 1):
        # iterate over columsn, first and last are periodic boundaries
        for j in range(1, self.width - 1):
            next_state[i][j] = 1./4 * (current_state[i+1][j]\
                                + current_state[i-1][j]\
                                + current_state[i][j+1]\
                                + current_state[i][j-1])

        # copy for periodic boundaries
        next_state[i][0] = next_state[i][self.width - 2]
        next_state[i][self.width - 1] = next_state[i][1]

    self.grid = copy.copy(next_state)

def next_step_SOR(self):
    """ Compute concentration in each grid point. """

    current_state = self.grid
