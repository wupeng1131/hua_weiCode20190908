from __future__ import division
import pickle
import random
import math

import time
import ballclient.service.constants as constants

direction = {0: '', 1: 'up', 2: 'down', 3: 'left', 4: 'right'}
INF = float('inf')

class node():
    def __init__(self,id,s,m_map):
        self.id = int(id)
        self.x = id % m_map.width
        self.y = id // m_map.width
        self.step = int(s)

class dir_connection():
    def __init__(self,own,task,m_map,m):
        self.a = own.id
        self.b = task.id
        self.task_state = 0
        self.direction = task.direction
        self.value = 0
        ex = task.x
        ey = task.y
        self.dis_b = 99999
        self.dis_a = own.find_distance(m_map,ex,ey)     #dis own---------enemy
        self.dis_a = int(self.dis_a)
        # require dist2
        ###########################
        me_dir = task.direction
        param = 9
        reach_list = could_reach(m, param, me_dir, ex, ey)  # 4.3 could reach
        # print "length of reach_list is", len(reach_list)
        if len(reach_list) == 0:  ###what to do with it
            # print "ZZZZZZZZZZZZZZZZZZZZZZZZZZZKKKKKKKKKKKKKKKKKKKKKKKKK"
            self.value = 0
            self.dis_b = 99999
        else:
            state = 0
            for _node in reach_list:
                dist1 = own.find_distance(m_map, _node.x, _node.y)  # djs_distance(fish_map, me.x,me.y,_node.x,_node.y )
                dist1 = int (dist1)
                dist2 = _node.step
                if dist1 >= dist2:
                    self.dis_b = dist1
                    state = 1   #find catch_point and its distance
                    break #bug!!!!!!!!!!

            if state == 0 :
                _node = reach_list[0]
                self.dis_b = own.find_distance(m_map, ex, ey)

            if self.dis_a == 0:
                self.dis_a = 0.01
            if self.dis_b == 0:
                self.dis_b = 0.01
            #self.value = 1/(dis_a*dis_b)
        self.value = (1/self.dis_a)*100 + (1/self.dis_b)
        # print "dist_a",dis_a
        # print "dis_b",dis_b


        ############################



class connection():
    def __init__(self, own, task, own_list,m_map):
        self.a= own.id
        self.b = task.id
        self.dx = task.x
        self.dy = task.y

        self.task_state = 0
        self.info = task.info
        x = task.x
        y = task.y
        _x = own.x
        _y = own.y
        # dist = distance_(_x,_y,x,y)
        self.dist = own.find_distance(m_map,x,y)
        if self.dist == 0:
            self.dist = 0.1
        # print own.dist
        self.value = task.value / self.dist
        self.direction = task.direction

        # if task.info == "enemy_task" or task.info == "enemy_power":
        #     ave_dis = average_distance(own_list, task)
        #     self.value = task.value/ave_dis
        # else:
        #     x1 = own.x
        #     y1 = own.y
        #     x2 = task.x
        #     y2 = task.y
        #     dist = distance_(x1, y1, x2, y2)
        #     self.value = task.value / dist



class task:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.task_state = 0
        self.info = "task"
        self.ownIndex = 0
        self.id = 0
        self.direction = 0


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
        self.dist = []
        self.path = []

    def printfPath(self, path, a):
        # path = path.astype(np.int32)
        # print path
        stack = [0 for i in range(999)]
        # stack = np.zeros(self.maxSize, dtype=float)
        top = -1
        while path[a] != -1.0:
            top += 1
            stack[top] = a
            a = path[a]

        top += 1
        stack[top] = a
        order = []
        while top != -1:
            order.append(stack[top])
            top -= 1
        return order

    def dijkstra(self, v, m_map, matrix):
        # print "v: ", v, "a:", a
        tmp = 0.0
        n = m_map.width * m_map.height
        dist = [0 for i in range(n)]
        path = [0 for i in range(n)]
        _set = [0 for i in range(n)]
        for i in range(n):
            dist[i] = matrix[v][i]
            _set[i] = 0
            if (matrix[v][i] < INF):
                path[i] = v
            else:
                path[i] = -1

        _set[v] = 1
        path[v] = -1

        u = 0  # bug
        # start = time.time()
        for i in range(n - 1):
            min = INF
            for j in range(n):
                if _set[j] == 0 and dist[j] < min:
                    u = j
                    min = dist[j]
            _set[u] = 1

            for j in range(n):
                # tmp = dist[u] + self.matrix[u][j]

                if _set[j] == 0 and dist[u] + matrix[u][j] < dist[j]:
                    dist[j] = dist[u] + matrix[u][j]

                    path[j] = u
        self.path = path
        self.dist = dist

        # generate wandering

    def find_direction(self, m_map, x, y):
        a = pos2idx(m_map, x, y)

        order = self.printfPath(self.path, a)
        if len(order) == 1:
            v = pos2idx(m_map, self.x, self.y)

            if order[0] == v:
                order.pop()
                order.append(v)
                order.append(v)
            else:
                order.pop()
                order.append(v)
                order.append(a)
        x0, y0 = idx2pos(m_map, order[0])
        x1, y1 = idx2pos(m_map, order[1])
        dir = s_d(m_map, x0, y0, x1, y1)
        return dir

    def find_distance(self, m_map, x, y):
        a = pos2idx(m_map, x, y)
        dis = self.dist[a]
        # print "path is",self.path
        if dis == 0:
            dis = 0.1
        return dis


