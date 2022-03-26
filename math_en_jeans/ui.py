__all__ = ['Label', 'Title', 'Header', 'Url', 'Info', 'Button', 'Cycle', 'Menu', 'Card', 'Background', 'Image', 'PaddedGrid', 'GameContainer', 'Color', 'expand_if_close', 'keep_square']

import webbrowser
import glooey


def expand_if_close(widget, widget_rect, max_rect):
	if widget_rect.width > max_rect.width * 0.85:
		widget_rect.width = max_rect.width
		widget_rect.height = max_rect.height
	widget_rect.bottom_left = max_rect.bottom_left


def keep_square(widget, widget_rect, max_rect):
	side = min(max_rect.width, max_rect.height)
	widget_rect.width = side
	widget_rect.height = side
	widget_rect.center = max_rect.center


def clamp_600(widget, widget_rect, max_rect):
	if max_rect.width * 0.8 > 600:
		widget_rect.width = 600
	else:
		widget_rect.width = max_rect.width * 0.8
	widget_rect.center = max_rect.center


class Color(glooey.Background):

	def __init__(self, color, **kwargs):
		super().__init__(color=color, **kwargs)


class Background(glooey.Stack):
	custom_alignment = 'fill'

	def __init__(self, *args, color=None, **kwargs):
		super().__init__(*args, **kwargs)
		self.color = Color(color=color or '#29434e')
		self.add_back(self.color)


class Image(glooey.Image):
	custom_padding = 8


class Label(glooey.Label):
	custom_color = '#ffffff'
	custom_alignment = 'center'
	custom_font_size = 12
	custom_padding = 8


class Title(glooey.Label):
	custom_color = '#ffffff'
	custom_alignment = 'center'
	custom_font_size = 24
	custom_padding = 16
	custom_underline = True


class Header(glooey.Stack):
	Foreground = Title

	class Background(glooey.Background):
		custom_color = '#29434e'

	def __init__(self, text, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.foreground = self.Foreground(text=text)
		self.background = self.Background()
		self.add(self.background)
		self.add(self.foreground)


class Url(glooey.Button):
	Foreground = Label
	custom_alignment = 'fill'

	def __init__(self, text, link):
		super().__init__(text=text, color='#58a6ff')
		self.link = link

	def on_click(self, widget):
		webbrowser.open(self.link)

	def on_mouse_enter(self, x, y):
		self.foreground.color = '#5094cc'

	def on_mouse_leave(self, x, y):
		self.foreground.color = '#58a6ff'


class Button(glooey.Button):
	Foreground = Label
	custom_alignment = 'fill'

	class Base(glooey.Background):
		custom_color = '#29434e'

	class Over(glooey.Background):
		custom_color = '#546e7a'

	class Down(glooey.Background):
		custom_color = '#819ca9'

	def __init__(self, *args, callback=None, callback_args=None, **kwargs):
		super().__init__(*args, **kwargs)
		self.callback = callback
		self.callback_args = callback_args

	def on_click(self, widget):
		if self.callback is not None:
			if self.callback_args is not None:
				self.callback(*self.callback_args)
			else:
				self.callback()


class Cycle(glooey.Button):
	Foreground = Label
	custom_alignment = 'fill'

	class Base(glooey.Background):
		custom_color = '#29434e'

	class Over(glooey.Background):
		custom_color = '#546e7a'

	class Down(glooey.Background):
		custom_color = '#819ca9'

	def __init__(self, states, *args, callback=None, callback_args=None, **kwargs):
		super().__init__(*args, **kwargs)
		self.states = states
		self.state_index = 0
		self.state = states[0] if states else None
		self.foreground.text = self.states[self.state_index]

		self.callback = callback
		self.callback_args = callback_args

	def on_click(self, widget):
		self.state_index = (self.state_index + 1) % len(self.states)
		self.state = self.states[self.state_index]
		self.foreground.text = self.state
		if self.callback is not None:
			if self.callback_args is not None:
				self.callback(*self.callback_args)
			else:
				self.callback()

	def do_claim(self):
		max_x, max_y = 0, 0
		for text in self.states:
			test_label = self.Foreground(text)
			text_width, text_height = test_label.do_claim()
			max_x = max(max_x, text_width + test_label.top_padding + test_label.bottom_padding)
			max_y = max(max_y, text_height + test_label.left_padding + test_label.right_padding)
		return max_x, max_y


class Menu(glooey.HBox):
	custom_alignment = 'fill'


class Card(Background):
	Description = Label
	Button = Button
	Image = Image

	def __init__(self, image=None, description=None):
		super().__init__(color='#546e7a')
		self.container = glooey.VBox()
		self._desc = description
		if image is not None:
			self.image = self.Image(image, responsive=True)
			self.container.add(self.image)
		else:
			self.image = None
		if description is not None:
			self.description = self.Description()
			self.container.pack(self.description)
		else:
			self.description = None
		self.add_front(self.container)

	def do_regroup_children(self):
		# Hack to allow dynamically changing linewrap
		if self.description is not None:
			self.description.enable_line_wrap(self.rect.width - 20)
			self.description.text = self._desc
		super().do_regroup_children()

	def add(self, *args, **kwargs):
		self.container.add(*args, **kwargs)

	def pack(self, *args, **kwargs):
		self.container.pack(*args, **kwargs)


class Info(glooey.ButtonDialog):
	custom_autoadd_content = True
	custom_alignment = clamp_600
	Content = Label
	OkButton = Button

	class Buttons(glooey.HBox):
		custom_alignment = 'right'
		custom_padding = 8

	class Decoration(glooey.Background):
		custom_color = '#819ca9'
		custom_outline = '#29434e'

	def __init__(self, text):
		super().__init__()
		self.text = text
		self.ok_button = self.OkButton(text='OK')
		self.ok_button.push_handlers(on_click=self.on_click_ok)
		self.buttons.pack(self.ok_button)

	def on_click_ok(self, widget):
		self.close()

	def do_regroup_children(self):
		# Hack to allow dynamically changing linewrap
		if self.content is not None:
			self.content.enable_line_wrap(self.rect.width - 20)
			self.content.text = self.text
		super().do_regroup_children()


class PaddedGrid(glooey.Grid):
	custom_cell_padding = 8


class GameContainer(glooey.Stack):
	pass


if __name__ == '__main__':
	import pyglet

	win = pyglet.window.Window(500, 500)
	gui_batch = pyglet.graphics.Batch()
	gui = glooey.Gui(win, batch=gui_batch)

	magik = GameContainer()
	container = glooey.VBox()
	buttons = glooey.HBox()

	header = Header('a header thats not a header')
	label = Label('haha funny label')
	para = Label('haha funny label that has a lot of text i need inspiration so maybe i can just ask but that wouldnt be based i wonder if this is enough', 450)

	button = Button('button that does stuff', callback=lambda x: print(x), callback_args=['this works'])
	cycle = Cycle(['is this funny?', 'i think it is!'])

	buttons.add(button)
	buttons.add(cycle)

	overlay = Info('text here plz')

	bg = Background()
	menu = Menu()
	bg.add(menu)
	lab1 = Label('number 1')
	but1 = Button('issou', callback=lambda: overlay.open(gui))
	cycl = Cycle(['1', '2', '3', 'viva l\'algérie'])
	menu.pack(lab1)
	menu.pack(but1)
	menu.pack(cycl)

	container.add(header)
	container.add(label)
	container.add(para)
	container.add(buttons)
	container.pack(bg)

	magik.add(container)

	gui.add(magik)

	@win.event
	def on_draw():
		win.clear()
		gui_batch.draw()

	pyglet.app.run()
