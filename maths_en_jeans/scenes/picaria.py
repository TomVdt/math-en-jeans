import pyglet
import glooey

from maths_en_jeans.scenes.scene import Scene
from maths_en_jeans.grid import PicariaGrid, Piece
from maths_en_jeans.players import *
from maths_en_jeans.ui import *


RULES = """How to play:
- Each player gets 3 pieces
- Every player takes turns to place 1 of their pieces, everywhere except the very middle
- Once all pieces are placed, you may only move pieces according to the lines
- If someone aligns 3 pieces, they win!
WARNING: the MiniMax algorithm does not work well with this game due to it's "openess" compared to the other two. Expect slow / unusable performance"""


class PieceButton(Button):
	custom_alignment = 'fill'

	class Foreground(glooey.Image):
		pass

	def __init__(self, index, callback):
		super().__init__(callback=callback, callback_args=(index,))


class GameGrid(glooey.Grid):
	custom_alignment = keep_square
	custom_padding = 8
	custom_cell_padding = 8
	PLAYER1_IMAGE = pyglet.resource.image('assets/round.png')
	PLAYER2_IMAGE = pyglet.resource.image('assets/cross.png')
	MAPPING = {
		0: (0, 0), 2: (0, 2), 4: (0, 4),
		6: (1, 1), 8: (1, 3),
		10: (2, 0), 12: (2, 2), 14: (2, 4),
		16: (3, 1), 18: (3, 3),
		20: (4, 0), 22: (4, 2), 24: (4, 4)
	}

	def __init__(self, callback):
		super().__init__(5, 5)
		self.callback = callback
		self.PLAYER1_IMAGE.width, self.PLAYER1_IMAGE.height = 80, 80
		self.PLAYER2_IMAGE.width, self.PLAYER2_IMAGE.height = 80, 80
		self.populate()

	def update(self, last_move, player):
		move_type, old_index, new_index = last_move
		self[self.MAPPING[new_index]].foreground = glooey.Image(image=self.PLAYER1_IMAGE if player == Piece.PLAYER1 else self.PLAYER2_IMAGE)
		if move_type == 'move':
			self[self.MAPPING[old_index]].foreground = PieceButton.Foreground()

	def populate(self):
		for i in range(0, 25, 2):
			button = PieceButton(i, self.callback)
			self.add(*self.MAPPING[i], button)

	def reset(self):
		for child in self._children:
			self[child].foreground = PieceButton.Foreground()


class Picaria(Scene):

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
		self.pending_move = None
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

		self.state = PicariaGrid()

	def reset_game(self):
		self.grid.reset()
		self.state = None
		self.player1 = None
		self.player2 = None
		self.players = None
		self.game_over = True
		self.move_origin = -1
		self.header.foreground.text = 'Picaria'

	def load(self):
		# UI stuff
		self.container = glooey.VBox()

		# Header
		self.header = Header('Picaria')

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
		self.options_info = Button('Info', callback=self.show_info)
		self.options_reset = Button('Reset Game', callback=self.reset_game)
		self.options_start = Button('Start Game', callback=self.start_game)
		self.options_params_container.pack(self.options_player1_label)
		self.options_params_container.pack(self.options_player1)
		self.options_params_container.pack(self.options_player2_label)
		self.options_params_container.pack(self.options_player2)
		self.options_control_container.pack(self.options_info)
		self.options_control_container.pack(self.options_reset)
		self.options_control_container.pack(self.options_start)
		self.options_menu.pack(self.options_params_container)
		self.options_menu.add(glooey.Spacer())
		self.options_menu.pack(self.options_control_container)
		self.options_bg.add(self.options_menu)

		# Info overlay
		self.info = Info(RULES)

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
		# Validate move before continuing
		phase = self.state.get_game_phase()
		if phase == 'tictactoe':
			move = ('new', 0, index)
		else:
			# Invalid move as placeholder
			move = ('invalid', -1, -1)
			if self.move_origin == -1:
				if not self.state.is_free(index):
					self.move_origin = index
			else:
				if self.state.is_free(index):
					move = ('move', self.move_origin, index)
					self.move_origin = -1

		if self.state.is_valid_move(move, self.current_player.piece):
			self.current_player.set_move(move)

	def on_game_over(self, msg):
		self.header.foreground.text = msg

	def show_info(self):
		self.info.open(self.gui)

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
