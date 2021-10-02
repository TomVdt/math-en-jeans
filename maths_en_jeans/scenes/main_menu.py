from pyglet.app import exit
import glooey
from maths_en_jeans.scenes.scene import Scene
from maths_en_jeans.scenes.ui import Button


class MainMenu(Scene):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.container = None
		self.button_container = None

		self.tictactoe_button = None
		self.hatchi_button = None
		self.picaria_button = None
		self.exit_button = None

	def load(self):
		# UI AND STUFF
		self.container = glooey.Grid(3, 3)
		self.button_container = glooey.VBox()

		self.tictactoe_button = Button('Tic-Tac-Toe', callback=self.to_tictactoe)
		self.hatchi_button = Button('Hatchi', callback=self.to_hatchi)
		self.picaria_button = Button('Picaria', callback=self.to_picaria)
		self.exit_button = Button('Exit', callback=exit)

		self.button_container.add(self.tictactoe_button)
		self.button_container.add(self.hatchi_button)
		self.button_container.add(self.picaria_button)
		self.button_container.add(self.exit_button)

		self.container.add(1, 1, self.button_container)

	def to_tictactoe(self):
		self.window.switch_to_scene('tictactoe')

	def to_hatchi(self):
		self.window.switch_to_scene('hatchi')

	def to_picaria(self):
		self.window.switch_to_scene('picaria')

	def begin(self):

		self.gui.clear()

		self.load()

		self.gui.add(self.container)

	def end(self):
		return

	def draw(self):
		self.gui.batch.draw()

	def run(self, dt):
		return
