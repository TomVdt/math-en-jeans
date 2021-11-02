import numpy as np
print("Hello, World!")


# Real player object, handles interaction with the human player
class Player:

	# Initialise player class by giving it it's corresponding piece
	def __init__(self, turn):
		self.turn = turn

	# Handle player input correctly, only send back a valid move
	def get_next_move(self, grid):
		while True:
			case = 0
			try:
				case = int(input(f"Player {1 if self.turn == 1 else 2}'s turn: "))
			except ValueError:
				print("Invalid")
			if 1 <= case <= 9:
				if not check_valid_move(grid, case):
					print("Occupied!")
				else:
					break
		return case


# Bot object, handles the minimax algorithm to find the best move
class Bot:

	def __init__(self, turn):
		self.turn = turn
		self.depth = 9

	# Attribute a score to a certain board state
	def get_score(self, grid):
		if check_victory(grid, self.turn):
			score = 1000000000
		elif check_victory(grid, -self.turn):
			score = -1000000000
		else:
			score = 0
		return score

	# Recursive minimax algorithm (TODO)
	def minimax(self, grid, turn, depth):
		if depth == 0 or game_end(grid):
			return self.get_score(grid)

	# Get the best move for the bot
	def get_next_move(self, grid):
		valid_moves = get_valid_moves(grid)
		for move in valid_moves:
			pass
		return


# See if the game has ended (full or player win)
def game_end(grid):
	return len(get_valid_moves(grid)) == 0 or check_victory(grid, 1) or check_victory(grid, -1)


# Give a list with all valid moves
def get_valid_moves(grid):
	moves = []
	for i in range(3):
		for j in range(3):
			if grid[i, j] == 0:
				moves.append(i * 3 + j)
	return moves


# Check if a player has won
def check_victory(grid, player):
	for i in range(3):
		# Check the columns
		if grid[i, 0] == grid[i, 1] == grid[i, 2] == player:
			return True
		# Check the rows
		if grid[0, i] == grid[1, i] == grid[2, i] == player:
			return True

	# Check the top-left down-right diagonal
	if grid[0, 0] == grid[1, 1] == grid[2, 2] == player:
		return True
	# Check the down-left top-right diagonal
	if grid[2, 0] == grid[1, 1] == grid[0, 2] == player:
		return True

	return False


# Check if a move is valid
def check_valid_move(grid, case):
	return grid[(case - 1) // 3, (case - 1) % 3] == 0


def main():
	# Initialisation
	grid = np.zeros((3, 3), dtype=int)
	player1 = Player(1)
	player2 = Player(-1)
	turn = 1
	case = 0
	v = 0
	game = True
	print(grid)

	# Main loop
	while game:
		# Get the move for the correct player
		if turn == 1:
			case = player1.get_next_move(grid)
		elif turn == -1:
			case = player2.get_next_move(grid)
		else:
			raise ValueError('`turn` is not 1 or -1, how did this happen?')

		# Place the player's piece on the selected place
		grid[(case - 1) // 3, (case - 1) % 3] = turn

		# Check if the move made the player win
		v = check_victory(grid, turn)
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
