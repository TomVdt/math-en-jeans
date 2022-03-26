

def main():
	import os
	import pyglet
	from math_en_jeans.scene_controller import SceneController

	pyglet.resource.path = [os.getcwd() + '/math_en_jeans']
	pyglet.resource.reindex()

	window = SceneController(caption='Math-en-Jeans', resizable=True)
	pyglet.clock.schedule_interval(window.update, window.frame_rate)

	try:
		pyglet.app.run()
	except KeyboardInterrupt:
		print('\nExited ungracefully. Goodbye.')


if __name__ == '__main__':
	main()
