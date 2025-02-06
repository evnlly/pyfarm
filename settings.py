from pygame.math import Vector2
# screen
screen_width = 720
screen_height = 720
tile_size = 64

player_tool_offset = {
	'left': Vector2(-50, 40),
	'right': Vector2(50, 40),
	'up': Vector2(0, -10),
	'down': Vector2(0, 50)
}

layers = {
	'ground': 1,
	'house bottom': 5,
	'ground plant': 6,
	'main': 7,
	'house top': 8,
	'tree': 9
}
