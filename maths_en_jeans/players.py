__all__ = ['HumanPlayer', 'RandomPlayer', 'MinimaxPlayer', 'SthPlayer']

import random


class Player:

	def __init__(self, piece, opponent):
		self.piece = piece
		self.opponent = opponent
		self.ready = True

	def on_user_interaction(self, row, col):
		return

	def get_next_move(self, state):
		raise NotImplementedError()


class HumanPlayer(Player):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ready = False
		self.move = None

	def on_user_interaction(self, row, col):
		self.move = (row, col)
		self.ready = True

	def get_next_move(self, state):
		self.ready = False
		return self.move


class RandomPlayer(Player):

	def get_next_move(self, state):
		return random.choice(state.get_available_moves())


class SthPlayer(Player):

	def get_next_move(self, state):
		return ...


class MinimaxPlayer(Player):
	SEARCH_DEPTH = 9

	def get_score(self, state, depth):
		winner = state.has_won()
		if winner == self.piece:
			score = 10000 + depth
		elif winner == self.opponent:
			score = -10000 + depth
		else:
			score = 0
			# Score for the position of the pieces
			pass
		return score

	def minimax(self, state, maximizer, depth):
		moves = state.get_available_moves()
		if depth == 0 or state.game_over():
			return self.get_score(state, depth)
		if maximizer:
			max_score = -999999999
			for move in moves:
				state.play(self.piece, *move)
				score = self.minimax(state, False, depth - 1)
				state.unplay(*move)
				max_score = max(score, max_score)
			return max_score
		else:
			min_score = 999999999
			for move in moves:
				state.play(self.opponent, *move)
				score = self.minimax(state, True, depth - 1)
				state.unplay(*move)
				min_score = min(score, min_score)
			return min_score

	def get_next_move(self, state):
		moves = state.get_available_moves()

		max_score = -999999999
		best_move = moves[0]
		for i, move in enumerate(moves):
			state.play(self.piece, *move)
			score = self.minimax(state, False, self.SEARCH_DEPTH)
			state.unplay(*move)
			if score > max_score:
				max_score = score
				best_move = move
		return best_move
