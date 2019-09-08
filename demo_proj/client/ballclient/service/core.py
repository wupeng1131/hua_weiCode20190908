from __future__ import division
import ballclient.service.constants as constants
from util import *
import copy
from graph import *
from config import *
# import djs
INF = float('inf')

import random
# def can_go(m_map, x , y):
#
#     if (x >=0 and x < m_map.width) and (y >=0 and y <= m_map.height):
#
#         if m_map.map[y][x] == 1:
#             return False
#         else:
#             return True
#
#     else:
#         return False
#
# def rand_choose(a,b,c):
#     l = []
#     l.append(a)
#     l.append(b)
#     l.append(c)
#     idx = random.randint(0, 2) #bug (0,3)
#     return l[idx]
#
#
# def s2d(m_map, x1,y1,x2,y2):
#
#     if x2 > x1:
#         if can_go(m_map, x1+1, y1):
#             return 4
#         else:
#             return rand_choose(1,2,3)
#
#     if x2 < x1:
#         if can_go(m_map, x1-1, y1):
#             return 3
#         else:
#             return rand_choose(1, 2, 4)
#     if y2 > y1:
#         if can_go(m_map, x1, y1+1):
#             return 2
#         else:
#             return rand_choose(1, 3, 4)
#     if y2 < y1:
#         if can_go(m_map, x1, y1-1):
#             return 1
#         else:
#             return rand_choose(2, 3, 4)
#     else:
#         return random.randint(1, 4)

def aggressive_action(fish_map, task_alloc,power_list, enemy_list, own_list):
    me = own_list[0]
    for o in own_list:
        if o.id == task_alloc.a:
            me = o
            break
    # m_graph = graph(fish_map, 0)
    x = task_alloc.dx
    y = task_alloc.dy
    control = me.find_direction(fish_map,x,y)
        # m_graph.move_direction(fish_map, me.x, me.y, x, y)
    if p_round_info:
        print "id", me.id, "from(", me.x, me.y, ")", "to(", x, y, ")", task_alloc.info,"value:",task_alloc.value,"task_id:",task_alloc.b
    return control


def conservative_action(fish_map, task_alloc,power_list, enemy_list, own_list):
    me = own_list[0]
    for o in own_list:
        if o.id == task_alloc.a:
            me = o
            break
    tmp_map = copy.deepcopy(fish_map)
    for e in enemy_list:
        x1 = o.x
        y1 = o.y
        x2 = e.x
        y2 = e.y
        dist1 = abs(x1 - x2)
        dist2 = abs(y1 - y2)
        if dist1 <= constants.add_enemy_vision and dist2 <= constants.add_enemy_vision:
            tmp_map.add_enemy(e, o)

    x = task_alloc.dx
    y = task_alloc.dy
    control =me.find_direction(tmp_map,x,y)
        #m_graph.move_direction(tmp_map, me.x, me.y, x, y)
    if p_round_info:
        print "id", me.id, "from(", me.x, me.y, ")", "to(", x, y, ")", task_alloc.info,"value::",task_alloc.value
    return control


def fish_action(fish_map,task_alloc,curr_mode,power_list, enemy_list, own_list):
    game_mode = judge_mode(fish_map, curr_mode)
    m_direct = []
    if game_mode == 1:
        control = aggressive_action(fish_map, task_alloc,power_list, enemy_list, own_list)
    else:
        control = conservative_action(fish_map, task_alloc,power_list, enemy_list, own_list)

    m_direct.append(direction[control])
    if p_direct:
        print m_direct
    return {"team": constants.team_id, "player_id": task_alloc.a, "move": m_direct}

def allocate_task(fish_map, power_list, enemy_list, own_list, curr_mode):
    game_mode = judge_mode(fish_map, curr_mode)
    if game_mode == 1:
        result_alloc = aggressive_alloc(fish_map, power_list, enemy_list, own_list)
    else:
        result_alloc = conservative_alloc(fish_map, power_list, enemy_list, own_list)

    return result_alloc

