import pyglet
import glooey

from maths_en_jeans.scenes.scene import Scene
from maths_en_jeans.grid import TicTacToeGrid, Piece
from maths_en_jeans.players import *
from maths_en_jeans.ui import *


class PieceButton(Button):
	custom_alignment = 'fill'
	custom_padding = 8

	class Foreground(glooey.Image):
		pass

	def __init__(self, index, callback):
		super().__init__(callback=callback, callback_args=(index,))


class GameGrid(glooey.Grid):
	custom_alignment = keep_square
	custom_padding = 8
	PLAYER1_IMAGE = pyglet.resource.image('assets/round.png')
	PLAYER2_IMAGE = pyglet.resource.image('assets/cross.png')

	def __init__(self, callback):
		super().__init__(3, 3)
		self.callback = callback
		self.populate()

	def update(self, last_move, player):
		index = last_move
		self[index // 3, index % 3].foreground = glooey.Image(image=self.PLAYER1_IMAGE if player == Piece.PLAYER1 else self.PLAYER2_IMAGE)

	def populate(self):
		for i in range(3):
			for j in range(3):
				button = PieceButton(i*3 + j, self.callback)
				self.add(i, j, button)

	def reset(self):
		for child in self._children:
			self[child].foreground = PieceButton.Foreground()


class TicTacToe(Scene):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.game = None
		self.container = None

		self.header = None

		self.game_container = None
		self.game_bg = None
		self.game = None

		self.options_bg = None
		self.options_menu = None
		self.options_params_container = None
		self.options_control_container = None
		self.options_player1_label = None
		self.options_player1 = None
		self.options_player2_label = None
		self.options_player2 = None
		self.options_reset = None
		self.options_start = None

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
		self.reset_game()
		self.player1 = {'Human': HumanPlayer, 'Minimax': MinimaxPlayer, 'Random': RandomPlayer}[self.options_player1.state](Piece.PLAYER1, Piece.PLAYER2)
		self.player2 = {'Human': HumanPlayer, 'Minimax': MinimaxPlayer, 'Random': RandomPlayer}[self.options_player2.state](Piece.PLAYER2, Piece.PLAYER1)
		self.players = (self.player1, self.player2)
		self.current_player_index = 0
		self.current_player = self.players[self.current_player_index]

		self.game_over = False

		self.state = TicTacToeGrid()

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
		self.grid = GameGrid(self.on_user_interaction)
		self.game_container.add(self.game_bg)
		self.game_container.add(self.grid)

		# Options menu
		self.options_bg = Background()
		self.options_menu = Menu()
		self.options_params_container = Menu()
		self.options_control_container = Menu()
		self.options_player1_label = Label('Player 1: ')
		self.options_player1 = Cycle(['Human', 'Minimax', 'Random'])
		self.options_player2_label = Label('Player 2: ')
		self.options_player2 = Cycle(['Minimax', 'Human', 'Random'])
		self.options_reset = Button('Reset Game', callback=self.reset_game)
		self.options_start = Button('Start Game', callback=self.start_game)
		self.options_params_container.pack(self.options_player1_label)
		self.options_params_container.pack(self.options_player1)
		self.options_params_container.pack(self.options_player2_label)
		self.options_params_container.pack(self.options_player2)
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
		self.gui.clear()

	def on_user_interaction(self, index):
		if self.game_over:
			self.start_game()
		if self.state.is_valid_move(index, self.current_player.piece):
			self.current_player.set_move(index)

	def on_game_over(self, msg):
		self.header.foreground.text = msg

	def run(self, dt):
		if not self.game_over:
			if self.current_player.ready:
				move = self.current_player.get_next_move(self.state)
				self.state.play(self.current_player.piece, move)
				self.grid.update(move, self.current_player.piece)

				self.current_player_index = (self.current_player_index + 1) % 2
				self.current_player = self.players[self.current_player_index]

				self.game_over = self.state.game_over()
				if self.game_over:
					winner = self.state.has_won()
					if winner == Piece.PLAYER1:
						msg = 'Player 1 (o) has won!'
					elif winner == Piece.PLAYER2:
						msg = 'Player 2 (x) has won!'
					else:
						msg = 'No one won.'
					self.on_game_over(msg)

	def draw(self):
		self.gui.batch.draw()
