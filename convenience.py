def adj_tile(tile, direction):
    return (tile[0] + direction[0], tile[1] + direction[1])

def distance(tile_1, tile_2):
    return (tile_2[0] - tile_1[0], tile_2[1] - tile_1[1])