def aggressive_alloc(fish_map, power_list, enemy_list, own_list):
    task_list = []

    result_connect = []

    for p in power_list:
        value = p.point
        x = p.x
        y = p.y
        _task = task(x,y,value)
        _task.info = "power_task"
        _task.id = len(task_list)
        task_list.append(_task)
    pos_list = []
    for o in own_list:
        p = position(o.x,o.y)
        pos_list.append(p)
    near_enemy = None
    if len(enemy_list) >= 1:
        nearest = 999
        for e in enemy_list:
            ave_dis = average_distance(own_list, e)
            if ave_dis < nearest:
                nearest = ave_dis
                near_enemy = e
        if closed_by_position(near_enemy.x, near_enemy.y, pos_list):
            pass  # 1.find the nearest enemy
        else:
            near_enemy = None

    if near_enemy != None:
        M_g = graph(fish_map, 0)
        x = near_enemy.x
        y = near_enemy.y
        v = pos2idx(fish_map, x, y)
        enemy_m = [[99 for i in range(fish_map.width)] for j in range(fish_map.width)]

        near_enemy.dijkstra(v,fish_map,M_g.matrix)
        for x in range(fish_map.width):
            for y in range(fish_map.width):
                dis=near_enemy.find_distance(fish_map,x,y)
                if dis == INF or fish_map.map[y][x] == 2:
                    pass
                else:
                    enemy_m[y][x] = int(dis)





        own_m_list = []
        for o in own_list:
            x = o.x
            y = o.y
            v = pos2idx(fish_map, x, y)
            e_m = [[99 for i in range(fish_map.width)] for j in range(fish_map.width)]

            for x in range(fish_map.width):
                for y in range(fish_map.width):
                    dis = o.find_distance(fish_map, x, y)
                    if dis == INF or fish_map.map[y][x] == 2:
                        pass
                    else:
                        e_m[y][x] = int(dis)
            own_m_list.append(e_m)

        own_m = [[99 for i in range(fish_map.width)] for j in range(fish_map.width)]

        for i in range(len(own_m)):
            for j in range(len(own_m)):
                min = 999
                for k in own_m_list:
                    if k[i][j] < min:
                        min = k[i][j]
                own_m[i][j] = min

        danger_m= [[99 for i in range(fish_map.width)] for j in range(fish_map.width)]
        for i in range(len(own_m)):
            for j in range(len(own_m)):
                if own_m[i][j] != 99:
                    dis = own_m[i][j] - enemy_m[i][j]
                    if dis>0: #is danger
                        danger_m[i][j] = 1
                    elif dis == 0:
                        danger_m[i][j] = -1
                    else:
                        danger_m[i][j] = 0

        # print "own matrix"
        # print_matrix(own_m)
        # print "enemy matrix"
        # print_matrix(enemy_m)
        print "danger matrix"
        print_matrix(danger_m)

    # find an enemy

    if near_enemy != None:
        can_catch = 1
        for i in range(len(own_m)): #i--->x
            for j in range(len(own_m)): #j--->y
                if danger_m[j][i] == 1 :
                    if not closed_by_position(i, j, pos_list):
                        can_catch = 1
                        break
        if can_catch == 1:
            flag = 0
            for i in range(len(own_m)):  # i--->x
                for j in range(len(own_m)):  # j--->y
                    if danger_m[j][i] == 1:
                        # if near_enemy.x == i and near_enemy.y == j and distance_(i,j )
                        value = 1000
                        x = i
                        y = j
                        _task = task(x, y, value)
                        _task.info = "enemy_power_task"
                        _task.id = len(task_list)
                        task_list.append(_task)
                        if flag == 0:
                            add_power_around_enemy(fish_map, near_enemy, value, task_list,danger_m)
                            flag = 1




    own_list_tmp = []
    for o in own_list:
        if o.task_state == 0:
            own_list_tmp.append(o)

    connection_list = []
    for o in own_list_tmp:
        _task = fish_map.wander_task[o.id]
        _task.id = len(task_list)
        task_list.append(_task)
        _connection = connection(o, _task,own_list,fish_map)
        connection_list.append(_connection)
        for t in task_list:
            if t.info == "wander_task":
                break
            else:
                _connection = connection(o,t,own_list,fish_map)
                connection_list.append(_connection)

    #******************************#
    # print_state(own_list)
    print "&&&&&&&&&&&&&&&",len(own_list_tmp),len(task_list)
    while to_be_alloc(own_list_tmp)  :
        _connection = choose_connection(connection_list)
        # print "choose",_connection.a,"---->", _connection.b, _connection.value
        own_id = _connection.a
        task_id = _connection.b
        delete_own(own_id, own_list, connection_list)
        delete_task(task_id, task_list, connection_list)
        result_connect.append(_connection)
    # for r in result_connect:
    #     print "result!!!:", r.a, "--->", r.direction, "x", r.dx, "y", r.dy

    #########################################







        #
        #
        # # for _ in m:
        # #     print
        # #     for a in _:
        # #         print("%-3s" % a),
        # set_n = 4
        # dir_list = []
        # for o in own_list:
        #     enemy2own = judge_task(near_enemy,o)#{1:up 2:down 3:left 4:right}
        #     # if not dir_overlap(dir_list,dir_enemy2own):
        #     # dir_list.append(dir_enemy2own)
        #     dis = distance_(o.x,o.y,near_enemy.x,near_enemy.y)
        #     print "enemy id:", near_enemy.id,"own id:",o.id,"catch_direction:",enemy2own
        #     dis_count = int(dis/2)
        #     x,y = search_limit(m,near_enemy.x,near_enemy.y,enemy2own, dis_count)
        #     value = 100
        #     _task = task(x, y, value)
        #     _task.info = "enemy_power"
        #     _task.id = len(task_list)
        #     task_list.append(_task)







        #
        # value = 0.9
        # x = near_enemy.x
        # y = near_enemy.y
        # _task = task(x, y, value)
        # _task.info = "enemy_task"
        # _task.id = len(task_list)
        # task_list.append(_task)
        # add_power_around_enemy(fish_map, near_enemy, value, task_list)




        # for e in enemy_list:
        #     # ave_dis = average_distance(fish_map,own_list,e)
        #     value = 100
        #     print "value of enemy:",e.id, "is",value
        #     x = e.x
        #     y = e.y
        #     _task = task(x, y, value)
        #     _task.info = "enemy_task"
        #     _task.id = len(task_list)
        #     task_list.append(_task)
        #     add_power_around_enemy(fish_map,e,value,task_list)

    # own_list----------task_list
    # connection_list = []
    # for o in own_list:
    #     for t in task_list:
    #         _connection = connection(o, t, own_list, fish_map)
    #         connection_list.append(_connection)

        #
        # _task = fish_map.wander_task[o.id]
        # _task.id = len(task_list)
        # task_list.append(_task)
        # _connection = connection(o, _task,own_list,fish_map)
        # connection_list.append(_connection)
        # for t in task_list:
        #     if t.info == "wander_task":
        #         break
        #     else:
        #         _connection = connection(o,t,own_list,fish_map)
        #         connection_list.append(_connection)



    #connection
    # result_alloc = []
    # print "the length of task list is ",len(task_list)
    # for t in task_list:
    #     print "(","id",t.id,t.x,t.y,")",
    # print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
    # print "the length of own list is ",len(own_list)
    # print "the lenght of connection is:", len(connection_list)
    # for t in own_list:
    #     print "(","id",t.id,t.x,t.y,")",
    ###bug!!!!!! own_list should restore
    # for o in own_list:
    #     o.task_state = 0
    # while to_be_alloc(own_list) and to_be_alloc(task_list) :
    #     # print_state(own_list)
    #     # print "^^^^^^^^^^^^^"
    #     # print_task_state(task_list)
    #     # print "WWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
    #     _connection = choose_connection(connection_list)
    #     # print "choose",_connection.a,"---->", _connection.b, _connection.value
    #     own_id = _connection.a
    #     task_id = _connection.b
    #     delete_own(own_id, own_list, connection_list)
    #     delete_task(task_id, task_list, connection_list)
    #     result_alloc.append(_connection)
    # for result in result_alloc:
    #     print "XXXXXXXXXXXXX",result.a,result.b
    return result_connect

