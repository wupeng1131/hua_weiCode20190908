import pickle
import random
import math
import ballclient.service.constants as constants

direction = {0: '', 1: 'up', 2: 'down', 3: 'left', 4: 'right'}


class task:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.info = "task"


class power:
    def __init__(self, x, y, point):
        self.x = x
        self.y = y
        self.point = point


class enemy:
    def __init__(self, id, score, sleep, x, y):
        self.id = id
        self.score = score
        self.sleep = sleep
        self.x = x
        self.y = y


class own:
    def __init__(self, id, score, sleep, x, y, mode):
        self.id = id
        self.score = score
        self.sleep = sleep
        self.x = x
        self.y = y
        self.mode = mode
        #generate wandering

def build_power_list(msg):
    power_list = []
    for info in msg:
        p = power(info['x'], info['y'], info['point'])
        power_list.append(p)

    return power_list



def choose_task(task_list):
    m_list = []
    for t in task_list:
        tmp = t.value
        m_list.append(tmp)
    task_id = m_list.index(max(m_list))
    m_task = task_list[task_id]
    return m_task

def distance(map, x1, y1, x2, y2):
    dist = abs(x1 - x2) + abs(y1 - y2)
    return dist if dist != 0 else 1

def distance_(x1, y1, x2, y2):
    dist = abs(x1 - x2) + abs(y1 - y2)
    return dist if dist != 0 else 0.5

def distance_0(x1, y1, x2, y2):
    dist = math.sqrt(math.pow(x1-x2,2) + math.pow(y1-y2,2))
    # dist = abs(x1 - x2) + abs(y1 - y2)
    return dist

def read_obj(path):
    file_obj = open(path,'rb')
    bunch = pickle.load(file_obj)
    file_obj.close()
    return bunch

def write_obj(path, obj):
    file_obj = open(path,'wb')
    pickle.dump(obj,file_obj)
    file_obj.close()


def print_matrix(matrix):
    col = matrix.shape[0]
    row = matrix.shape[1]
    for i in range(col):
        print
        for j in range(row):
            print matrix[i][j],

def idx2pos(m_map, idx):
    width = m_map.width
    #height = m_map.height
    x = idx % width
    y = idx // width
    return x,y

def pos2idx(m_map, x, y):
    width = m_map.width
    return y*width + x


def can_go(m_map, x , y):
    if (x >=0 and x < m_map.width) and (y >=0 and y < m_map.height):
        if m_map.map[y][x] == 1:
            return False
        else:
            return True

    else:
        return False


def s_d(m_map, x1,y1,x2,y2):  #move one step
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)
    if x2 > x1:
        return 4
    elif x2 < x1:
        return 3
    elif y2 > y1:
        return 2
    elif y2 < y1:
        return 1
    else:
        # print " $$$$$$$$$$$the road has been blocked"
        # m_map.print_map()
        if can_go(m_map,x1-1,y1):  #left
            # print "x1,y1", x1,y1
            # print "x2,y2", x2,y2
            # print "order",order
            # print "path", path
            # print "v:",idx2pos(m_map,v)
            # print "a:",idx2pos(m_map,a)
            # print m_map.map[y1][x1]
            return 3
        elif can_go(m_map,x1+1,y1):     #right
            return 4
        elif can_go(m_map,x1,y1-1):     #up
            return 1
        elif can_go(m_map,x1,y1+1):     #down
            return 2
        else:
            # print "no way to go!!!!!!!!!!!!!!!!!!!!!!!!!!"
            return random.randint(1, 4)



def next_pos(control, x1,y1):
    _x = x1
    _y = y1
    if control == 1:
        _y = y1-1
        # y1 -=1
    elif control == 2:
        _y = y1+1
        # y1 += 1
    elif control == 3:
        _x = x1-1
        # x1 -= 1
    elif control == 4:
        _x = x1+1
        # x1 += 1
    else:# ==0
        pass
    return _x,_y

def rand_choose(width, height):
    vision = constants.vision
    x = random.randint(0 + vision, width - vision - 1 )
    y = random.randint(0 + vision, height - vision - 1 )
    return x , y
def rand_choose_0(width, height):
    vision = constants.vision
    x = random.randint(0 , width  - 1 )
    y = random.randint(0 , height - 1 )
    return x , y
