from __future__ import division
# from util import *
# from map import *
# from graph import *
# import numpy as np
# import pyximport
# pyximport.install()
# from djs_ import *
import time
# import hello
import math

# m_map = read_obj('m_ob1j.data')
# # m_map.print_map()
# m_graph = graph(m_map,0)
# print "start"
# start = time.time()
# nodes = m_graph.BFS(5,0,m_map)
# end = time.time()
# print "time is:", end-start,"s"
# m = [[99 for i in range(20)] for j in range(20) ]
#
# for node in nodes:
#     x = node.x
#     y = node.y
#     step = node.step
#     m[y][x] = step
# for _ in m:
#     print
#     for a in _:
#         print("%-3s"%a),


def Angle( x1,  y1,  x2,  y2):
    angle = 0.0;
    dx = x2 - x1
    dy = y2 - y1
    if  x2 == x1:
        angle = math.pi / 2.0
        if  y2 == y1 :
            angle = 0.0
        elif y2 < y1 :
            angle = 3.0 * math.pi / 2.0
    elif x2 > x1 and y2 > y1:
        angle = math.atan(dx / dy)
    elif  x2 > x1 and  y2 < y1 :
        angle = math.pi / 2 + math.atan(-dy / dx)
    elif  x2 < x1 and y2 < y1 :
        angle = math.pi + math.atan(dx / dy)
    elif  x2 < x1 and y2 > y1 :
        angle = 3.0 * math.pi / 2.0 + math.atan(dy / -dx)
    return (angle * 180 / math.pi)

def calc_angle(x1,y1,x2,y2):
    angle=0
    dy= y2-y1
    dx= x2-x1
    if dx==0 and dy>0:
        angle = 0
    if dx==0 and dy<0:
        angle = 180
    if dy==0 and dx>0:
        angle = 90
    if dy==0 and dx<0:
        angle = 270
    if dx>0 and dy>0:
       angle = math.atan(dx/dy)*180/math.pi
    elif dx<0 and dy>0:
       angle = 360 + math.atan(dx/dy)*180/math.pi
    elif dx<0 and dy<0:
       angle = 180 + math.atan(dx/dy)*180/math.pi
    elif dx>0 and dy<0:
       angle = 180 + math.atan(dx/dy)*180/math.pi
    return angle


n = 10
m = 5
for i in range(n-1,m-1,-1):
    print i


#print_matrix(m_graph.matrix)
# print
# hello.say_hello_to("asdfaasdfgasfd")



# x1 = 0
# y1 = 0
# while 1:
#     start = time.time()
#     m_graph = graph(m_map,1)
#     end = time.time()
#     print "build:", end - start
#
#
#     start = time.time()
#     # path = djs.djs(m_graph.matrix, 0, 17, m_map)
#     # control = move_direction(m_graph.matrix, m_map, x1,y1,17,18)
#     control = m_graph.move_direction(m_map, x1, y1, 19, 1)
#     end = time.time()
#     print "run:",end - start
#
#
#     print control



# idx1 = pos2idx(m_map,0,0)
# idx2 = pos2idx(m_map,10,15)
# print "source is:", idx2pos(m_map,idx1)
# print "destination is:", idx2pos(m_map,idx2)
# order = m_graph.dijkstra(idx1,idx2,m_map)
# print order
# for i in order:
#     print idx2pos(m_map,i)