def conservative_alloc(fish_map, power_list, enemy_list, own_list):
    task_list = []
    # start= time.time()

    for o in own_list:
        tmp_map = copy.deepcopy(fish_map)
        if len(enemy_list):
            for e in enemy_list:
                x1 = o.x
                y1 = o.y
                x2 = e.x
                y2 = e.y
                dist1 = abs(x1 - x2)
                dist2 = abs(y1 - y2)
                if dist1 <= constants.add_enemy_vision and dist2 <= constants.add_enemy_vision:
                    tmp_map.add_enemy(e, o)
        m_graph = graph(tmp_map, 1)
        v = pos2idx(tmp_map,o.x,o.y)
        o.dijkstra(v,tmp_map,m_graph.matrix)
    # end= time.time()
    # print "!!!!!!!!!!!!!!!!",end-start,"s"
    #**********************************************#

    for p in power_list:
        value = p.point
        x = p.x
        y = p.y
        _task = task(x, y, value)
        _task.info = "power_task"
        _task.id = len(task_list)
        task_list.append(_task)



    # own_list----------task_list
    connection_list = []
    for o in own_list:
        _task = fish_map.wander_task[o.id]
        _task.id = len(task_list)
        task_list.append(_task)
        _connection = connection(o, _task,own_list,tmp_map)
        connection_list.append(_connection)
        for t in task_list:
            if t.info == "wander_task":
                break
            else:
                _connection = connection(o, t,own_list,tmp_map)
                connection_list.append(_connection)
    # connection
    result_alloc = []
    # print "the length of task list is ",len(task_list)
    # for t in task_list:
    #     print "(",t.x,t.y,")",
    while to_be_alloc(own_list):
        _connection = choose_connection(connection_list)
        own_id = _connection.a
        task_id = _connection.b
        delete_own(own_id, own_list, connection_list)
        delete_task(task_id, task_list, connection_list)
        result_alloc.append(_connection)
    return result_alloc

