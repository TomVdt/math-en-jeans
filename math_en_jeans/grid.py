from enum import Enum


class Piece(Enum):
	EMPTY = 0
	PLAYER1 = 1
	PLAYER2 = -1


class Grid:
	EMPTY = Piece.EMPTY
	PLAYER1 = Piece.PLAYER1
	PLAYER2 = Piece.PLAYER2

	def __init__(self, state=None):
		self.reset_state = state or []
		self.state = state or []

	def __iter__(self):
		return iter(self.state)

	def __hash__(self):
		return hash(tuple(self.state))

	def reset(self):
		self.state = self.reset_state

	def game_over(self):
		raise NotImplementedError()

	def has_won(self):
		raise NotImplementedError()

	def is_free(self, index):
		return self.state[index] == self.EMPTY

	def is_empty(self):
		raise NotImplementedError()

	def is_full(self):
		raise NotImplementedError()

	def is_valid_move(self, move, player):
		raise NotImplementedError()

	def play(self, player, move):
		raise NotImplementedError()

	def unplay(self, move):
		raise NotImplementedError()

	def get_available_moves(self, player):
		raise NotImplementedError()

	def get_score(self):
		return 0


# Move is a tuple (row, col)
class TicTacToeGrid(Grid):

	def __init__(self, state=None):
		state = state or [Piece.EMPTY for i in range(9)]
		super().__init__(state=state)

	def __repr__(self):
		new_lst = ['' for i in range(9)]
		for i, piece in enumerate(self.state):
			new_lst[i] = {self.EMPTY: ' ', self.PLAYER1: 'o', self.PLAYER2: 'x'}[piece]
		return '{}|{}|{}\n-+-+-\n{}|{}|{}\n-+-+-\n{}|{}|{}'.format(*new_lst)

	def has_won(self):
		for i in range(3):
			# Row
			if self.state[i*3] == self.state[i*3 + 1] == self.state[i*3 + 2] != self.EMPTY:
				# Return winning player
				return self.state[i*3]
			# Column
			if self.state[i] == self.state[i + 3] == self.state[i + 6] != self.EMPTY:
				return self.state[i]
		# Top-left diagonal
		if self.state[0] == self.state[4] == self.state[8] != self.EMPTY:
			return self.state[0]
		# Bottom-left diagonal
		if self.state[6] == self.state[4] == self.state[2] != self.EMPTY:
			return self.state[6]
		# No one won
		return self.EMPTY

	def is_full(self):
		# Check if there are no empty spaces left
		return self.EMPTY not in self.state

	def is_empty(self):
		return self.state.count(self.EMPTY) == len(self.state)

	def is_free(self, index):
		return self.state[index] == self.EMPTY

	def is_valid_move(self, move, player):
		return self.is_free(move)

	def game_over(self):
		return (self.has_won() != self.EMPTY) or self.is_full()

	def play(self, player, move):
		if self.state[move] != self.EMPTY:
			raise ValueError("Tried placing a piece in a non-free space!")
		else:
			self.state[move] = player

	def unplay(self, move):
		self.state[move] = self.EMPTY

	def get_available_moves(self, player):
		return [i for i in range(9) if self.state[i] == self.EMPTY]


# Move is a tuple (type, old_index, new_index)
class AchiGrid(Grid):
	# Define how the grid is connected
	# 0 1 2
	# 3 4 5
	# 6 7 8
	CONNECTIONS = {
		0: (1, 3, 4),
		1: (0, 2, 4),
		2: (1, 4, 5),
		3: (0, 4, 6),
		4: (0, 1, 2, 3, 5, 6, 7, 8),
		5: (2, 4, 8),
		6: (3, 4, 7),
		7: (4, 6, 8),
		8: (4, 5, 7)
	}
	# Number of pieces per person
	NUM_PIECES = 4

	def __init__(self, state=None):
		state = state or [Piece.EMPTY for i in range(9)]
		super().__init__(state=state)

	def __repr__(self):
		new_lst = ['' for i in range(9)]
		for i, piece in enumerate(self.state):
			new_lst[i] = {self.EMPTY: ' ', self.PLAYER1: 'o', self.PLAYER2: 'x'}[piece]
		return '{}|{}|{}\n-+-+-\n{}|{}|{}\n-+-+-\n{}|{}|{}'.format(*new_lst)

	def has_won(self):
		for i in range(3):
			# Row
			if self.state[i*3] == self.state[i*3 + 1] == self.state[i*3 + 2] != self.EMPTY:
				# Return winning player
				return self.state[i*3]
			# Column
			if self.state[i] == self.state[i + 3] == self.state[i + 6] != self.EMPTY:
				return self.state[i]
		# Top-left diagonal
		if self.state[0] == self.state[4] == self.state[8] != self.EMPTY:
			return self.state[0]
		# Bottom-left diagonal
		if self.state[6] == self.state[4] == self.state[2] != self.EMPTY:
			return self.state[6]
		# No one won
		return self.EMPTY

	def is_full(self):
		# Check if there are no empty spaces left
		return self.EMPTY not in self.state

	def is_empty(self):
		return self.state.count(self.EMPTY) == len(self.state)

	def is_valid_move(self, move, player):
		move_type, old_index, new_index = move
		if move_type == 'new':
			return self.state[new_index] == self.EMPTY
		else:
			return (self.state[old_index] == player) and (old_index in self.CONNECTIONS[new_index])

	def game_over(self):
		return self.has_won() != self.EMPTY

	def play(self, player, move):
		move_type, old_index, new_index = move
		if self.state[new_index] != self.EMPTY:
			raise ValueError("Tried placing a piece in a non-free space!")
		else:
			if move_type == 'move':
				self.state[new_index] = self.state[old_index]
				self.state[old_index] = self.EMPTY
			elif move_type == 'new':
				self.state[new_index] = player

	def unplay(self, move):
		move_type, old_index, new_index = move
		if move_type == 'move':
			self.state[old_index] = self.state[new_index]
			self.state[new_index] = self.EMPTY
		elif move_type == 'new':
			self.state[new_index] = self.EMPTY

	def get_available_moves(self, player):
		phase = self.get_game_phase()
		# Phase 1: TicTacToe phase
		if phase == 'tictactoe':
			# Same as TicTacToe
			return [('new', 0, i) for i in range(9) if self.state[i] == self.EMPTY]
		# Phase 2 (moving phase)
		else:
			# Find empty space
			destination = self.state.index(self.EMPTY)
			# Find every single piece of the player that can be moved
			return [('move', origin, destination) for origin in self.CONNECTIONS[destination] if self.state[origin] == player]

	def get_game_phase(self):
		return 'move' if self.state.count(self.PLAYER1) == self.NUM_PIECES and self.state.count(self.PLAYER2) == self.NUM_PIECES else 'tictactoe'

	def get_free_spaces_adjacent(self, index):
		return self.state.index(self.EMPTY)


