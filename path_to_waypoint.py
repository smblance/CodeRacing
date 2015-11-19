from convenience import *
from itertools import product

def path_to_waypoint(cur_tile, waypoint, tiles_x_y):
	left, right, top, bot = (-1,0), (1,0), (0,-1), (0,1)
	type_exits = {
        0 : [],
        1 : [top, bot],
        2 : [left, right],
        3 : [right, bot],
        4 : [left, bot],
        5 : [right, top],
        6 : [left, top],
        7 : [left, top, bot],
        8 : [right, top, bot],
        9 : [left, right, top],
        10 : [left, right, bot],
        11 : [left, right, top, bot],
        12 : [left, right, top, bot]
    	}

	if abs_distance(cur_tile, waypoint) == 1:
		return [cur_tile, waypoint]


	for row in tiles_x_y:
		if 12 in row:
			min_dist = 1000
			for exit in type_exits[ tiles_x_y[cur_tile[0]][cur_tile[1]] ]:
				if distance(cur_tile, waypoint)[0] * exit[0] >= 0 and distance(cur_tile,waypoint)[1] * exit[1] >= 0:
					return [cur_tile, adj_tile(cur_tile,exit)]

	paths = [[cur_tile]]
	while [path[-1] for path in paths] != [waypoint]*len(paths):
		new_paths = []
		for path in paths:
			tile = path[-1]
			if tile != waypoint:
				for exit in type_exits[ tiles_x_y[tile[0]][tile[1]] ]:
					if distance(tile, waypoint)[0] * exit[0] >= 0 and distance(tile,waypoint)[1] * exit[1] >= 0:
						if adj_tile(tile, exit) not in path:
							new_paths.append(path + [adj_tile(tile,exit)])
			else:
				new_paths.append(path)
		paths = new_paths

	min_length = len(tiles_x_y) * len(tiles_x_y[0])

	for path in paths:
		if len(path) < min_length:
			path_to_waypoint = path
			min_length = len(path)

	return path_to_waypoint