def fish_move(fish_map, player, power_list, enemy_list, own_list, curr_mode):
    me = own(player['id'], player['score'], player['sleep'], player['x'], player['y'],curr_mode)
    m_direct = []
    game_mode = judge_mode(fish_map, curr_mode)

    if game_mode ==1:
        control = aggressive(fish_map, me, power_list, enemy_list, own_list)
    else:
        control = conservative(fish_map, me, power_list, enemy_list, own_list)

    m_direct.append(direction[control])
    if p_direct:
        print m_direct
    return {"team": player['team'], "player_id": player['id'], "move": m_direct}

def aggressive(fish_map, me, power_list, enemy_list, own_list):

    m_graph = graph(fish_map,0)


    task_list = []  # make a task list, the target are power and enemy

    #add task
    # 0
    idx = me.id
    fish_map.wander_task_check(me,0)
    _task = fish_map.wander_task[idx]
    task_list.append(_task)
    # 1
    for p in power_list:
        x1 = me.x
        y1 = me.y
        x2 = p.x
        y2 = p.y
        dist1 = abs(x1 - x2)
        dist2 = abs(y1 - y2)
        if dist1 <= constants.power_vision and dist2 <= constants.power_vision:
            value = p.point / distance_(x1, y1, x2, y2)
            _task = task(x2, y2, value)
            _task.info = "power_task"
            task_list.append(_task)
        else:
            pass
    # 2
    c_ = catch_enemy_count(own_list)
    if c_ <= constants.catch_enemy_count-1:
        for e in enemy_list:
            x1 = me.x
            y1 = me.y
            x2 = e.x
            y2 = e.y
            dist1 = abs(x1 - x2)
            dist2 = abs(y1 - y2)
            if dist1 <= constants.enemy_vision and dist2 <= constants.enemy_vision:
                # dist = distance(fish_map, x1, y1, x2, y2)
                dist = average_distance(fish_map,own_list,e)

                dist_corner = corner_distance(fish_map,e)
                # value = e.score + 10 / (dist2)  # decrease the value of enemy
                # value = (e.score + 10)*dist1 / (dist*constants.enemy_decay*10)
                # value = (10) * dist1 / (dist * constants.enemy_decay * 10)
                if constants.enemy_value_stragy == 1:
                    dist3 = distance(fish_map, x1, y1, x2, y2)
                    value = constants.enemy_value*2 / (dist3*dist_corner )
                # print "enemy",e.id,"score is",value*dist2
                else:
                    value = constants.treat_enemy_as/distance_(x1, y1, x2, y2)
                _task = task(x2, y2, value)
                _task.info = "enemy_task"
                task_list.append(_task)
        # _x = x2-1
        # _y = y2-1
        # if fish_map.has_space(_x,_y):
        #     dist = distance(fish_map, x1, y1, _x, _y)
        #     value = random.randint(0,5) / dist
        #     _task = task(_x, _y, value)
        #     task_list.append(_task)
        #
        # _x = x2+1
        # _y = y2+1
        # if fish_map.has_space(_x,_y):
        #     dist = distance(fish_map, x1, y1, _x, _y)
        #     value = random.randint(0,5) / dist
        #     _task = task(_x, _y, value)
        #     task_list.append(_task)
        #
        # _x = x2+1
        # _y = y2-1
        # if fish_map.has_space(_x,_y):
        #     dist = distance(fish_map, x1, y1, _x , _y)
        #     value = random.randint(0,5) / dist
        #     _task = task(_x, _y, value)
        #     task_list.append(_task)
        #
        # _x = x2-1
        # _y = y2+1
        # if fish_map.has_space(_x,_y):
        #     dist = distance(fish_map, x1, y1, _x , _y)
        #     value = random.randint(0,5) / dist
        #     _task = task(_x, _y, value)
        #     task_list.append(_task)

        # _x = x2 - 1
        # _y = y2
        # if fish_map.has_space(_x, _y):
        #     dist = distance(fish_map, x1, y1, _x, _y)
        #     value = 1 / dist
        #     _task = task(_x, _y, value)
        #     task_list.append(_task)
        # _x = x2 + 1
        # _y = y2
        # if fish_map.has_space(_x, _y):
        #     dist = distance(fish_map, x1, y1, _x, _y)
        #     value = 1 / dist
        #     _task = task(_x, _y, value)
        #     task_list.append(_task)
        # _x = x2
        # _y = y2 - 1
        # if fish_map.has_space(_x, _y):
        #     dist = distance(fish_map, x1, y1, _x, _y)
        #     value = 1 / dist
        #     _task = task(_x, _y, value)
        #     task_list.append(_task)
        # _x = x2
        # _y = y2 + 1
        # if fish_map.has_space(_x, _y):
        #     dist = distance(fish_map, x1, y1, _x, _y)
        #     value = 1 / dist
        #     _task = task(_x, _y, value)
        #     task_list.append(_task)


    m_task = choose_task(task_list)

    if m_task.info == "power_task":
        tmp = power_list[:]
        for p in tmp:
            if p.x == m_task.x and p.y == m_task.y:
                power_list.remove(p)

    if m_task.info == 'enemy_task':#specialize
        for o in own_list:
            if me.id == o.id:
                o.catch_enemy = 1

    if constants.catch_function:
        if m_task.info == 'enemy_task':#specialize
            control = catch_fish(fish_map,me,own_list,enemy_list,power_list,m_task)
            if p_round_info:
                print "id",me.id,"from(",me.x,me.y,")","to(",m_task.x, m_task.y,")", m_task.info
            return control





        #delete enemy for only one
        # tmp_list = enemy_list[:]
        # for e in tmp_list:
        #     if e.x == m_task.x and e.y == m_task.y:
        #         print "i want to catch fish",e.id
        #         pass
        #     else:
        #
        #         enemy_list.remove(e)

        # print "length of enemy_list:", len(enemy_list)



    # if m_task.info == 'enemy_task':#specialize
    #     #1 build a map with own list
    #     tmp_map = copy.deepcopy(fish_map)
    #     for o in own_list:
    #         tmp_map.add_own(o)
    #     #2 input: position ,  tmp_map  output: a vector
    #     a, b, c = catch_dirtction(tmp_map, m_task.x, m_task.y)
    #     if abs(a) + abs(b) == 1 : #no way to go, task is a direction
    #         d0 = distance_(me.x, me.y, m_task.x , m_task.y )
    #         d1 = distance_(me.x,me.y,m_task.x +a,m_task.y+b)
    #         if d1 > d0:                         #!!!!!!!!!!!!!!!!!!
    #             control = m_graph.move_direction(fish_map, me.x, me.y, me.x + a, me.y +b)
    #         else:
    #             control = m_graph.move_direction(fish_map, me.x, me.y, me.x - a, me.y -b)
    #
    #     elif  abs(a) + abs(b) == 0 and c == 0:   # == 2 or == 0  task is enemy
    #         control = 0
    #         # if abs(a)==1 and abs(b)==1:
    #         #     control = 0
    #         # else:
    #         #     control = m_graph.move_direction(fish_map, me.x, me.y, m_task.x, m_task.y)
    #     else:
    #         control = m_graph.move_direction(fish_map, me.x, me.y, m_task.x, m_task.y)
    if p_round_info:
        print "id",me.id,"from(",me.x,me.y,")","to(",m_task.x, m_task.y,")", m_task.info
    control = m_graph.move_direction(fish_map, me.x, me.y, m_task.x, m_task.y)


    # me and control  ---> update own list
    # for o in own_list:
    #     if me.x == o.x and me.y == o.y:
    #         update_position(o,control)
    # update_own_list(me, control, own_list)

    return control

    # if not len(power_list) and not len(enemy_list):# no task, wandering
    #     # fish_map.update_wander_task()
    #     idx = me.id
    #     m_task = fish_map.wander_task[idx]
    #     print "fish id",idx,"target(",m_task.x, m_task.y, ")"
    #     if use_cython == 1:
    #         control = djs.move_direction(m_graph.matrix, fish_map, me.x, me.y, m_task.x, m_task.y)
    #     else:
    #         control = m_graph.move_direction(fish_map, me.x, me.y, m_task.x, m_task.y)
    #     return control
    #
    # else:
    #     for p in power_list:
    #         x1 = me.x
    #         y1 = me.y
    #         x2 = p.x
    #         y2 = p.y
    #         dist1 = abs(x1 - x2)
    #         dist2 = abs(y1 - y2)
    #         if dist1 <= constants.vision  and dist2 <= constants.vision:
    #             value = p.point / distance_(x1,y1,x2,y2)
    #             _task = task(x2, y2, value)
    #             task_list.append(_task)
    #         else:
    #             pass
    #     for e in enemy_list:
    #         x1 = me.x
    #         y1 = me.y
    #         x2 = e.x
    #         y2 = e.y
    #         dist = distance(fish_map, x1, y1, x2, y2)
    #         value = 0 / dist  # decrease the value of enemy
    #         _task = task(x2, y2, value)
    #         task_list.append(_task)
    #     #finish task list, find the most valuable task
    #
    #     m_task = choose_task(task_list)
    #     #control = random.randint(1, 4)
    #     # control = s2d(fish_map, me.x, me.y, m_task.x, m_task.y)
    #     if use_cython == 1:
    #         control = djs.move_direction(m_graph.matrix, fish_map, me.x, me.y, m_task.x, m_task.y)
    #     else:
    #         control = m_graph.move_direction(fish_map, me.x, me.y, m_task.x, m_task.y)
    #     # control = m_graph.move_direction(fish_map, 0, 0, 10, 10)
    #
    #     return control