# Move is a tuple (type, old_index, new_index)
class PicariaGrid(AchiGrid):
	# Define how the grid is connected
	# 0  -  2  -  4
	# -  6  -  8  -
	# 10 -- 12 -- 14
	# -- 16 -- 18 --
	# 20 -- 22 -- 24
	CONNECTIONS = {
		0: (2, 6, 10),
		2: (0, 4, 6, 8, 12),
		4: (2, 8, 14),
		6: (0, 2, 10, 12),
		8: (2, 4, 12, 14),
		10: (0, 6, 12, 16, 20),
		12: (2, 6, 8, 10, 14, 16, 18, 22),
		14: (4, 8, 12, 18, 24),
		16: (10, 12, 20, 22),
		18: (12, 14, 22, 24),
		20: (10, 16, 22),
		22: (12, 16, 18, 20, 24),
		24: (14, 18, 22),
	}
	# Number of pieces per person
	NUM_PIECES = 3

	def __init__(self, state=None):
		state = state or [Piece.EMPTY for i in range(25)]
		super().__init__(state=state)

	# TODO: a clean repr? (not essential)
	def __repr__(self):
		return repr(self.state)

	def has_won(self):
		for i in range(3):
			# Row
			if self.state[i*10] == self.state[i*10 + 2] == self.state[i*10 + 4] != self.EMPTY:
				# Return winning player
				return self.state[i*10]
			# Column
			if self.state[i*2] == self.state[i*2 + 10] == self.state[i*2 + 20] != self.EMPTY:
				return self.state[i*2]
		# Top-left diagonal
		if self.state[6] == self.state[12] == self.state[18]:
			return self.state[0]
		# Bottom-left diagonal
		if self.state[16] == self.state[12] == self.state[8] != self.EMPTY:
			return self.state[6]
		# Check small squares (ugly but works)
		if self.state[0] == self.state[6] == self.state[12] != self.EMPTY:
			return self.state[0]
		if self.state[10] == self.state[6] == self.state[2] != self.EMPTY:
			return self.state[10]
		if self.state[2] == self.state[8] == self.state[14] != self.EMPTY:
			return self.state[2]
		if self.state[12] == self.state[8] == self.state[4] != self.EMPTY:
			return self.state[12]
		if self.state[10] == self.state[16] == self.state[22] != self.EMPTY:
			return self.state[10]
		if self.state[20] == self.state[16] == self.state[12] != self.EMPTY:
			return self.state[20]
		if self.state[12] == self.state[18] == self.state[24] != self.EMPTY:
			return self.state[12]
		if self.state[22] == self.state[18] == self.state[14] != self.EMPTY:
			return self.state[22]
		# Check small middle diagonals
		if self.state[6] == self.state[12] == self.state[18] != self.EMPTY:
			return self.state[6]
		if self.state[16] == self.state[12] == self.state[8] != self.EMPTY:
			return self.state[16]
		# No one won
		return self.EMPTY

	def is_full(self):
		# Check if there are no empty spaces left
		# Skip every odd space
		return self.EMPTY not in self.state[::2]

	def is_valid_move(self, move, player):
		move_type, old_index, new_index = move
		if not 0 <= old_index <= 24 or not 0 <= new_index <= 24:
			return False
		if move_type == 'new':
			return (new_index != 12) and (self.state[new_index] == self.EMPTY)
		elif move_type == 'move':
			return (self.state[old_index] == player) and (old_index in self.CONNECTIONS[new_index])
		else:
			return False

	def get_available_moves(self, player):
		phase = self.get_game_phase()
		# Phase 1: TicTacToe phase
		if phase == 'tictactoe':
			# Disallow placing in the center
			return [('new', 0, i) for i in range(0, 25, 2) if (self.state[i] == self.EMPTY and i != 12)]
		# Phase 2 (moving phase)
		else:
			# Find empty space
			moves = []
			for i, piece in enumerate(self.state):
				if piece == player:
					destinations = self.get_free_spaces_adjacent(i)
					for destination in destinations:
						moves.append(('move', i, destination))
			return moves

	def get_free_spaces_adjacent(self, index):
		return [place for place in self.CONNECTIONS[index] if self.state[place] == self.EMPTY]
