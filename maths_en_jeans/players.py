__all__ = ['HumanPlayer', 'RandomPlayer', 'MinimaxPlayer']

import random


# Avoid importing math.inf ¯\_(ツ)_/¯
inf = float('inf')


class Player:

	def __init__(self, piece, opponent):
		self.piece = piece
		self.opponent = opponent
		self.ready = True

	def set_move(self, move):
		return

	def get_next_move(self, state):
		raise NotImplementedError()


class HumanPlayer(Player):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ready = False
		self.move = None

	def set_move(self, move):
		self.move = move
		self.ready = True

	def get_next_move(self, state):
		self.ready = False
		return self.move


class CustomPlayer(Player):

	def get_next_move(self, state):
		return ...


class RandomPlayer(Player):

	def get_next_move(self, state):
		return random.choice(state.get_available_moves(self.piece))


class MinimaxPlayer(Player):
	SEARCH_DEPTH = 10

	def get_score(self, state, depth):
		winner = state.has_won()
		if winner == self.piece:
			return 1000 + depth
		elif winner == self.opponent:
			return -1000 - depth
		else:
			# Score for the position of the pieces
			# Depends on the game, so we leave the
			# implementation inside the game logic
			return state.get_score()

	def minimax(self, state, maximizer, depth):
		moves = state.get_available_moves(self.piece if maximizer else self.opponent)
		if depth == 0 or state.game_over():
			return self.get_score(state, depth)
		if maximizer:
			score = -inf
			for move in moves:
				state.play(self.piece, move)
				score = max(self.minimax(state, False, depth - 1), score)
				state.unplay(move)
		else:
			score = inf
			for move in moves:
				state.play(self.opponent, move)
				score = min(self.minimax(state, True, depth - 1), score)
				state.unplay(move)
		return score

	def get_next_move(self, state):
		moves = state.get_available_moves(self.piece)

		# Emulate 1 round of minimax to save the best move
		max_score = -inf
		best_move = moves[0]
		for i, move in enumerate(moves):
			state.play(self.piece, move)
			score = self.minimax(state, False, self.SEARCH_DEPTH)
			state.unplay(move)
			if score > max_score:
				max_score = score
				best_move = [move]
			elif score == max_score:
				# Save all moves with the same score
				best_move.append(move)
		# Chose 1 move from all of the best moves (more fun!)
		return random.choice(best_move)
