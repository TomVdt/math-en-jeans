import numpy as np


def check_victory(grid):
	for i in range(3):
		if grid[i, 0] == grid[i, 1] == grid[i, 2]:
			return grid[i, 0]
	return 0


def main():
	# Initialisation
	grid = np.zeros((3, 3), dtype=int)
	turn = 1
	v = 0
	game = True

	# Main loop
	while game:
		print(grid)
		case = int(input(f"Au tour du joueur {1 if turn == 1 else 2}:\n"))
		grid[(case-1)//3, (case-1)%3] = turn
		v = check_victory(grid)
		if v != 0:
			game = False
		turn *= -1
	print(v)


if __name__ == '__main__':
	main()
