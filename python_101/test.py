import numpy as np


def check_victory(grid):
	for i in range(3):
		if grid[i, 0] == grid[i, 1] == grid[i, 2]:
			return grid[i, 0]
		if grid[0, i] == grid[1, i] == grid[2, i]:
			return grid[0, i]
	if grid[0, 0] == grid[1, 1] == grid[2, 2] or grid[0, 2] == grid[1, 1] == grid[2, 0]:
		return grid[1, 1]
	#if grid[0, 2] == grid[1, 1] == grid[2, 0]:
	#	return grid[1, 1]
	return 0


def main():
	# Initialisation de Pn à n=0
	grid = np.zeros((3, 3), dtype=int)
	turn = 1
	v = 0
	game = True

	# Main lööps
	while game:
		print(grid)
		case = int(input(f"Player {1 if turn == 1 else 2}: "))
		grid[(case-1)//3, (case-1)%3] = turn
		v = check_victory(grid)
		if v != 0:
			game = False
		turn *= -1
	print(v)

# Some wizard shit I don't understand. Must question the grand-sorcerer cat-lord dude Thursday
# I'm guessing it runs the script if the code is the main. But just like... SYNTAX???
if __name__ == '__main__':
	main()
