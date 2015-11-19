import sys

def map_to_file(world, start, file = 'map.txt'):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    tile_type_to_symbols = {
        0 : u' ',
        1 : u'\u2551',
        2 : u'\u2550',
        3 : u'\u2554',
        4 : u'\u2557',
        5 : u'\u255A',
        6 : u'\u255D',
        7 : u'\u2563',
        8 : u'\u2560',
        9 : u'\u2569',
        10: u'\u2566',
        11: u'\u256C',
        12: u'?'
        }

    with open(file, 'rb+') as f:
        f.write('Width: %s tiles\n'%str(world.width))
        f.write('Height: %s tiles\n\n'%str(world.height))
        f.write('Map: S=start\n\n')
        col_names = '  '
        for col in range(world.width):
            col_names += str(col)
        f.write(col_names + '\n')
        row_num = 0
        for y in range(world.height):
            row = []
            f.write(str(row_num))
            if row_num < 10:
                f.write(' ')
            for x in range(world.width):
                if (x,y) == start:
                    f.write('S')
                else:
                    f.write(tile_type_to_symbols[world.tiles_x_y[x][y]])
            row_num += 1
            f.write('\n')
        f.write(str(world.waypoints))
    exit(0)

