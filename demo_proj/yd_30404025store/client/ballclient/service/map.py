import ballclient.service.constants as constants
import random
import sys
from util import *
# import numpy as np

class Map:
    def __init__(self, msg):
        self.width = msg['msg_data']['map']['width']
        self.height = msg['msg_data']['map']['height']
        self.vision = msg['msg_data']['map']['vision']

        self.meteor_list = []
        self.tunnel_list = []
        self.wormhole_list = []
        self.team = []

        for team_info in msg['msg_data']['teams']:
            id = team_info['id']
            # players = team_info['players']
            force = team_info['force']
            _team = team(id, force)
            self.team.append(_team)

        for meteor_info in msg['msg_data']['map']['meteor']:
            x = meteor_info['x']
            y = meteor_info['y']
            _meteor = meteor(x, y)
            self.meteor_list.append(_meteor)

        for tunnel_info in msg['msg_data']['map']['tunnel']:
            x = tunnel_info['x']
            y = tunnel_info['y']
            direction = tunnel_info['direction']
            if direction == 'up':
                d = 1
            elif direction == 'down':
                d = 2
            elif direction == 'left':
                d = 3
            else:# 'right'
                d = 4
            _tunnel = tunnel(x, y, d)
            self.tunnel_list.append(_tunnel)


        for wormhole_info in msg['msg_data']['map']['wormhole']:
            x = wormhole_info['x']
            y = wormhole_info['y']
            name = wormhole_info['name']
            _wormhole = wormhole(x, y, name)
            self.wormhole_list.append(_wormhole)



        self.generate_map()

        self.wander_task = []

        for i in range(8):

            _x, _y = rand_choose(self.width, self.height)

            while not self.is_space(_x, _y):
                _x, _y = rand_choose(self.width, self.height)
            _task = task(_x, _y, 0.001 )
            _task.info = "wander_task"

            self.wander_task.append(_task)

    def wander_task_check(self,own,mode):
        idx = own.id
        x1 = self.wander_task[idx].x
        y1 = self.wander_task[idx].y
        x2 = own.x
        y2 = own.y
        dist1 = abs(x1 - x2)
        dist2 = abs(y1 - y2)
        vision = constants.vision
        value = 0.001
        # vision = 2
        if mode == 0:#aggressive
            if dist1 <= 2 and dist2 <= 2:
                _x, _y = rand_choose_0(self.width, self.height)
                while not self.is_space(_x, _y):
                    _x, _y = rand_choose_0(self.width, self.height)

                _task = task(_x, _y, value)
                _task.info = "wander_task"
                self.wander_task[idx] = _task
        else: #conservative
            if dist1 <= 2 and dist2 <= 2:
                _x, _y = rand_choose_1(self.width, self.height)
                while not self.is_space(_x, _y):
                    _x, _y = rand_choose_1(self.width, self.height)

                _task = task(_x, _y, value)
                _task.info = "wander_task"
                self.wander_task[idx] = _task
                # print "fish:", idx, "get a new goal (", _x, _y,")"

        idx = own.id
        x1 = self.wander_task[idx].x
        y1 = self.wander_task[idx].y

        count = 0
        _x = x1-1
        _y = y1
        if self.is_tunnel(_x,_y):
            count +=1

        _x = x1+1
        _y = y1
        if self.is_tunnel(_x,_y):
            count +=1

        _x = x1
        _y = y1-1
        if self.is_tunnel(_x,_y):
            count +=1


        _x = x1
        _y = y1+1
        if self.is_tunnel(_x,_y):
            count +=1

        if count == 4:
            # print "find it!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! cant reach here changing"
            # print "the cannot reach position is", x1,y1
            while not self.is_space(_x, _y):
                _x, _y = rand_choose_1(self.width, self.height)

            _task = task(_x, _y, value)
            _task.info = "wander_task"
            self.wander_task[idx] = _task


        # if x1 == x2 and y1 == y2:
        #     _x, _y = rand_choose(self.width, self.height)
        #     while not self.is_space(_x, _y):
        #
        #         _x, _y = rand_choose(self.width, self.height)
        #
        #     _task = task(_x, _y, 0.001)
        #     self.wander_task[idx] = _task
        #     print "fish:",idx,"get a new goal "


    def is_space(self, _x, _y):
        if self.has_space(_x,_y):
            if self.map[_y][_x] == 0:
                return True
            else:
                return False
        else:
            return False

    def can_go(self, _x, _y):
        if self.has_space(_x,_y):
            if self.map[_y][_x] != 1:
                return True
            else:
                return False
        else:
            return False
    def update_wander_task(self):
        _x, _y = rand_choose(self.width, self.height)
        while not self.is_space(_x, _y):
            _x, _y = rand_choose(self.width, self.height)
        self.wander_task = task(_x, _y, 0.0001 )

    def generate_map(self):
        '''
        0 nothing
        1 meteor
        2 tunnel
        3 wormhole
        '''
        self.map = [[0 for i in range(self.width)] for j in range(self.height)]
        # self.map = np.zeros((self.height,self.width), dtype = int)


        # modeling metetor
        for _meteor in self.meteor_list:
            self.map[_meteor.y][_meteor.x] = 1

        # modeling tunnel
        for _tunnel in self.tunnel_list:
            self.map[_tunnel.y][_tunnel.x] = 2

        # modeling wormhole
        for _wormhole in self.wormhole_list:
            self.map[_wormhole.y][_wormhole.x] = 3

    def print_map(self):
        print "############"
        for x in range(self.width):
            print "\n"
            for y in range(self.height):
                print (self.map[x][y]),

    def has_space(self,x,y):
        if (x>=0 and x < self.width) and (y>=0 and y < self.height):
            return True
        else:
            return False

    def not_me(self, x,y, me):
        if x == me.x and y == me.y:
            return False
        else:
            return True

    def add_enemy(self,enemy, me):
        p = []
        p.append([enemy.x,enemy.y])
        p.append([enemy.x-1, enemy.y])
        p.append([enemy.x+1, enemy.y])
        p.append([enemy.x, enemy.y-1])
        p.append([enemy.x, enemy.y+1])
        for i in range(5):
            # distance && not me && has_space
            if distance_(me.x, me.y, p[i][0], p[i][1]) <=1 and self.not_me(p[i][0], p[i][1],me) and self.has_space(p[i][0], p[i][1]):
                # == 0
                _x = p[i][0]
                _y = p[i][1]
                if self.map[_y][_x] == 0 or self.map[_y][_x] == 3:
                    self.map[_y][_x] = 1



        # x = enemy.x
        # y = enemy.y
        # #0
        # _x = x
        # _y = y
        # if self.has_space(_x,_y):
        #     self.map[_y][_x] = 1 if self.map[_y][_x] == 0 and self.not_me(_x,_y,me) else self.map[_y][_x]
        # #1
        # _x = x-1
        # _y = y
        # if self.has_space(_x,_y):
        #     self.map[_y][_x] = 1 if self.map[_y][_x] == 0 and self.not_me(_x,_y,me) else self.map[_y][_x]
        # #2
        # _x = x+1
        # _y = y
        # if self.has_space(_x,_y):
        #     self.map[_y][_x] = 1 if self.map[_y][_x] == 0 and self.not_me(_x,_y,me) else self.map[_y][_x]
        # #3
        # _x = x
        # _y = y-1
        # if self.has_space(_x,_y):
        #     self.map[_y][_x] = 1 if self.map[_y][_x] == 0 and self.not_me(_x,_y,me) else self.map[_y][_x]
        # #4
        # _x = x
        # _y = y+1
        # if self.has_space(_x,_y):
        #     self.map[_y][_x] = 1 if self.map[_y][_x] == 0 and self.not_me(_x,_y,me) else self.map[_y][_x]

    def add_own(self,me):
        p = []
        p.append([me.x,me.y])
        p.append([me.x-1, me.y])
        p.append([me.x+1, me.y])
        p.append([me.x, me.y-1])
        p.append([me.x, me.y+1])
        for i in range(5):
            _x = p[i][0]
            _y = p[i][1]
            if self.is_space(_x,_y):
                self.map[_y][_x] = 1

    def is_wormhole(self,x1,y1):
        for w in self.wormhole_list:
            if w.x == x1 and w.y == y1:
                return True
        return False

    def is_couple(self, name1, name2 ):
        if abs(ord(name1) - ord(name2)) == 32:
            return True
        else:
            return False

    def wormhole_next(self,x1,y1):
        for w in self.wormhole_list:
            if w.x == x1 and w.y == y1:
                for _w in self.wormhole_list:
                    if self.is_couple(w.name,_w.name):
                        return _w.x, _w.y
        return x1, y1

    def run_wormhole(self, x1, y1):
        x1,y1 = self.wormhole_next(x1,y1)
        return x1,y1
    def tunnel_direction(self,x1,y1):
        for t in self.tunnel_list:
            if t.x == x1 and t.y == y1:
                return t.direction
        return 0



    def is_tunnel(self,x1, y1):
        for t in self.tunnel_list:
            if t.x == x1 and t.y == y1:
                return True
        return False

    def tunnel_next(self, x1, y1):
        for t in self.tunnel_list:
            if t.x == x1 and t.y == y1:
                if t.direction == 1: #up
                    return x1, y1-1
                elif t.direction == 2:#down
                    return x1, y1+1
                elif t.direction == 3:#left
                    return x1-1, y1
                else:   # right
                    return x1+1, y1
        return x1,y1

    def run_tunnel(self,x1,y1):
        while(self.is_tunnel(x1,y1)):
            x1,y1 = self.tunnel_next(x1,y1)
        return x1,y1





class meteor:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class tunnel:
    '''
    direction{1:up , 2: down, 3: left, 4: right}
    '''
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

class wormhole:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name


class team:
    def __init__(self, id,  force):
        self.id = id
        # self.players = players
        self.force = force