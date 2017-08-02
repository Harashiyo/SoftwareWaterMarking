# coding: utf-8
u"""Software Water Marking.

"""
import sys
import math


class Graph:
    u"""Graph Class."""

    def __init__(self, num, edge):
        self.num = num
        self.vertex = [0] * num
        for i in range(self.num):
            self.vertex[i] = i + 1
        self.edge = edge[:]
        self.edge.sort()

    def set_zero_vertex(self):
        for i in range(self.num):
            self.vertex[i] = 0

    def get_adjacent_nodes(self, num):
        nodes = []
        i = 0
        while(self.edge[i][0] < num):
            if self.edge[i][1] == num:
                nodes.append(self.edge[i][0])
            i += 1
        if i < self.num:
            while(self.edge[i][0] == num):
                nodes.append(self.edge[i][1])
                i += 1
                if i == self.num:
                    break
        return nodes


def gc(graph):
    u"""GC Algorithm.
    """
    g = Graph(graph.num, graph.edge)
    g.set_zero_vertex()
    color = 1
    for i in range(g.num):
        if g.vertex[i] == 0:
            g.vertex[i] = color
            for j in range(i + 1, g.num):
                if g.vertex[j] == 0 and check_color(g, color, j):
                    g.vertex[j] = color
            color += 1
    return g


def check_color(graph, color, num):
    u"""Determine whether vertices can be colored.
    """
    for i in range(num):
        if graph.vertex[i] == color and [i, num] in graph.edge:
            return False
    return True


def qp(graph, message):
    u"""QP Algorithm.
    """
    g = Graph(graph.num, graph.edge)
    message_count = 0
    for i in range(g.num):
        node_count = 0
        nodes = []
        for j in range(i + 1, g.num + i):
            if [min(i, j % g.num), max(i, j % g.num)] not in g.edge:
                nodes.append(j % g.num)
                node_count += 1
                if node_count == 2:
                    break
        if(node_count == 2):
            g.edge.append([min(nodes[message[message_count]], i),
                           max(nodes[message[message_count]], i)])
            message_count += 1
            if message_count == len(message):
                break
    if message_count != len(message):
        sys.exit()
    g.edge.sort()
    return gc(g)


def qps(graph, message):
    u"""QPS Algorithm.
    """
    g = gc(Graph(graph.num, graph.edge))
    color = max(g.vertex) + 1
    flags = []
    for i in range(g.num):
        flags.append(False)
    message_count = 0
    for i in range(len(g.vertex) - 2):
        if flags[i]:
            continue
        node_count = 0
        nodes = []
        for j in range(i + 1, len(g.vertex)):
            if g.vertex[i] == g.vertex[j] and flags[j] is False:
                nodes.append(j)
                node_count += 1
                if node_count == 2:
                    break
        if(node_count == 2):
            g.vertex[nodes[message[message_count]]] = color
            g.edge.append([i, nodes[message[message_count]]])
            color += 1
            message_count += 1
            if message_count == len(message):
                break
            flags[i] = True
            flags[nodes[0]] = True
            flags[nodes[1]] = True
    if message_count != len(message):
        sys.exit()
    g.edge.sort()
    return g


def cc(graph, message):
    u"""CC Algorithm.
    """
    m = len(message)
    if graph.num < m:
        sys.exit()
    g = gc(Graph(graph.num, graph.edge))
    for i in range(m, g.num):
        message.append(0)
    for i in range(g.num):
        if message[i] == 1:
            nodes = g.get_adjacent_nodes(i)
            for j in range(1, max(g.vertex) + 2):
                if j == g.vertex[i]:
                    continue
                flag = True
                for k in range(len(nodes)):
                    if j == g.vertex[nodes[k]]:
                        flag = False
                        break
                if flag:
                    g.vertex[i] = j
                    break
    return g


def icc(graph, message):
    u"""ICC Algorithm.
    """
    if len(graph.vertex) < len(message):
        sys.exit()
    else:
        for i in range(len(message), len(graph.vertex)):
            message.append(0)
    g = gc(Graph(graph.num, graph.edge))
    for i in range(len(message)):
        if message[i] == 1:
            color_min = max(g.vertex) + 1
            colors = [g.vertex[i]]
            for j in range(len(g.vertex)):
                edge = [i, j]
                edge.sort()
                if g.vertex[j] < color_min and edge not in g.edge and g.vertex[j] not in colors:
                    color_min = g.vertex[j]
                else:
                    colors.append(g.vertex[j])
            for j in range(i + 1, len(g.vertex)):
                edge = [i, j]
                edge.sort()
                if message[j] == 1 and g.vertex[j] < color_min and edge in g.edge:
                    color_min = g.vertex[j]
            g.vertex[i] = color_min
    return g


def cp(graph, message):
    u"""CP Algorithm.
    """
    m = len(message)
    M = 0
    for i in range(m):
        M += message[i] * 2 ** i
    g = gc(Graph(graph.num, graph.edge))
    color = max(g.vertex)
    if math.floor(math.log2(math.factorial(color))) < len(message):
        sys.exit()
    r = []
    for i in range(color):
        r.append(M // math.factorial((color - i - 1)))
        M %= math.factorial((color - i - 1))
    u = []
    for i in range(color):
        u.append(False)
    p = []
    for i in range(color):
        count = 0
        for j in range(color):
            if u[j] != True:
                if count == r[i]:
                    u[j] = True
                    p.append(j + 1)
                    break
                else:
                    count += 1
    for i in range(len(g.vertex)):
        g.vertex[i] = p[g.vertex[i] - 1]
    return g


if __name__ == '__main__':
    e = [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5],
         [1, 2], [1, 3], [1, 4], [1, 5], [1, 6],
         [1, 7], [1, 8], [1, 9], [2, 3], [3, 4],
         [3, 5], [3, 6], [3, 7], [3, 8], [3, 9],
         [4, 5], [5, 6], [5, 7], [5, 8], [5, 9],
         [6, 7], [6, 8], [6, 9], [7, 8], [7, 9]]
    m = [1, 0, 1, 0, 1, 1, 0, 1, 0, 0]
    n = 10
    g = Graph(n, e)
    cc = cc(g, m)
    print(cc.vertex)
