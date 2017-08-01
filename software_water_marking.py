# coding: utf-8
u"""Software Water Marking.

"""
import sys


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
    u"""QPS Algorithm.
    """
    if len(graph.vertex) < len(message):
        sys.exit()
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
            g.vertex[i] = color_min
    return g


def improved_cc(graph, message):
    u"""QPS Algorithm.
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


def check_color_extend(graph, color, num, N):
    u"""Determine whether vertices can be colored.
    """
    for i in range(N):
        edge = [i, num]
        edge.sort()
        if graph.vertex[i] == color and edge in graph.edge:
            return False
    return True


if __name__ == '__main__':
    e = [[0, 2], [0, 3], [1, 2], [1, 4], [3, 4]]
    m = [1, 0, 1, 1, 0]
    n = 5
    g = Graph(n, e)
    cc = improved_cc(g, m)
    print(cc.vertex)
    print(cc.edge)
