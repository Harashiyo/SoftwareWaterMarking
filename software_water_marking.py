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
        for i in range(len(edge)):
            self.edge[i].sort()
        self.edge.sort()

    def set_zero_vertex(self):
        for i in range(self.num):
            self.vertex[i] = 0

    def get_adjacent_nodes(self, num):
        nodes = []
        i = 0
        n = len(self.edge)
        while(self.edge[i][0] < num):
            if self.edge[i][1] == num:
                nodes.append(self.edge[i][0])
            i += 1
            if i == n:
                break
        if i < n:
            while(self.edge[i][0] == num):
                nodes.append(self.edge[i][1])
                i += 1
                if i == n:
                    break
        return nodes

    def get_not_adjacent_nodes(self, num):
        nodes = []
        n = self.get_adjacent_nodes(num)
        if len(n) == 0:
            for i in range(self.num):
                if i == num:
                    nodes.append(i)
        else:
            j = 0
            for i in range(self.num):
                if i == num:
                    continue
                if j != len(n):
                    if i != n[j]:
                        nodes.append(i)
                    else:
                        j += 1
                else:
                    nodes.append(i)
        return nodes

    def get_adjacent_colors(self, num):
        colors = []
        nodes = self.get_adjacent_nodes(num)
        for i in nodes:
            if self.vertex[i] not in colors:
                colors.append(self.vertex[i])
        return colors


def gc(graph):
    u"""GC Algorithm.
    """
    g = Graph(graph.num, graph.edge)
    g.set_zero_vertex()
    color = 1
    for i in range(g.num):
        if g.vertex[i] == 0:
            g.vertex[i] = color
            nodes = g.get_not_adjacent_nodes(i)
            for j in nodes:
                if j > i:
                    colors = g.get_adjacent_colors(j)
                    if color not in colors and g.vertex[j] == 0:
                        g.vertex[j] = color
            color += 1
    return g


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
                for k in nodes:
                    if j == g.vertex[k]:
                        flag = False
                        break
                if flag:
                    g.vertex[i] = j
                    break
    return g


def icc(graph, message):
    u"""ICC Algorithm.
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
                for k in nodes:
                    if j == g.vertex[k] and (k < i or message[k] == 0):
                        flag = False
                        break
                if flag:
                    g.vertex[i] = j
                    break
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
    if math.floor(math.log2(math.factorial(color))) < m:
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
    for i in range(g.num):
        g.vertex[i] = p[g.vertex[i] - 1]
    return g


if __name__ == '__main__':
    e = [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5],
         [1, 2], [1, 3], [1, 4], [1, 5], [1, 6],
         [1, 7], [1, 8], [1, 9], [2, 3], [3, 4],
         [3, 5], [3, 6], [3, 7], [3, 8], [3, 9],
         [4, 5], [5, 6], [5, 7], [5, 8], [5, 9],
         [6, 7], [6, 8], [6, 9], [7, 8], [7, 9]]
    m = [1, 0, 1, 0, 1, 1, 0, 1, 0]
    n = 10
    g = Graph(n, e)
    cc = cp(g, m)
    print(cc.vertex)
