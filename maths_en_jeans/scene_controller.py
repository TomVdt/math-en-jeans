import pyglet
from pyglet.window import key
import glooey

from maths_en_jeans.options import options
from maths_en_jeans.scenes.main_menu import MainMenu
from maths_en_jeans.scenes.tictactoe import TicTacToe
from maths_en_jeans.scenes.hatchi import Hatchi
from maths_en_jeans.scenes.picaria import Picaria


class SceneController(pyglet.window.Window):

	def __init__(self, *args, **kwargs):
		super().__init__(options['width'], options['height'], *args, **kwargs)

		# Important settings
		self.set_minimum_size(options['width'], options['height'])
		self.frame_rate = 1 / 60.0

		# Click event stuff
		self.register_event_type('on_click')
		self.mouse_press_x = 0
		self.mouse_press_y = 0

		# For the GUI
		self.gui_batch = pyglet.graphics.Batch()
		self.gui_group = pyglet.graphics.Group()
		self.gui = glooey.Gui(self, batch=self.gui_batch, group=self.gui_group)

		# Set up scene management
		self.scene_stack = []
		self.scenes = {
			'menu': MainMenu(self, self.gui),
			'tictactoe': TicTacToe(self, self.gui),
			'hatchi': Hatchi(self, self.gui),
			'picaria': Picaria(self, self.gui),
		}

		self.switch_to_scene('menu')

	def pop_scene(self) -> bool:
		# verify there is at least 1 scene to remove from the stack
		if len(self.scene_stack) > 0:
			self.remove_handlers(self.scene_stack[-1])
			self.scene_stack[-1].end()
			self.scene_stack.pop(-1)

		# show the scene on top of the stack, if it exists
		if len(self.scene_stack) > 0:
			self.scene_stack[-1].begin()
			return True
		else:
			return False

	def switch_to_scene(self, scene_id: str) -> None:
		if len(self.scene_stack) > 0:
			self.scene_stack[-1].end()

		self.scene_stack.append(self.scenes[scene_id])
		self.scene_stack[-1].begin()
		self.push_handlers(self.scene_stack[-1])

	def on_key_press(self, symbol, modifier):
		if symbol == key.ESCAPE:
			if not self.pop_scene():
				pyglet.app.exit()
		if symbol == key.F4 and modifier & key.MOD_ALT:
			pyglet.app.exit()

	def on_mouse_press(self, x, y, buttons, modifiers):
		self.mouse_press_x = x
		self.mouse_press_y = y

	def on_mouse_release(self, x, y, buttons, modifiers):
		if self.mouse_press_x == x and self.mouse_press_y == y:
			self.dispatch_event('on_click', x, y)

	def on_draw(self):
		self.clear()
		if len(self.scene_stack) > 0:
			self.scene_stack[-1].draw()

	def update(self, dt):
		if len(self.scene_stack) > 0:
			self.scene_stack[-1].run(dt)
