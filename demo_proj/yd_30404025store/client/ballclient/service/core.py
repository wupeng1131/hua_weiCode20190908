from __future__ import division
import ballclient.service.constants as constants
from util import *
import copy
from graph import *
# import djs

import random

use_cython = 0

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

def distance1(fish, power):
    x1 = fish.x
    y1 = fish.y
    x2 = power.x
    y2 = power.y
    dist = abs(x1 - x2) + abs(y1 - y2)
    return dist



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


def fish_move(fish_map, player, power_list, enemy_list, own_list, curr_mode):
    me = own(player['id'], player['score'], player['sleep'], player['x'], player['y'],curr_mode)
    m_direct = []
    game_mode = judge_mode(fish_map, curr_mode)

    if game_mode ==1:    #game_mode 1: aggressive
        control = aggressive(fish_map, me, power_list, enemy_list, own_list)
    else:                #game_mode 0:conservative
        control = conservative(fish_map, me, power_list, enemy_list, own_list)

    m_direct.append(direction[control])
    # print m_direct
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
    for e in enemy_list:
        x1 = me.x
        y1 = me.y
        x2 = e.x
        y2 = e.y
        dist1 = abs(x1 - x2)
        dist2 = abs(y1 - y2)
        if dist1 <= constants.enemy_vision and dist2 <= constants.enemy_vision:
            # dist = distance(fish_map, x1, y1, x2, y2)
            # dist2 = distance(fish_map, x1, y1, x2, y2)
            # dist = enemy_distance(fish_map,own_list,e)
            # dist1 = center_distance(fish_map,e)
            # dist_corner = corner_distance(fish_map,e)
            # value = e.score + 10 / (dist2)  # decrease the value of enemy
            # value = (e.score + 10)*dist1 / (dist*constants.enemy_decay*10)
            # value = (10) * dist1 / (dist * constants.enemy_decay * 10)
            #value = constants.enemy_value*2 / (dist2*dist_corner )
            # print "enemy",e.id,"score is",value*dist2
            value = 1/distance_(x1, y1, x2, y2)
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

    # if m_task.info == 'enemy_task':#specialize
    #     control = catch_fish(fish_map,me,own_list,enemy_list,power_list,m_task)
    #     # print "id",me.id,"from(",me.x,me.y,")","to(",m_task.x, m_task.y,")", m_task.info
    #     return control





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

    # print "id",me.id,"from(",me.x,me.y,")","to(",m_task.x, m_task.y,")", m_task.info
    control = m_graph.move_direction(fish_map, me.x, me.y, m_task.x, m_task.y)


    # me and control  ---> update own list
    # for o in own_list:
    #     if me.x == o.x and me.y == o.y:
    #         update_position(o,control)


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
            if dist1 <= constants.vision and dist2 <= constants.vision:
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
    # print "id", me.id, "from(", me.x, me.y, ")", "to(", m_task.x, m_task.y, ")",m_task.info
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
                dist2 = distance(fish_map, x1, y1, x2, y2)
                dist = enemy_distance(fish_map, own_list, e)
                # value = e.score + 10 / (dist*10)  # decrease the value of enemy
                dist1 = center_distance(fish_map, e)
                dist_corner = corner_distance(fish_map, e)
                # value = (e.score + 10)*dist1 / (dist*constants.enemy_decay*10)
                # value = (10) * dist1 / (dist * constants.enemy_decay * 10)
                # dist = distance(fish_map, x1, y1, x2, y2)
                # value = e.score + 10 / (dist2)  # decrease the value of enemy
                # value = 1 / (dist2)
                value = constants.enemy_value*2 / (dist2*dist_corner)
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
        score1 = score_distance(m_task,teammate_list_,me)

        score2 = score_overlap(teammate_list_)

        score3 = 0
        # if num_direct==0:
        #     score3, _ = score_enemy_direction1(fish_map, m_task, teammate_list_)





        #score3,_ = score_enemy_direction(fish_map,m_task, teammate_list_)
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







def score_distance(m_task,teammate_list,me):
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

def score_enemy_direction1(fish_map, m_task, teammate_list_,teammate_list):
    pass

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


