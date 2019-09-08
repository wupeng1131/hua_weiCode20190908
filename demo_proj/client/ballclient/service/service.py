# encoding:utf8
'''
业务方法模块，需要选手实现

选手也可以另外创造模块，在本模块定义的方法中填入调用逻辑。这由选手决定

所有方法的参数均已经被解析成json，直接使用即可

所有方法的返回值为dict对象。客户端会在dict前面增加字符个数。
'''
import random
import ballclient.service.constants as constants
from map import Map, meteor, tunnel, wormhole
from core import *
from util import *
from config import *
import time


def leg_start(msg):
    '''
    :param msg:
    :return: None
    '''
    if p_round_id:
        print "round start"
    if p_leg_start:
        # print "msg_name:%s" % msg['msg_name']
        # print "map_width:%s" % msg['msg_data']['map']['width']
        # print "map_height:%s" % msg['msg_data']['map']['height']
        # print "vision:%s" % msg['msg_data']['map']['vision']
        # print "meteor:%s" % msg['msg_data']['map']['meteor']
        # print "tunnel:%s" % msg['msg_data']['map']['tunnel']
        # print "wormhole:%s" % msg['msg_data']['map']['wormhole']
        print "teams:%s" % msg['msg_data']['teams']


    constants.version = msg['msg_data']['map']['vision']
    global fish_map
    fish_map = Map(msg)



    # write_obj('m_obj.data',fish_map)


def leg_end(msg):
    if p_round_id:
        print "round over"
    teams = msg["msg_data"]['teams']
    for team in teams:
        constants.score.append(team['id'])
        constants.score.append(team['point'])


def game_over(msg):
    print constants.score
    print constants.score[0],constants.score[1]+constants.score[5]
    print constants.score[2], constants.score[3] + constants.score[7]
    print "game over!"


def round(msg):

    round_id = msg['msg_data']['round_id']
    if p_round_id:
        print round_id
    players = msg['msg_data']['players']

    if 'power' in msg['msg_data']:
        power_list = build_power_list(msg['msg_data']['power'])
    else:
        power_list = []

    if 'players' in msg['msg_data']:
        enemy_list = build_enemy_list(msg['msg_data']['players'])

        own_list = build_own_list(msg['msg_data']['players'], msg['msg_data']['mode'])

    else:
        enemy_list = []
        own_list = []



    result = {
        "msg_name": "action",
        "msg_data": {
            "round_id": round_id
        }
    }



    action = []
    curr_mode = msg['msg_data']['mode']
    start = 0
    if p_round_time:
        start = time.time()

        ##########run djs for each fish and store##############
    game_mode = judge_mode(fish_map, curr_mode)
    start1 = time.time()
    if game_mode == 1:
        # start = time.time()
        m_graph = graph(fish_map, 0)
        for o in own_list:
            v = pos2idx(fish_map, o.x, o.y)
            o.dijkstra(v, fish_map, m_graph.matrix)
        # end = time.time()
        # print "the media time",end - start,"s"

    else:
        pass
    ########################

    result_alloc = allocate_task(fish_map, power_list, enemy_list, own_list, curr_mode)
    #connections   [a:own.id,    b: task.id, value, task_state]




    for r in result_alloc:
        # update the wander task
        for o in own_list:
            if r.a == o.id:
                fish_map.wander_task_check(o,0)
                break

        # take action

        a = fish_action(fish_map,r,curr_mode,power_list, enemy_list, own_list)
        action.append(a)


    # for player in players:
    #     if player['team'] == constants.team_id:
    #         a = fish_move(fish_map, player, power_list, enemy_list, own_list, curr_mode)
    #         action.append(a)

    end1 = time.time()
    print end1 - start1,"s"
    if p_round_time:
        end = time.time()
        print end - start
    result['msg_data']['actions'] = action
    return result
