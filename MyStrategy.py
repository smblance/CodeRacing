from model.Car import Car
from model.Game import Game
from model.Move import Move
from model.World import World
from math import sin, cos, sqrt, pi

from convenience import adj_tile, distance, abs_distance, ttype, sign
from path_to_waypoint import path_to_waypoint
from map_to_file import map_to_file

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

def get_target(me, world, game, path):
    # if cur_tile[0] == next_tile[0]:
    #     return ( (cur_tile[0] + 1/2.)*tile_size, ((cur_tile[1] + next_tile[1])/2 + 1/2.)*tile_size)
    # elif cur_tile[1] == next_tile[1]:
    #     return ( ((cur_tile[0] + next_tile[0])/2 + 1/2.)*tile_size, ((cur_tile[1])+ 1/2.)*tile_size)
    
    tile1, tile2, tile3 = path[0], path[1], path[2]
    if tile3[0] == tile1[0]: #2 tiles straight top or bot
        return  me.x, me.y + sign(tile3[1] - tile1[1]) * game.track_tile_size
    elif tile3[1] == tile1[1]: #2 tiles straight left or right
        return  me.x + sign(tile3[0] - tile1[0]) * game.track_tile_size, me.y
    
    elif tile2[0] > tile1[0]: #first right than turn
        #if me.x < tile1[0]*(game.track_tile_size + 1/2): #if didnt pass half of tile1
        #    return me.x + game.track_tile_size, me.y
        if tile3[1] < tile2[1]: #time to turn -> move right than top
            return tile2[0]*game.track_tile_size + (me.y - tile1[1] * game.track_tile_size) , tile2[1] *game.track_tile_size
        elif tile3[1] > tile2[1]: #time to turn -> move right than bot
            return tile2[0]*game.track_tile_size + (me.y - tile1[1] * game.track_tile_size) , (tile2[1]+1)*game.track_tile_size
    
    elif tile2[0] < tile1[0]: #first left than turn
        #if me.x > tile1[0]*(game.track_tile_size + 1/2): #if didnt pass half of tile1
        #    return me.x - game.track_tile_size, me.y
        if tile3[1] < tile2[1]: #time to turn -> move left than top
            return (tile2[0]+1)*game.track_tile_size - (me.y - tile[1] * game.track_tile_size) , tile2[1]*game.track_tile_size
        elif tile3[1] > tile2[1]: #time to turn -> move left than bot
            return (tile2[0]+1)*game.track_tile_size - (me.y - tile[1] * game.track_tile_size) , (tile2[1]+1)*game.track_tile_size
            
    elif tile2[1] < tile1[1]: #first top than turn
        #if me.y > tile1[1]*(game.track_tile_size + 1/2): #if didnt pass half of tile1
        #    return me.x, me.y - game.track_tile_size
        if tile3[0] < tile2[0]: #time to turn -> move top than left
            return tile2[0]*game.track_tile_size, (tile2[1] + 1)*game.track_tile_size - (me.x - tile1[0] * game.track_tile_size)
        elif tile3[0] > tile2[0]: #time to turn -> move top than right
            return (tile2[0]+1)*game.track_tile_size, (tile2[1] + 1)*game.track_tile_size - (me.x - tile1[0] * game.track_tile_size)
    
    elif tile2[1] > tile1[1]: #first bot than turn
        #if me.y < tile1[1]*(game.track_tile_size + 1/2): #if didnt pass half of tile1
        #    return me.x, me.y + game.track_tile_size
        if tile3[0] < tile2[0]: #time to turn -> move bot than left
            return tile2[0]*game.track_tile_size, tile2[1]*game.track_tile_size + (me.x - tile1[0] * game.track_tile_size)
        elif tile3[0] > tile2[0]: #time to turn -> move bot than right
            return (tile2[0]+1)*game.track_tile_size, tile2[1]*game.track_tile_size + (me.x - tile1[0] * game.track_tile_size)
    


class MyStrategy:

    def __init__(self):
        self.distance_to_waypoint = None
        self.map_path = None
        self.path = None

    def move(self, me, world, game, move):

        """
        @type me: Car
        @type world: World
        @type game: Game
        @type move: Move
        """
        
        #calculate variables
        tile_x = int(me.x/game.track_tile_size)  #round down
        tile_y = int(me.y/game.track_tile_size)  #round down
        cur_tile = (tile_x, tile_y)
        #map_to_file(world, cur_tile)
        waypoint = (me.next_waypoint_x,me.next_waypoint_y)
        path = path_to_waypoint(cur_tile, waypoint, world.tiles_x_y)
        if len(path) == 2:
            second_wp = tuple(world.waypoints[(me.next_waypoint_index + 1) % len(world.waypoints)])
            #if abs_distance(waypoint,second_wp) == 1:
            #    second_wp = world.waypoints[(me.next_waypoint_index + 2) % len(world.waypoints)]
            path.append(path_to_waypoint(waypoint, second_wp, world.tiles_x_y)[1])
        # move
        move.engine_power = 0.5
        target = get_target(me, world, game, path)
        angle_to_target = me.get_angle_to(target[0], target[1])
        move.wheel_turn = angle_to_target/pi

        if world.tick % 30 == 0:
            print 'me, target, wheelturn: ', (me.x,me.y), target, angle_to_target/pi * 2, path

        move.throw_projectile = False
        move.spill_oil = False
        if world.tick > game.initial_freeze_duration_ticks:
            move.use_nitro = False
