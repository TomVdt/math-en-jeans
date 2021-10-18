import numpy as np


def check_victory(grid):
	for i in range(3):
		# Check the colums
		if grid[i, 0] == grid[i, 1] == grid[i, 2] != 0:
			return grid[i, 0]
		# Check the rows
		if grid[0, i] == grid[1, i] == grid[2, i] != 0:
			return grid[0, i]

	# Check the top-left down-right diagonal
	if grid[0, 0] == grid[1, 1] == grid[2, 2] != 0:
		return grid[0, 0]
	# Check the down-left top-right diagonal
	if grid[2, 0] == grid[1, 1] == grid[0, 2] != 0:
		return grid[2, 0]

	# No one has won
	return 0


def check_valid_move(grid, case):
	return grid[(case - 1) // 3, (case - 1) % 3] == 0


def main():
	# Initialisation
	grid = np.zeros((3, 3), dtype=int)
	turn = 1
	v = 0
	game = True
	print(grid)

	# Main loop
	while game:
		# Wait for user to input a valid move
		while True:
			case = int(input(f"Au tour du joueur {1 if turn == 1 else 2}: "))
			if check_valid_move(grid, case):
				break

		# Place the player's piece on the selected place
		grid[(case - 1) // 3, (case - 1) % 3] = turn

		# Look if the move made the player win
		v = check_victory(grid)
		if v != 0:
			game = False

		# Next player's turn
		turn *= -1

		# Show the board to the users
		print(grid)

	# Show who has won
	print(f"Player {1 if v == 1 else 2} has won the game!")


if __name__ == '__main__':
	main()