class own:
    def __init__(self, id, score, sleep, x, y, mode):
        self.id = id
        self.score = score
        self.sleep = sleep
        self.x = x
        self.y = y
        self.mode = mode
        self.catch_enemy = 0
        self.run = 0
        self.task_state = 0 # 1: have been allocated task
        self.dist = []
        self.path = []

    def printfPath(self, path, a):
        # path = path.astype(np.int32)
        # print path
        stack = [0 for i in range(999)]
        # stack = np.zeros(self.maxSize, dtype=float)
        top = -1
        while path[a] != -1.0:
            top += 1
            stack[top] = a
            a = path[a]

        top += 1
        stack[top] = a
        order = []
        while top != -1:
            order.append(stack[top])
            top -= 1
        return order

    def dijkstra(self, v, m_map,matrix):
        # print "v: ", v, "a:", a
        tmp = 0.0
        n = m_map.width * m_map.height
        dist = [0 for i in range(n)]
        path = [0 for i in range(n)]
        _set = [0 for i in range(n)]
        for i in range(n):
            dist[i] = matrix[v][i]
            _set[i] = 0
            if (matrix[v][i] < INF):
                path[i] = v
            else:
                path[i] = -1

        _set[v] = 1
        path[v] = -1

        u = 0  # bug
        # start = time.time()
        for i in range(n - 1):
            min = INF
            for j in range(n):
                if _set[j] == 0 and dist[j] < min:
                    u = j
                    min = dist[j]
            _set[u] = 1

            for j in range(n):
                # tmp = dist[u] + self.matrix[u][j]

                if _set[j] == 0 and dist[u] + matrix[u][j] < dist[j]:
                    dist[j] = dist[u] + matrix[u][j]

                    path[j] = u
        self.path = path
        self.dist = dist




        #generate wandering

    def find_direction(self,m_map,x,y):
        a = pos2idx(m_map,x,y)

        order = self.printfPath(self.path, a)
        if len(order) == 1:
            v = pos2idx(m_map, self.x, self.y)

            if order[0] == v:
                order.pop()
                order.append(v)
                order.append(v)
            else:
                order.pop()
                order.append(v)
                order.append(a)
        x0, y0 = idx2pos(m_map, order[0])
        x1, y1 = idx2pos(m_map, order[1])
        dir = s_d(m_map, x0, y0, x1, y1)
        return dir

    def find_distance(self,m_map,x,y):
        a = pos2idx(m_map, x, y)
        dis = self.dist[a]
        # print "path is",self.path
        if dis == 0:
            dis = 0.1
        return dis



def build_enemy_list(msg):
    enemy_list = []
    for info in msg:
        if info['team']!= constants.team_id:
            e = enemy(info['id'], info['score'], info['sleep'], info['x'], info['y'])
            enemy_list.append(e)
    return enemy_list


def build_own_list(msg,mode):

    own_list = []
    for info in msg:
        if info['team'] == constants.team_id:
            e = own(info['id'], info['score'], info['sleep'], info['x'], info['y'], mode)
            own_list.append(e)
    return own_list


def judge_mode(fish_map, curr_mode):
    team = fish_map.team
    for t in team:
        if t.id == constants.team_id:
            if t.force == curr_mode:
                return 1
            else:
                return 0
    return 0

# def distance1(fish, power):
#     x1 = fish.x
#     y1 = fish.y
#     x2 = power.x
#     y2 = power.y
#     dist = abs(x1 - x2) + abs(y1 - y2)
#     return dist

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
    # dist = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
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


