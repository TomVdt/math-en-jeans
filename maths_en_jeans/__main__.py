

def main():
	import os
	import pyglet
	from maths_en_jeans.scene_controller import SceneController

	pyglet.resource.path = [os.getcwd() + '/maths_en_jeans']
	pyglet.resource.reindex()

	window = SceneController(caption='Maths-en-Jeans', resizable=True)
	pyglet.clock.schedule_interval(window.update, window.frame_rate)

	pyglet.app.run()


if __name__ == '__main__':
	main()