def conservative(fish_map, me, power_list, enemy_list, own_list):

    task_list = []  # make a task list, the target are power and enemy
    tmp_map = copy.deepcopy(fish_map)
    if len(enemy_list):
        for e in enemy_list:
            x1 = me.x
            y1 = me.y
            x2 = e.x
            y2 = e.y
            dist1 = abs(x1 - x2)
            dist2 = abs(y1 - y2)
            if dist1 <= constants.add_enemy_vision and dist2 <= constants.add_enemy_vision:
                tmp_map.add_enemy(e, me)
    m_graph = graph(tmp_map,1)

    # add task
    # 0
    idx = me.id
    fish_map.wander_task_check(me,1)
    _task = fish_map.wander_task[idx]
    task_list.append(_task)
    # 1
    for p in power_list:
        x1 = me.x
        y1 = me.y
        x2 = p.x
        y2 = p.y
        dist1 = abs(x1 - x2)
        dist2 = abs(y1 - y2)
        if dist1 <= constants.power_vision and dist2 <= constants.power_vision:
            if tmp_map.map[y2][x2] ==0:   #bug!!!!!!!!!!!
                value = p.point / distance_(x1, y1, x2, y2)
                _task = task(x2, y2, value)
                _task.info = "power_task"
                task_list.append(_task)
            else:
                # print "!!!!!!!!!!!!! power is enemy"
                pass
        else:
            pass

    m_task = choose_task(task_list)
    if m_task.info == "power_task":
        tmp = power_list[:]
        for p in tmp:
            if p.x == m_task.x and p.y == m_task.y:
                power_list.remove(p)
    if p_round_info:
        print "id", me.id, "from(", me.x, me.y, ")", "to(", m_task.x, m_task.y, ")",m_task.info
    control = m_graph.move_direction(tmp_map, me.x, me.y, m_task.x, m_task.y)
    return control

    # if not len(power_list):
    #     idx = me.id
    #     m_task = fish_map.wander_task[idx]
    #
    #     if use_cython == 1:
    #         control = djs.move_direction(m_graph.matrix, tmp_map, me.x, me.y, m_task.x, m_task.y)
    #     else:
    #         control = m_graph.move_direction(tmp_map, me.x, me.y, m_task.x, m_task.y)
    #     return control
    #
    # else:
    #     for p in power_list:
    #         x1 = me.x
    #         y1 = me.y
    #         x2 = p.x
    #         y2 = p.y
    #         dist = distance(tmp_map, x1, y1, x2, y2)
    #         value = p.point / dist
    #         _task = task(x2, y2, value)
    #         task_list.append(_task)
    #     m_task = choose_task(task_list)
    #     if use_cython == 1:
    #         control = djs.move_direction(m_graph.matrix, tmp_map, me.x, me.y, m_task.x, m_task.y)
    #     else:
    #         control = m_graph.move_direction(tmp_map, me.x, me.y, m_task.x, m_task.y)
    #     return control