def can_go_(m_map,_x,_y, x , y):
    if (x >=0 and x < m_map.width) and (y >=0 and y < m_map.height):
        if m_map.map[y][x] == 1:
            return False
        elif m_map.map[y][x] == 2:  # tunnel
            x1, y1 = m_map.run_tunnel(x, y)
            if _x == x1 and _y ==y1:
                return False
            else:
                return True

        # else:
        #     return True

    else:
        return False

def can_go(m_map,_x,_y, x , y):
    if (x >=0 and x < m_map.width) and (y >=0 and y < m_map.height):
        if m_map.map[y][x] == 1:
            return False
        elif m_map.map[y][x] == 2:#tunnel
            x1,y1 = m_map.run_tunnel(x,y)
            if m_map.map[y1][x1] == 1 or (_x == x1 and _y ==y1):
                return False
            else:
                return True
        else:
            return True

        # else:
        #     return True

    else:
        return False


def s_d(m_map, x1,y1,x2,y2):  #move one step
    if x1 == x2 and y1 == y2:
        return 0
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)
    if distance_(x1,y1,x2,y2)>1:
        print " $$$$$$$$$$$the road has been blocked"
        # m_map.print_map()
        if can_go(m_map, x1, y1, x1 - 1, y1):  # left
            print "x1,y1", x1,y1
            print "x2,y2", x2,y2

            print m_map.map[y1][x1]
            return 3
        elif can_go(m_map, x1, y1, x1 + 1, y1):  # right
            return 4
        elif can_go(m_map, x1, y1, x1, y1 - 1):  # up
            return 1
        elif can_go(m_map, x1, y1, x1, y1 + 1):  # down
            return 2
        else:

            if can_go_(m_map, x1, y1, x1 - 1, y1):  # left
                return 3
            elif can_go_(m_map, x1, y1, x1 + 1, y1):  # right
                return 4
            elif can_go_(m_map, x1, y1, x1, y1 - 1):  # up
                return 1
            elif can_go_(m_map, x1, y1, x1, y1 + 1):  # down
                return 2
            else:
                # print "no way to go!!!!!!!!!!!!!!!!!!!!!!!!!!"
                return 0

    if x2 > x1:
        return 4
    elif x2 < x1:
        return 3
    elif y2 > y1:
        return 2
    elif y2 < y1:
        return 1



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
    # random.seed(time.time())
    x = random.randint(0+2 , width  -2- 1 )
    y = random.randint(0+2 , height -2- 1 )
    return x , y
def rand_choose_1(width, height):
    vision = constants.vision
    # random.seed(time.time())
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


def average_distance(own_list, task):
    dis = 0
    for o in own_list:
        x1 = o.x
        y1 = o.y
        x2 = task.x
        y2 = task.y
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


def catch_enemy_count(own_list):
    c = 0
    for o in own_list:
        if o.catch_enemy == 1:
            c+=1
    return c

def to_be_alloc(own_list):
    own_num = len(own_list)
    count = 0
    for o in own_list:
        if o.task_state == 1:
            count +=1
    if count == own_num:
        return False # dont need to be alloc
    else:
        return True # need to be alloc

def choose_connection(connection_list):
    _max = -1
    _tmp = connection_list[0]  # !!! keep there is connection
    for con in connection_list: # choose the max value of connect
        if con.task_state == 0:
            if con.value > _max:
                _max = con.value
                _tmp = con
    # print _tmp.value
    return _tmp

def delete_own(own_id, own_list, connection_list):
    own = own_list[0]
    for o in own_list:
        if o.task_state == 0:
            if own_id == o.id:
                o.task_state = 1 #allocate over
                # print "owQQQQQQQQQQQQQ ownn id: ",o.id ,"has been finished"
                own = o
                break
    # delete all the connection has own
    for con in connection_list:
        if con.task_state == 0:
            if con.a == own.id: # to be deleted
                con.task_state = 1


def delete_task(task_id, task_list, connection_list):
    _task = task_list[0]
    for t in task_list:
        if t.task_state == 0:
            if task_id == t.id:
                t.task_state = 1
                _task = t
                break
    #find it
    #delete all the connection has task
    for con in connection_list:
        if con.task_state == 0:
            if con.b == _task.id:
                con.task_state = 1


