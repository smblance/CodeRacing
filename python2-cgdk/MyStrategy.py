from model.Car import Car
from model.Game import Game
from model.Move import Move
from model.World import World
from math import sin, cos, sqrt, pi

from convenience import adj_tile, distance
from map_to_file import map_to_file
from map_path import map_path

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

def get_target(me, world, cur_tile, next_tile, tile_size):
    if cur_tile[0] == next_tile[0]:
        return ( (cur_tile[0] + 1/2.)*tile_size, ((cur_tile[1] + next_tile[1])/2 + 1/2.)*tile_size)
    elif cur_tile[1] == next_tile[1]:
        return ( ((cur_tile[0] + next_tile[0])/2 + 1/2.)*tile_size, ((cur_tile[1])+ 1/2.)*tile_size)


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
        if self.path == None:
            self.path = map_path(world, me)
        
        #calculate variables
        tile_x = int(me.x/game.track_tile_size)  #round down
        tile_y = int(me.y/game.track_tile_size)  #round down
        cur_tile = (tile_x, tile_y)
        if self.path.index(cur_tile) != len(self.path):
            next_tile = self.path[self.path.index(cur_tile) + 1]
        else:
            next_tile == self.path[0]

        # move
        move.engine_power = 0.5
        target = get_target(me, world, cur_tile, next_tile, game.track_tile_size)
        angle_to_target = me.get_angle_to(target[0], target[1])
        move.wheel_turn = angle_to_target/pi

        if world.tick % 30 == 0:
            print (me.x,me.y), angle_to_target, target, move.wheel_turn

        move.throw_projectile = False
        move.spill_oil = False
        if world.tick > game.initial_freeze_duration_ticks:
            move.use_nitro = False
