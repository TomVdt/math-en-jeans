import pyglet
import glooey

from maths_en_jeans.scenes.scene import Scene
from maths_en_jeans.players import *


class Grid:
	EMPTY = 0
	PLAYER1 = 1
	PLAYER2 = -1

	def __init__(self, state=[0 for i in range(9)]):
		self.state = state

	def __iter__(self):
		return iter(self.state)

	def game_over(self):
		return (self.has_won() != self.EMPTY) or self.is_full()

	def has_won(self):
		for i in range(3):
			# Row
			if self.state[i*3] == self.state[i*3 + 1] == self.state[i*3 + 2]:
				# Return winning player
				return self.state[i*3]
			# Column
			if self.state[i] == self.state[i + 3] == self.state[i + 6]:
				return self.state[i]
		# Top-left diagonal
		if self.state[0] == self.state[4] == self.state[8]:
			return self.state[0]
		# Bottom-left diagonal
		if self.state[6] == self.state[4] == self.state[2]:
			return self.state[6]
		# No one won
		return self.EMPTY

	def is_full(self):
		# Check if there are no empty spaces left
		return self.EMPTY not in self.state

	def is_empty(self, row, col):
		return self.state[row*3 + col] == self.EMPTY

	def play(self, player, row, col):
		if self.state[row*3 + col] != self.EMPTY:
			raise ValueError("Tried placing a piece in a non-free space!")
		else:
			self.state[row*3 + col] = player

	def unplay(self, row, col):
		self.state[row*3 + col] = self.EMPTY

	def get_available_moves(self):
		return [(i // 3, i % 3) for i in range(9) if self.state[i] == self.EMPTY]


class Piece(glooey.Button):
	custom_alignment = 'fill'

	class Foreground(glooey.Image):
		pass

	class Base(glooey.Background):
		custom_color = '#000000'

	class Over(glooey.Background):
		custom_color = '#777777'
		custom_outline = '#ff0000'

	def __init__(self, row, col, callback):
		super().__init__()
		self.row = row
		self.col = col
		self.callback = callback
		self.used = False

	def on_click(self, widget):
		if not self.used:
			self.callback(self.row, self.col)


class GridObject(glooey.Grid):
	# NEUTRAL_COLOR = '#777777'
	# PLAYER1_COLOR = '#ff0000'
	# PLAYER2_COLOR = '#0000ff'
	PLAYER1_IMAGE = pyglet.resource.image('assets/round.png')
	PLAYER2_IMAGE = pyglet.resource.image('assets/cross.png')

	def __init__(self, state, callback):
		super().__init__(3, 3)
		for i in range(3):
			for j in range(3):
				button = Piece(i, j, callback)
				self.add(i, j, button)

	def update(self, last_move, player):
		row, col = last_move
		# self[row, col].base_background.color = self.PLAYER1_COLOR if player == Grid.PLAYER1 else self.PLAYER2_COLOR
		self[row, col].foreground = glooey.Image(image=self.PLAYER1_IMAGE if player == Grid.PLAYER1 else self.PLAYER2_IMAGE)
		self[row, col].used = True


class TicTacToeObject:

	def __init__(self, gui, player1, player2):
		self.players = (player1, player2)
		self.current_player_index = 0
		self.current_player = self.players[self.current_player_index]

		self.game_over = False

		self.state = Grid()
		self.grid_object = GridObject(self.state, self.on_user_interaction)
		gui.add(self.grid_object)

	def on_user_interaction(self, row, col):
		self.current_player.on_user_interaction(row, col)

	def update(self):
		if not self.state.game_over():
			if self.current_player.ready:
				move = self.current_player.get_next_move(self.state)
				self.state.play(self.current_player.piece, *move)
				self.grid_object.update(move, self.current_player.piece)

				self.current_player_index = (self.current_player_index + 1) % 2
				self.current_player = self.players[self.current_player_index]
		else:
			self.game_over = True
			winner = self.state.has_won()
			if winner == Grid.PLAYER1:
				print('Player 1 has won!')
			elif winner == Grid.PLAYER2:
				print('Player 2 has won!')
			else:
				print('No one won.')


class TicTacToe(Scene):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.game = None
		self.game_container = None

	def load(self):
		self.game_container = glooey.Bin()
		player1 = HumanPlayer(Grid.PLAYER1, Grid.PLAYER2)
		player2 = HumanPlayer(Grid.PLAYER2, Grid.PLAYER1)
		self.game = TicTacToeObject(self.game_container, player1, player2)

	def begin(self):
		self.gui.clear()
		self.load()
		self.gui.add(self.game_container)

	def end(self):
		self.gui.clear()

	def run(self, dt):
		if not self.game.game_over:
			self.game.update()

	def draw(self):
		self.gui.batch.draw()
