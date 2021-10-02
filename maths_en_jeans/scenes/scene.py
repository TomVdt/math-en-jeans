import pyglet


class Scene(pyglet.event.EventDispatcher):

	def __init__(self, window, gui, *args, **kwargs):
		super().__init__()
		self.window = window
		self.gui = gui

	def begin(self):
		return
		# raise NotImplementedError('abstract')

	def end(self):
		return
		# raise NotImplementedError('abstract')

	def load(self):
		return
		# raise NotImplementedError('abstract')

	def draw(self):
		return
		# raise NotImplementedError('abstract')

	def run(self, dt):
		pass
