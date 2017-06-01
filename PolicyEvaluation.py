import copy, numpy as np
from enum import Enum

gridH, gridW, moveReward = 4, 4, -1
grid = np.full((gridW, gridH), 0.)
terminalStates = [[1, 0], [1, 3]]


# Gets the value of (i, j) in grid. Takes into account out of bounds by trimming the values to the nearest legal value
def get_value(grid, i, j):
    if i < 0 or j < 0:
        return grid[0][j] if i < 0 else grid[i][0]
    dim = grid.shape
    if i >= dim[0] or j >= dim[1]:
        return grid[dim[0] - 1][j] if i >= dim[0] else grid[i][dim[1] - 1]
    return grid[i][j]


# A get_val() method that is easier to call
def get_val(i, j):
    return get_value(grid, i, j)


# Computes the values of the states using the iterative policy evaluation method
# The parameter is the gamma in the Bellman equation
def iterative_policy_eval(y):
    global grid
    tempGrid = np.copy(grid)
    for i in range(0, gridW):
        for j in range(0, gridH):
            if [i, j] in terminalStates:
                continue

            tempGrid[i][j] = 1/4 * y * (4 * moveReward + get_val(i + 1, j) +
                                        get_val(i - 1, j) + get_val(i, j + 1) + get_val(i, j-1))

    grid = tempGrid

for i in range(0, 500):
    iterative_policy_eval(1)

print(grid)


