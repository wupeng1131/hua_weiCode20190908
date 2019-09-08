from util import *
from map import *
from graph import *
# import numpy as np
# import pyximport
# pyximport.install()
# from djs_ import *
import time
# import hello

m_map = read_obj('m_obj.data')
m_map.print_map()

#print_matrix(m_graph.matrix)
print
# hello.say_hello_to("asdfaasdfgasfd")



x1 = 0
y1 = 0
while 1:
    start = time.time()
    m_graph = graph(m_map,1)
    end = time.time()
    print "build:", end - start


    start = time.time()
    # path = djs.djs(m_graph.matrix, 0, 17, m_map)
    # control = move_direction(m_graph.matrix, m_map, x1,y1,17,18)
    control = m_graph.move_direction(m_map, x1, y1, 19, 1)
    end = time.time()
    print "run:",end - start


    print control



# idx1 = pos2idx(m_map,0,0)
# idx2 = pos2idx(m_map,10,15)
# print "source is:", idx2pos(m_map,idx1)
# print "destination is:", idx2pos(m_map,idx2)
# order = m_graph.dijkstra(idx1,idx2,m_map)
# print order
# for i in order:
#     print idx2pos(m_map,i)

