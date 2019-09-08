from util import *
import map
# import numpy as np
import copy
import time

# import djs
INF = float('inf')


def get_w0(matrix, m_map, x1, y1, x2, y2):
    if not m_map.has_space(x2, y2):
        return
    col = y1 * m_map.width + x1
    row = y2 * m_map.width + x2
    _val = m_map.map[y2][x2]
    if _val == 0:
        matrix[col][row] = 1
    elif _val == 1:  # meteor
        return
    elif _val == 2:  # tunnel(x2,y2)
        row1 = y2 * m_map.width + x2
        matrix[col][row1] = 1
        # the next position (x,y)
        x2, y2 = m_map.run_tunnel(x2, y2)
        row2 = y2 * m_map.width + x2
        matrix[row1][row2] = 1
    elif _val == 3:  # wormhole(x2,y2)
        row1 = y2 * m_map.width + x2
        matrix[col][row1] = 1  # bug!!!    1-3  dis is 1   3->1 also has road

        x2, y2 = m_map.run_wormhole(x2, y2)
        row2 = y2 * m_map.width + x2
        matrix[row1][row2] = 1
        matrix[row2][row1] = 1
    return


def get_w1(matrix, m_map, x1, y1, x2, y2):
    if not m_map.has_space(x2, y2):
        return
    # block = 222
    col = y1 * m_map.width + x1
    row = y2 * m_map.width + x2
    _val = m_map.map[y2][x2]
    if _val == 0:
        # if matrix[col][row] != block:
        matrix[col][row] = 1
    elif _val == 1:  # meteor
        return
    elif _val == 2:  # tunnel(x2,y2)
        row1 = y2 * m_map.width + x2
        matrix[col][row1] = 40
        # the next position (x,y)
        x2, y2 = m_map.run_tunnel(x2, y2)
        row2 = y2 * m_map.width + x2
        matrix[row1][row2] = 40
        # _x = x2-1
        # _y = y2
        # if m_map.is_space(_x,_y) or m_map.is_wormhole:
        #     _row = _y * m_map.width + _x
        #     matrix[_row][row2] = block
        #
        # _x = x2+1
        # _y = y2
        # if m_map.is_space(_x, _y) or m_map.is_wormhole:
        #     _row = _y * m_map.width + _x
        #     matrix[_row][row2] = block
        #
        # _x = x2
        # _y = y2-1
        # if m_map.is_space(_x, _y)or m_map.is_wormhole:
        #     _row = _y * m_map.width + _x
        #     matrix[_row][row2] = block
        #
        # _x = x2
        # _y = y2+1
        # if m_map.is_space(_x, _y)or m_map.is_wormhole:
        #     _row = _y * m_map.width + _x
        #     matrix[_row][row2] = block





    elif _val == 3:  # wormhole(x2,y2)
        row1 = y2 * m_map.width + x2
        matrix[col][row1] = 1  # bug!!!    1-3  dis is 1   3->1 also has road

        x2, y2 = m_map.run_wormhole(x2, y2)
        row2 = y2 * m_map.width + x2
        matrix[row1][row2] = 1
        # if matrix[row2][row1] != block:
        matrix[row2][row1] = 1
    return


class graph:
    def __init__(self, m_map,mode):
        n = m_map.width * m_map.height
        self.matrix = [[INF for i in range(n)] for j in range(n)]
        self.maxSize = 999
        for i in range(m_map.width):
            for j in range(m_map.height):
                # col = i * m_map.width + j
                val = m_map.map[j][i]
                if val == 0 or val == 3:  # pay attention to space
                    if mode == 0:  #aggressive
                        get_w0(self.matrix, m_map, i, j, i - 1, j)
                        get_w0(self.matrix, m_map, i, j, i + 1, j)
                        get_w0(self.matrix, m_map, i, j, i, j - 1)
                        get_w0(self.matrix, m_map, i, j, i, j + 1)
                    else:  #conservation
                        get_w1(self.matrix, m_map, i, j, i - 1, j)
                        get_w1(self.matrix, m_map, i, j, i + 1, j)
                        get_w1(self.matrix, m_map, i, j, i, j - 1)
                        get_w1(self.matrix, m_map, i, j, i, j + 1)

        for i in range(n):
            self.matrix[i][i] = 0
        # print self.matrix

    def printfPath(self, path, a):
        # path = path.astype(np.int32)
        # print path
        stack = [0 for i in range(self.maxSize)]
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

    def dijkstra(self, v, a, m_map):
        # print "v: ", v, "a:", a
        tmp = 0.0
        if v == a:
            dir = random.randint(1, 4)
            return dir
        n = m_map.width * m_map.height
        dist = [0 for i in range(n)]
        path = [0 for i in range(n)]
        _set = [0 for i in range(n)]
        for i in range(n):
            dist[i] = self.matrix[v][i]
            _set[i] = 0
            if (self.matrix[v][i] < INF):
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
            if u == a:
                break

            for j in range(n):
                # tmp = dist[u] + self.matrix[u][j]

                if _set[j] == 0 and dist[u] + self.matrix[u][j] < dist[j]:
                    dist[j] = dist[u] + self.matrix[u][j]

                    path[j] = u

        # end = time.time()
        # print "during:", end - start
        #################################
        # print path
        # print dist
        order = self.printfPath(path, a)
        if len(order) == 1:
            order.pop()
            order.append(v)
            order.append(v)

        # print order
        # print "::", order[0], order[1], "::"
        x0, y0 = idx2pos(m_map, order[0])
        x1, y1 = idx2pos(m_map, order[1])
        # print "!!!!!!!!!!!!!!!"

        dir = s_d(m_map, x0, y0, x1, y1)
        return dir

    def move_direction(self, m_map, x1, y1, x2, y2):

        v = pos2idx(m_map, x1, y1)
        a = pos2idx(m_map, x2, y2)
        width = m_map.width
        height = m_map.height

        # dir = djs.move_direction1(self.matrix, width, height, x1, y1,x2,y2)

        dir = self.dijkstra(v, a, m_map)
        return dir






