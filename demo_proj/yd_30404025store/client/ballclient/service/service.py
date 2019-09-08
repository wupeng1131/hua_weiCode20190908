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
import time


def leg_start(msg):
    '''
    :param msg:
    :return: None
    '''
    print "round start"
    constants.version = msg['msg_data']['map']['vision']
    global fish_map
    fish_map = Map(msg)

    # write_obj('m_obj.data',fish_map)




def leg_end(msg):
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
    # print round_id
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
    '''add the wanderring target for fish'''
    # if round_id % 10 == 0:  #update each 10 round
    #     fish_map.update_wander_task()


    action = []
    curr_mode = msg['msg_data']['mode']
    # start = time.time()
    for player in players:
        if player['team'] == constants.team_id:
            a = fish_move(fish_map, player, power_list, enemy_list, own_list, curr_mode)
            action.append(a)
    # end = time.time()
    # print end - start
    result['msg_data']['actions'] = action
    return result