def rand_choose_1(width, height):
    vision = constants.vision
    x = random.randint(0+2 , width -2 -  1 )
    y = random.randint(0+2 , height -2 -  1 )
    return x , y

def catch_dirtction(m_map, x0, y0):
    _x = x0-1
    _y = y0
    p = []
    c = 0
    if m_map.is_space(_x,_y):
        p.append([-1,0])
        c+=1
    else:
        p.append([0, 0])

    _x = x0+1
    _y = y0
    if m_map.is_space(_x,_y):
        p.append([1,0])
        c += 1
    else:
        p.append([0, 0])

    _x = x0
    _y = y0-1
    if m_map.is_space(_x,_y):
        p.append([0,-1])
        c += 1
    else:
        p.append([0, 0])

    _x = x0
    _y = y0+1
    if m_map.is_space(_x,_y):
        p.append([0,1])
        c += 1
    else:
        p.append([0, 0])

    a = 0
    b = 0
    for i in range(4):
        a += p[i][0]
        b += p[i][1]
    return  a,b,c


def update_position(me, control):
    if control == 0:
        pass
    elif control == 1:#up
        me.x = me.x
        me.y = me.y-1
    elif control == 2:#down
        me.x = me.x
        me.y = me.y+1
    elif control == 3:#left
        me.x = me.x-1
        me.y = me.y
    else:              #right
        me.x = me.x+1
        me.y = me.y


def update_teammate_list(m_map,me,control):
    if control == 0:
        return
    x1 = me.x
    y1 = me.y
    # print "before:",x1,y1
    _x,_y = next_pos(control,x1,y1)
    if m_map.has_space(_x,_y):
        val = m_map.map[_y][_x]
        if val == 0:#space
            me.x = _x
            me.y = _y
        elif val == 1:#meteor
            pass
        elif val == 2:#tunnel
            _x,_y = m_map.run_tunnel(_x,_y)
            me.x = _x
            me.y = _y
        else:  #==3  wormhole
            _x, _y = m_map.run_wormhole(_x, _y)
            me.x = _x
            me.y = _y
    else:
        pass
    # print "after:", me.x,me.y









    # if control == 0:
    #     pass
    # elif control == 1:  # up
    #     if m_map.can_go(me.x,me.y-1):
    #         me.x = me.x
    #         me.y = me.y - 1
    #     else:
    #         pass
    # elif control == 2:  # down
    #     if m_map.can_go(me.x,me.y+1):
    #         me.x = me.x
    #         me.y = me.y + 1
    #     else:
    #         pass
    # elif control == 3:  # left
    #     if m_map.can_go(me.x-1,me.y):
    #         me.x = me.x - 1
    #         me.y = me.y
    #     else:
    #         pass
    # else:  # right
    #     if m_map.can_go(me.x+1,me.y):
    #         me.x = me.x + 1
    #         me.y = me.y
    #     else:
    #         pass



def enemy_distance(fish_map, own_list, enemy):
    dis = 0
    for o in own_list:
        x1 = o.x
        y1 = o.y
        x2 = enemy.x
        y2 = enemy.y
        d = distance_(x1,y1,x2,y2)
        dis += d
    return dis/len(own_list)

def center_distance(fish_map,enemy):
    center_x = int(fish_map.width/2)
    center_y = int(fish_map.height/2)
    # if enemy.x + enemy.y ==0 or enemy.x + enemy.y == fish_map.width + fish_map.height -2:
    #     print "!!!!!!!!!!!!!!!!!!!!!!!!!valuable!!!!"
        # distance_(center_x, center_y, enemy.x, enemy.y)*10
    return distance_(center_x,center_y,enemy.x,enemy.y)


def corner_distance(fish_map,e):
    d = []
    w = fish_map.width
    h = fish_map.height
    x1 = 0
    y1 = 0
    dis = distance_(e.x,e.y,x1,y1)
    d.append(dis)

    x1 = 0
    y1 = h-1
    dis = distance_(e.x, e.y, x1, y1)
    d.append(dis)

    x1 = w-1
    y1 = 0
    dis = distance_(e.x, e.y, x1, y1)
    d.append(dis)

    x1 = w-1
    y1 = h-1
    dis = distance_(e.x, e.y, x1, y1)
    d.append(dis)

    return min(d)