def add_dir_around_enemy(fish_map,e,value,task_list):
    pos = []
    x2 = e.x
    y2 = e.y


    _x = x2
    _y = y2 - 1
    pos.append([_x, _y])

    _x = x2
    _y = y2 + 1
    pos.append([_x, _y])


    _x = x2 - 1
    _y = y2
    pos.append([_x,_y])

    _x = x2 + 1
    _y = y2
    pos.append([_x, _y])




    idx_count = 0
    for p in pos:
        idx_count += 1
        _x = p[0]
        _y = p[1]

        if fish_map.has_space(x2,y2):
            _task = task(x2, y2, value)
            _task.info = "direction"
            _task.id = len(task_list)
            _task.direction = idx_count
            task_list.append(_task)


def add_power_around_enemy(fish_map,e,value,task_list,matrix):
    pos = []
    x2 = e.x
    y2 = e.y


    _x = x2
    _y = y2 - 1
    pos.append([_x, _y])

    _x = x2
    _y = y2 + 1
    pos.append([_x, _y])


    _x = x2 - 1
    _y = y2
    pos.append([_x,_y])

    _x = x2 + 1
    _y = y2
    pos.append([_x, _y])




    idx_count = 0
    for p in pos:
        idx_count += 1
        _x = p[0]
        _y = p[1]

        if fish_map.has_space(_x,_y):
            if fish_map.map[_y][_x] == 0 and matrix[_y][_x] != 1: #space
                _task = task(_x, _y, value)
                _task.info = "add_enemy_power_space"
                _task.id = len(task_list)
                _task.direction = idx_count
                task_list.append(_task)
            elif fish_map.map[_y][_x] == 1: #stone
                pass
            elif fish_map.map[_y][_x] == 2 and matrix[_y][_x] != 1:  # tunnel
                x, y = fish_map.run_tunnel(_x,_y)
                if x == _x and y == _y:
                    pass
                else:
                    _task = task(x, y, value)
                    _task.info = "add_enemy_power_tunnel"
                    _task.id = len(task_list)
                    _task.direction = idx_count
                    task_list.append(_task)

            elif fish_map.map[_y][_x] == 3 and matrix[_y][_x] != 1:  # wormhole
                _task = task(_x, _y, value)
                _task.info = "add_enemy_power_worm_hole"
                _task.id = len(task_list)
                _task.direction = idx_count
                task_list.append(_task)
            else:
                pass




def is_left(x1,x2):
    if x2 < x1:
        return True
    else:
        return False
def is_up(y1,y2):
    if y2 < y1:
        return True
    else:
        return False

def judge_task(near_enemy,o):
    x1 = near_enemy.x
    y1 = near_enemy.y
    x2 = o.x
    y2 = o.y
    dx = abs(x1 -x2)
    dy = abs(y1-y2)
    if is_left(x1,x2):
        if is_up(y1,y2):
            if dy<dx:
                return 3
            else:
                return 1
        else:
            if dy<dx:
                return 3
            else:
                return 2
    else:
        if is_up(y1,y2):
            if dy<dx:
                return 4
            else:
                return 1
        else:
            if dy<dx:
                return 4
            else:
                return 2



def search_limit(m,ex,ey,dir_enemy2own, dis_count):
    print "dis_count is:", dis_count
    if dis_count == 0:
        return ex,ey
    if dir_enemy2own == 1:#up
        for y in range(0,len(m)):
            for x in range(len(m)):
                if m[y][x] <= dis_count:
                    return x,y
    elif dir_enemy2own == 2:#down
        for y in range(len(m)-1,-1,-1):
            for x in range(len(m)):
                if m[y][x] <= dis_count:
                    return x,y
    elif dir_enemy2own == 3:#left
        for x in range(0,len(m)):
            for y in range(len(m)):
                if m[y][x] <= dis_count:
                    return x,y
    else:#right
        for x in range(len(m)-1,-1,-1):
            for y in range(len(m)):
                if m[y][x] <= dis_count:
                    return x,y


class reach_node():
    def __init__(self,x,y,s):
        self.x = x
        self.y = y
        self.step = int(s)

def could_reach(m,param,dir_enemy2own,ex,ey):
    reach_list =[]

    if dir_enemy2own == 1:  # up

        for y in range(0, ey):
            if m[y][ex] <= param:
                _node = reach_node(ex,y,m[y][ex])
                reach_list.append(_node)
                # print "###",x,y,m[y][x]
    elif dir_enemy2own == 2:  # down
        for y in range(len(m) - 1, ey, -1):
            if m[y][ex] <= param:
                _node = reach_node(ex, y, m[y][ex])
                reach_list.append(_node)
                # print "###", x, y, m[y][x]
    elif dir_enemy2own == 3:  # left
        # print "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"

        for x in range(0, ex):
            # print"EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE"
            # print m[ey][x], param
            if m[ey][x] <= param:
                # print "FFFFFFFFFFFFFFFFFFFFFFFFF"
                _node = reach_node(x, ey, m[ey][x])
                reach_list.append(_node)
                # print "#######%%%%%%%%#########", x, ey, m[ey][x]
    else:  # right
        for x in range(len(m) - 1, ex, -1):
            if m[ey][x] <= param:
                _node = reach_node(x, ey, m[ey][x])
                reach_list.append(_node)
                # print "###", x, y, m[y][x]
    return reach_list

