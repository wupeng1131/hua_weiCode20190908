import numpy as np
cimport numpy as np
cimport cython
import time
from util import *
# cdef np.ndarray[np.float32_t,ndim = 1]
INF = float('inf')


def printfPath(path, a):
    path = path.astype(np.int32)
    # print path
    stack = np.zeros(999, dtype=float)
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


############################
cdef int djs(np.ndarray matrix, int v, int a, m_map):
    cdef int dir
    if v == a:
        dir = random.randint(1, 4)
        return dir
    cdef float inf = 9999999
    cdef int n = m_map.width * m_map.height
    cdef np.ndarray dist = np.zeros(n, dtype=float)
    cdef np.ndarray path = np.zeros(n, dtype=float)
    cdef np.ndarray _set = np.zeros(n, dtype=float)
    cdef int i
    cdef int j
    cdef int u
    cdef float tmp
    for i in range(n):
        dist[i] = matrix[v][i]
        _set[i] = 0
        if(matrix[v][i] < inf):
            path[i] = v
        else:
            path[i] = -1

    _set[v] = 1
    path[v] = -1
    u = 0

    for i in range(n-1):
        min = inf
        for j in range(n):
            if _set[j] == 0 and dist[j] < min:
                u = j
                min = dist[j]
        _set[u] = 1
        if u == a:
            break

        for j in range(n):
            tmp = dist[u] + matrix[u][j]
            if _set[j] == 0 and tmp < dist[j]:
                dist[j] = tmp
                path[j] = u



    order = printfPath(path, a)
    if len(order)==1:
        order.append(order[0])
    # print order
    # print "::", order[0], order[1], "::"
    x0, y0 = idx2pos(m_map,order[0])
    x1, y1 = idx2pos(m_map,order[1])
    # print "!!!!!!!!!!!!!!!"

    dir = s_d(x0,y0,x1,y1)
    return dir


###########################
def dijkstra(matrix, v, a, m_map):
    n = m_map.width * m_map.height
    dist = np.zeros(n, dtype=float)
    path = np.zeros(n, dtype=float)
    _set = np.zeros(n, dtype=float)
    for i in range(n):
        dist[i] = matrix[v][i]
        _set[i] = 0
        if(matrix[v][i] < INF):
            path[i] = v
        else:
            path[i] = -1

    _set[v] = 1
    path[v] = -1
    u = 0




    start = time.time()
    for i in range(n-1):
        min = INF
        for j in range(n):
            if _set[j] == 0 and dist[j] < min:
                u = j
                min = dist[j]
        _set[u] = 1

        for j in range(n):
            if _set[j] == 0 and dist[u] + matrix[u][j] < dist[j]:
                dist[j] = dist[u] + matrix[u][j]
                path[j] = u
    end = time.time()
    print "during:", end -start

    #################################
    #print path
    #print dist
    order = printfPath(path, a)
    if len(order)==1:
        order.append(order[0])
    # print order
    # print "::", order[0], order[1], "::"
    x0, y0 = idx2pos(m_map,order[0])
    x1, y1 = idx2pos(m_map,order[1])
    # print "!!!!!!!!!!!!!!!"

    dir = s_d(x0,y0,x1,y1)
    return x1,y1, dir


def move_direction(matrix,m_map, x1, y1, x2, y2):


    v = pos2idx(m_map,x1,y1)
    a = pos2idx(m_map,x2,y2)
    start = time.time()
    dir = djs(matrix, v, a, m_map)
    end = time.time()
    # print "during time:", end - start
    return dir


# cdef int djs1(np.ndarray matrix,int width, int height, int v, int a):
#     INF = float('inf')
#     cdef int n = width * height
#     cdef int i
#     cdef int j
#     cdef np.ndarray dist = np.zeros(n, dtype=float)
#     cdef np.ndarray path = np.zeros(n, dtype=float)
#     cdef np.ndarray _set = np.zeros(n, dtype=float)
#     for i in range(n):
#         dist[i] = matrix[]





def say_hello_to(name):
    print "-->", name
    print name