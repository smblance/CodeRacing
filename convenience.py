def adj_tile(tile, direction):
    return (tile[0] + direction[0], tile[1] + direction[1])

def distance(tile_1, tile_2):
    return (tile_2[0] - tile_1[0], tile_2[1] - tile_1[1])

def abs_distance(tile_1, tile_2):
	return (abs(tile_2[0] - tile_1[0]) + abs(tile_2[1] - tile_1[1]))

def ttype(tile, world):
	return world.tiles_x_y[tile[0]][tile[1]]

def sign(x):
	if x >= 0:
		return 1
	if x < 0:
		return -1