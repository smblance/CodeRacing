from math import sin, cos
from convenience import adj_tile, distance


def map_path(world, me, file = None):
    tiles_x_y = world.tiles_x_y
    waypoints = [tuple(x) for x in (world.waypoints + [world.waypoints[0]]) ]
    starting_direction = (int(round(cos(me.angle))),int(round(-sin(me.angle))))
    path = [waypoints[0]]
    entry_direction = starting_direction

    for n in range(1, len(waypoints)):
        shortest_path_between_wp = shortest_path_between_tiles(tiles_x_y, waypoints[n-1], waypoints[n], entry_direction)
        if shortest_path_between_wp != None:
            path.extend(shortest_path_between_wp)
            entry_direction = distance(path[-2], path[-1])
    
    if file != None:
        with open(file, 'rb+') as f:
            for tile in path:
                f.write(str(tile))
                f.write('\n')

    return path

def shortest_path_between_tiles(tiles_x_y, tile_1, tile_2, entry_direction):
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

    cur_tile = tile_1
    if tiles_x_y[cur_tile[0]][cur_tile[1]] == 12:
        return None
    paths = []
    for exit_direction in type_exits[tiles_x_y[cur_tile[0]][cur_tile[1]]]:
        if exit_direction != (-entry_direction[0], -entry_direction[1]):
            paths.append([cur_tile, adj_tile(cur_tile, exit_direction)])
    while [path[-1] for path in paths] != [tile_2]*len(paths):
        new_paths = []
        for path in paths:
            if path[-1] != tile_2:
                cur_tile = path[-1]
                cur_tile_type = tiles_x_y[cur_tile[0]][cur_tile[1]]
                print cur_tile, cur_tile_type
                if cur_tile_type == 12:
                    return get_shortest_path(paths, tiles_x_y)
                good_exit_directions = []
                for exit_direction in type_exits[cur_tile_type]:
                    if adj_tile(cur_tile, exit_direction) not in path:
                        good_exit_directions.append(exit_direction)
                for exit_direction in good_exit_directions:
                    new_paths.append(path + [adj_tile(cur_tile, exit_direction)])
            else:
                new_paths.append(path)
        paths = new_paths
    
    return get_shortest_path(paths, tiles_x_y)

def turns(path, tile_x_y):
    turns = 0
    for n in range(len(path) - 1):
        tile = path[n]
        tile_type = tile_x_y[tile[0]][tile[1]]
        exit = distance(path[n], path[n+1])
        if tile_type in (3,4,5,6):
            turns += 1
        elif tile_type == 7 and exit == left:
            turns += 1
        elif tile_type == 8 and exit == right:
            turns += 1
        elif tile_type == 9 and exit == top:
            turns += 1
        elif tile_type == 10 and exit == bot:
            turns += 1
        elif tile_type == 11 and n > 0:
            if exit != distance(path[n-1], path[n]):
                turn += 1
    return turns

def get_shortest_path(paths, tiles_x_y):
    min_length = len(tiles_x_y) * len(tiles_x_y[0])
    shortest_path = None
    for path in paths:
        if len(path) < min_length:
            shortest_path = path
            min_length = len(path)
        elif len(path) == min_length:
            if turns(path, tiles_x_y) < turns(shortest_path, tiles_x_y):
                shortest_path = path
                min_length = len(path)

    return shortest_path[1:]
