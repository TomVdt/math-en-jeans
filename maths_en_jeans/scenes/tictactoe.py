import pyglet
import glooey

from maths_en_jeans.scenes.scene import Scene
from maths_en_jeans.players import *
from maths_en_jeans.ui import *


class Grid:
	EMPTY = 0
	PLAYER1 = 1
	PLAYER2 = -1

	def __init__(self, state=None):
		self.state = state or [0 for i in range(9)]

	def __iter__(self):
		return iter(self.state)

	def __repr__(self):
		new_lst = ['' for i in range(9)]
		for i, piece in enumerate(self.state):
			new_lst[i] = {self.EMPTY: ' ', self.PLAYER1: 'o', self.PLAYER2: 'x'}[piece]
		return '{}|{}|{}\n-+-+-\n{}|{}|{}\n-+-+-\n{}|{}|{}'.format(*new_lst)

	def game_over(self):
		return (self.has_won() != self.EMPTY) or self.is_full()

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

	def is_empty(self, row, col):
		return self.state[row*3 + col] == self.EMPTY

	def play(self, player, row, col):
		if self.state[row*3 + col] != self.EMPTY:
			raise ValueError("Tried placing a piece in a non-free space!")
		else:
			self.state[row*3 + col] = player

	def unplay(self, row, col):
		self.state[row*3 + col] = self.EMPTY

	def reset(self):
		self.state = [0 for i in range(9)]

	def get_available_moves(self):
		return [(i // 3, i % 3) for i in range(9) if self.state[i] == self.EMPTY]


class Piece(Button):
	custom_alignment = 'fill'
	custom_padding = 8

	class Foreground(glooey.Image):
		pass

	def __init__(self, row, col, callback):
		super().__init__(callback=callback, callback_args=(row, col))
		self.row = row
		self.col = col


class GridObject(glooey.Grid):
	custom_alignment = keep_square
	custom_padding = 8
	PLAYER1_IMAGE = pyglet.resource.image('assets/round.png')
	PLAYER2_IMAGE = pyglet.resource.image('assets/cross.png')

	def __init__(self, callback):
		super().__init__(3, 3)
		self.callback = callback
		self.populate()

	def update(self, last_move, player):
		row, col = last_move
		self[row, col].foreground = glooey.Image(image=self.PLAYER1_IMAGE if player == Grid.PLAYER1 else self.PLAYER2_IMAGE)
		self[row, col].callback = None

	def populate(self):
		for i in range(3):
			for j in range(3):
				button = Piece(i, j, self.callback)
				self.add(i, j, button)

	def reset(self):
		for child in self._children:
			self[child].foreground = Piece.Foreground()
			self[child].callback = self.callback


class TicTacToe(Scene):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.game = None
		self.container = None

		self.header = None

		self.game_container = None
		self.game = None

		self.options_bg = None
		self.options_menu = None
		self.options_label = None
		self.options_cycle = None

		# Game logic
		self.player1 = None
		self.player2 = None
		self.players = None
		self.current_player_index = None
		self.current_player = None

		self.game_over = True

		self.state = None
		self.grid_object = None

	def start_game(self):
		if not self.game_over:
			self.reset_game()
		bot = {'Minimax': MinimaxPlayer, 'Random': RandomPlayer}[self.options_type.state]
		if self.options_p1.state == 'Human':
			self.player1 = HumanPlayer(Grid.PLAYER1, Grid.PLAYER2)
			self.player2 = bot(Grid.PLAYER2, Grid.PLAYER1)
		else:
			self.player1 = bot(Grid.PLAYER1, Grid.PLAYER2)
			self.player2 = HumanPlayer(Grid.PLAYER2, Grid.PLAYER1)
		self.players = (self.player1, self.player2)
		self.current_player_index = 0
		self.current_player = self.players[self.current_player_index]

		self.game_over = False

		self.state = Grid()

	def reset_game(self):
		self.grid.reset()
		self.state = None
		self.player1 = None
		self.player2 = None
		self.players = None
		self.game_over = True
		self.header.foreground.text = 'Tic-Tac-Toe'

	def load(self):
		# UI stuff
		self.container = glooey.VBox()

		# Header
		self.header = Header('Tic-Tac-Toe')

		# Game
		self.game_container = GameContainer()
		self.game_bg = Color('#e1e2e1')
		self.grid = GridObject(self.on_user_interaction)
		self.game_container.add(self.game_bg)
		self.game_container.add(self.grid)

		# Options menu
		self.options_bg = Background()
		self.options_menu = Menu()
		self.options_params_container = Menu()
		self.options_control_container = Menu()
		self.options_p1_label = Label('1st player:')
		self.options_p1 = Cycle(['Human', 'Bot'])
		self.options_type_label = Label('Bot type:')
		self.options_type = Cycle(['Minimax', 'Random'])
		self.options_reset = Button('Reset Game', callback=self.reset_game)
		self.options_start = Button('Start Game', callback=self.start_game)
		self.options_params_container.pack(self.options_p1_label)
		self.options_params_container.pack(self.options_p1)
		self.options_params_container.pack(glooey.Spacer(min_width=10))
		self.options_params_container.pack(self.options_type_label)
		self.options_params_container.pack(self.options_type)
		self.options_control_container.pack(self.options_reset)
		self.options_control_container.pack(self.options_start)
		self.options_menu.pack(self.options_params_container)
		self.options_menu.add(glooey.Spacer())
		self.options_menu.pack(self.options_control_container)
		self.options_bg.add(self.options_menu)

		# Put everything together
		self.container.add(self.header, size=50)
		self.container.add(self.game_container)
		self.container.add(self.options_bg, size=50)

	def begin(self):
		self.gui.clear()
		self.load()
		self.gui.add(self.container)

	def end(self):
		self.reset_game()
		self.game_over = True
		self.gui.clear()

	def on_user_interaction(self, row, col):
		if self.game_over:
			self.reset_game()
			self.start_game()
		self.current_player.on_user_interaction(row, col)

	def on_game_over(self, msg):
		self.header.foreground.text = msg

	def update(self):
		if not self.state.game_over():
			if self.current_player.ready:
				move = self.current_player.get_next_move(self.state)
				self.state.play(self.current_player.piece, *move)
				self.grid.update(move, self.current_player.piece)

				self.current_player_index = (self.current_player_index + 1) % 2
				self.current_player = self.players[self.current_player_index]
		else:
			self.game_over = True
			winner = self.state.has_won()
			if winner == Grid.PLAYER1:
				msg = 'Player 1 (o) has won!'
			elif winner == Grid.PLAYER2:
				msg = 'Player 2 (x) has won!'
			else:
				msg = 'No one won.'
			self.on_game_over(msg)

	def run(self, dt):
		if not self.game_over:
			self.update()

	def draw(self):
		self.gui.batch.draw()
