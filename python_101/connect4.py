import numpy as np


grid = np.zeros((6, 7), dtype=int)
print(grid)
turn = 1
game = True


while game:
    column = int(input(f"Player {turn}: "))
    for i in range(5, -1, -1):
        if grid[i, column-1] == 0:
            grid[i, column-1] = turn
            turn *=-1
            break
    print(grid)
    horizontal_sums = [sum(grid[j,i] for i in range(k,k+4)) for j in range(6) for k in range(4)]
    vertical_sums = [sum(grid[i,j] for i in range(k,k+4)) for j in range(6) for k in range(3)]
    dexter_sums = [sum(grid[i+k,i+j] for i in range(4)) for j in range(4) for k in range(3)]
    sinister_sums = [sum(grid[i+k,6-(i+j)] for i in range(4)) for j in range(4) for k in range(3)]
    score_sum = horizontal_sums + vertical_sums + dexter_sums + sinister_sums
    for i in range(len(score_sum)):
        if abs(score_sum[i]) == 4:
            print("\nPlayer", int(score_sum[i]/4), "wins")
            game = False
            break