def catch_fish(fish_map, me, own_list, enemy_list,power_list, m_task):
    #1  me
    #2  m_task
    teammate_list = []
    task_list = []
    enemy_value = 1
    for o in own_list:
        task_list_tmp = []
        for p in power_list:
            x1 = o.x
            y1 = o.y
            x2 = p.x
            y2 = p.y
            dist1 = abs(x1 - x2)
            dist2 = abs(y1 - y2)
            if dist1 <= constants.power_vision and dist2 <= constants.power_vision:
                value = p.point / distance_(x1, y1, x2, y2)
                _task = task(x2, y2, value)
                _task.info = "power_task"
                task_list_tmp.append(_task)
            else:
                pass
        #
        for e in enemy_list:
            x1 = o.x
            y1 = o.y
            x2 = e.x
            y2 = e.y

            dist1 = abs(x1 - x2)
            dist2 = abs(y1 - y2)
            if dist1 <= constants.enemy_vision and dist2 <= constants.enemy_vision:
                dist3 = distance(fish_map, x1, y1, x2, y2)
                dist = enemy_distance(fish_map, own_list, e)
                # value = e.score + 10 / (dist*10)  # decrease the value of enemy
                dist1 = center_distance(fish_map, e)
                dist_corner = corner_distance(fish_map, e)
                # value = (e.score + 10)*dist1 / (dist*constants.enemy_decay*10)
                # value = (10) * dist1 / (dist * constants.enemy_decay * 10)
                # dist = distance(fish_map, x1, y1, x2, y2)
                # value = e.score + 10 / (dist2)  # decrease the value of enemy
                # value = 1 / (dist2)
                value = constants.enemy_value*2 / (dist3*dist_corner)
                _task = task(x2, y2, value)
                _task.info = "enemy_task"
                task_list_tmp.append(_task)

            # dist = distance(fish_map, x1, y1, x2, y2)
            # value = e.score +10 / dist  # decrease the value of enemy
            #
            # _task = task(x2, y2, value)
            # _task.info = "enemy_task"
            # task_list_tmp.append(_task)
        if len(task_list_tmp) !=0:
            _task = choose_task(task_list_tmp)
            task_list.append([o, _task])

    # member and its task
    for i in range(len(task_list)):
        if task_list[i][1].x == m_task.x and task_list[i][1].y == m_task.y:
            teammate_list.append(task_list[i][0])

    #
    # for i in range(len(teammate_list)):
    #     print teammate_list[i].id, task_list[i][1].x, task_list[i][1].y


    # teammate: in  teammate_list[],   task: m_task

    s = 5
    state_space = find_state_space(teammate_list, s)
    # print len(state_space)
    # state_space
    min_space = []
    min_score = 999999
    teammate_list_ = []
    for space in state_space:
        #score1: distance score2:the number of over lap  score3: direction enemy can go
        direct_list = []
        for d in space:
            direct_list.append(d)
        #update position
        teammate_list_ = copy.deepcopy(teammate_list)
        for i in range(len(teammate_list_)):
            update_teammate_list(fish_map,teammate_list_[i],direct_list[i])

        # direct_list
        ###################################
        #find the number of direction
        num_direct,dir= score_enemy_direction(fish_map,m_task, teammate_list)
        if num_direct == 1 or num_direct == 0:
            # print "******************i have lock it!!!!!!!!!!!!!!!!!!!"
            _x,_y = next_pos(dir, m_task.x, m_task.y)
            m_task.x = _x
            m_task.y = _y
            # print "next position is", m_task.x,m_task.y
        else:
            pass
        ###################################
        score1 = score_distance(fish_map,m_task,teammate_list_,me)

        score2 = score_overlap(teammate_list_)

        score3 = 0
        # if num_direct==0:
        #     score3, _ = score_enemy_direction1(fish_map, m_task, teammate_list_)





        score3,_ = score_enemy_direction(fish_map,m_task, teammate_list_)
        # print score1, score2#, score3,  "space",space

        score = score1 + score2*2 + score3
        # score = score1 + score3

        if score < min_score:
            min_score = score
            min_space = space
    # print "last result!!!!!",min_score, min_space
    idx = 0
    for i in range(len(teammate_list_)):
        if me.id == teammate_list_[i].id:
            # print "find it!!!!!!!!!!"
            idx = i
            break
        # print "do not find it!!!!!!!!"
    # print "position is!!!!!!!!!!!!!!!!!", idx, min_space
    # print
    # print
    # print

    return min_space[idx]