def print_state(state_list):
    for l in state_list:
        print "(",l.id,":",l.task_state,")"

def print_task_state(state_list):
    print "%%%%%%%%%%%%%%%%%%"
    for l in state_list:
        print "(","task id:",l.id,"state",l.task_state,"x",l.x,"y",l.y,"info:",l.info,"value",l.value,")"



def has_own_member(own_list,x,y):
    for o in own_list:
        if o.x == x and o.y == y:
            return True
    return False


def is_danger(fish_map, own_list,m_task, x,y):
    # judge on the map
    if not fish_map.has_space(x,y):
        return True
    if fish_map.map[y][x] == 2:#tunnel,judge if can go
        x1 = m_task.x
        y1 = m_task.y

        x2 = x #tunnel position
        y2 = y
        dir = fish_map.tunnel_direction(x2,y2) #tunnel_direction????
        if dir == 0:
            print "error!!!!!!!!!!!!!!!!!!!!"
        #  x2---->x1    equal   dir??
        d = 0
        if x1 > x2:#right
            d = 4
        elif x1 < x2:#left
            d = 3
        elif y1 > y2:#down
            d = 2
        elif y1 < y2:#up
            d = 1
        else:
            pass
            # print "error #################"
            # print x1,y1
            # print x2,y2
        if d == dir:
            # print "tunnel has been blocked!!!"
            return True
        else:
            pass





    if fish_map.map[y][x] != 1:
        _x = x
        _y = y
        if has_own_member(own_list,_x,_y):
            return True

        _x = x-1
        _y = y
        if has_own_member(own_list,_x,_y):
            return True

        _x = x+1
        _y = y
        if has_own_member(own_list,_x,_y):
            return True

        _x = x
        _y = y-1
        if has_own_member(own_list,_x,_y):
            return True

        _x = x
        _y = y+1
        if has_own_member(own_list,_x,_y):
            return True
        return False

    else:
        return True

# def find_score3()



def score_enemy_direction(fish_map, m_task, teammate_list):
    c = 0
    dir = 0
    x0 = m_task.x
    y0 = m_task.y

    _x = x0
    _y = y0
    if not is_danger(fish_map,teammate_list,m_task,_x,_y):
        c+=1
        dir = 0

    _x = x0-1
    _y = y0
    if not is_danger(fish_map,teammate_list,m_task,_x,_y):
        c+=1
        dir = 3


    _x = x0+1
    _y = y0
    if not is_danger(fish_map,teammate_list,m_task,_x,_y):
        c+=1
        dir = 4


    _x = x0
    _y = y0-1
    if not is_danger(fish_map,teammate_list,m_task,_x,_y):
        c+=1
        dir = 1


    _x = x0
    _y = y0+1
    if not is_danger(fish_map,teammate_list,m_task,_x,_y):
        c+=1
        dir = 2
    # tmp_map = copy.deepcopy(fish_map)
    # for o in teammate_list:
    #     tmp_map.add_own(o)
    # a,b,c = catch_dirtction(tmp_map, m_task.x, m_task.y)
    return c,dir


def can_not_go(near_enemy,own_list,fish_map):
    _task = task(near_enemy.x,near_enemy.y,1)
    num = score_enemy_direction(fish_map,_task, own_list)
    if num == 0:
        return True
    else:
        return False

class position():
    def __init__(self,x,y):
        self.x = x
        self.y = y
def closed_by_position(x,y,pos_list):
    max_x = -1
    max_y = -1
    min_x = 999
    min_y = 999
    for p in pos_list:
        if p.x > max_x:
            max_x = p.x
        if p.y > max_y:
            max_y = p.y
        if p.x < min_x:
            min_x = p.x
        if p.y < min_y:
            min_y = p.y
    if x>= min_x-1 and x <= max_x+1 and y>=min_y-1 and y<=max_y+1:
        return True
    else:
        return False

def print_matrix(m):
    for _ in m:
        print
        for a in _:
            print("%-3s" % a),
    print