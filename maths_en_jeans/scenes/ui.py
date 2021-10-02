import glooey


class ButtonLabel(glooey.Label):
	custom_alignment = 'center'
	custom_text_alignment = 'center'
	custom_font_size = 26


class Button(glooey.Button):
	Foreground = ButtonLabel
	custom_alignment = 'fill'

	def __init__(self, label, callback=None, *args, **kwargs):
		super().__init__(label, *args, **kwargs)
		self.callback = callback

	def on_click(self, widget):
		if self.callback is not None:
			self.callback()

	class Base(glooey.Background):
		custom_color = 'ffffff'

	class Over(glooey.Background):
		custom_color = 'dddddd'

	class Down(glooey.Background):
		custom_color = 'bbbbbb'