def djs_distance(m_map,x1,x2,y1,y2):
    m_graph = graph(m_map,0)
    v = pos2idx(m_map, x1, y1)
    a = pos2idx(m_map, x2, y2)
    _,path = m_graph.dijkstra(v,a,m_map)
    dist = path[a]
    return dist


def score_distance(m_map,m_task,teammate_list,me):
    dis = 0
    #
    # idx = 0
    # for i in range(len(teammate_list)):
    #     if me.id == teammate_list[i].id:
    #         # print "find it@@@@@@@@@@"
    #         idx = i

    #         break
    #
    # dis = distance_0(m_task.x, m_task.y,teammate_list[idx].x,teammate_list[idx].y)
    # print "from:" ,teammate_list[idx].x,teammate_list[idx].y ,"to:",m_task.x, m_task.y
    # print "distance is:",
    for o in teammate_list:
        d_ = distance_0(m_task.x, m_task.y, o.x, o.y)
        # print d_,
        dis += d_

    return dis


def score_overlap(teammate_list):
    tmp = []
    for t in teammate_list:
        num = t.x*100 + t.y
        tmp.append(num)
    tmp_set = set(tmp)
    count = len(tmp)- len(tmp_set)
    return count


def find_state_space(teammate_list,s):
    state_space = []
    if len(teammate_list) == 1:
        for i in range(1,s):
            tmp = []
            tmp.append(i)
            state_space.append(tmp)

    elif len(teammate_list) == 2:
        for i in range(1,s):
            for j in range(1,s):
                tmp = []
                tmp.append(i)
                tmp.append(j)
                state_space.append(tmp)

    elif len(teammate_list) == 3:
        for i in range(1,s):
            for j in range(1,s):
                for k in range(1,s):
                    tmp = []
                    tmp.append(i)
                    tmp.append(j)
                    tmp.append(k)
                    state_space.append(tmp)
    else:  # == 4
        for i in range(1,s):
            for j in range(1,s):
                for k in range(1,s):
                    for l in range(1,s):
                        tmp = []
                        tmp.append(i)
                        tmp.append(j)
                        tmp.append(k)
                        tmp.append(l)
                        state_space.append(tmp)
    return state_space


