import numpy as np


grid = np.zeros((3, 3), dtype=int)
turn = 1

print(grid)

case = int(input("truc"))

grid[(case-1)//3, (case-1)%3] = turn

print(grid)
