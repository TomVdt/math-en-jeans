import pyglet
import glooey
from math_en_jeans.scenes.scene import Scene
from math_en_jeans.ui import *


class MainMenu(Scene):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.container = None

	def load(self):
		# UI AND STUFF
		self.background = Background()
		self.container = glooey.VBox()
		self.grid = PaddedGrid(2, 2)

		self.header = Header('MATh.en.JEANS')

		self.tictactoe_card = Card(description='Tic-tac-toe, the well known pen-and-paper game.', image=pyglet.resource.image('assets/tictactoe.png'))
		self.tictactoe_button = Button('Start', callback=self.to_tictactoe)
		self.tictactoe_card.pack(self.tictactoe_button)
		self.achi_card = Card(description='Achi is similar to Tic-tac-toe, but with a twist!', image=pyglet.resource.image('assets/achi.png'))
		self.achi_button = Button('Start', callback=self.to_achi)
		self.achi_card.pack(self.achi_button)
		self.picaria_card = Card(description='Picaria is a variation of Achi that allows more movement.', image=pyglet.resource.image('assets/picaria.png'))
		self.picaria_button = Button('Start', callback=self.to_picaria)
		self.picaria_card.pack(self.picaria_button)

		self.extra = glooey.VBox()
		self.extra.set_alignment('fill bottom')
		self.credits = Label('Programming by Tom Vdt')
		self.github_container = glooey.HBox()
		self.github_container.set_alignment('center')
		self.github_icon = Image(image=pyglet.resource.image('assets/github.png'), responsive=True)
		self.github_url = Url(text='GitHub', link='https://github.com/TomVdt/math-en-jeans')
		self.github_container.add(self.github_icon)
		self.github_container.add(self.github_url)
		self.exit_button = Button('Exit', callback=pyglet.app.exit)
		self.extra.pack(self.credits)
		self.extra.pack(self.github_container)
		self.extra.pack(self.exit_button)

		self.grid.add(0, 0, self.tictactoe_card)
		self.grid.add(0, 1, self.achi_card)
		self.grid.add(1, 0, self.picaria_card)
		self.grid.add(1, 1, self.extra)

		self.container.add(self.header, size=50)
		self.container.add(self.grid)
		self.background.add(self.container)

	def to_tictactoe(self):
		self.window.switch_to_scene('tictactoe')

	def to_achi(self):
		self.window.switch_to_scene('achi')

	def to_picaria(self):
		self.window.switch_to_scene('picaria')

	def begin(self):

		self.gui.clear()
		self.load()
		self.gui.add(self.background)

	def end(self):
		self.gui.clear()

	def draw(self):
		self.gui.batch.draw()

	def run(self, dt):
		return
