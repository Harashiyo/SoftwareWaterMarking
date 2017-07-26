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
            if message_count == 3:
                break
    if message_count != 3:
        sys.exit()
    g.edge.sort()
    return gc(g)


if __name__ == '__main__':
    e = [[0, 1], [0, 4], [1, 2], [3, 4]]
    m = [1, 0, 1]
    n = 5
    g = Graph(n, e)
    gra = qp(g, m)
    print(gra.vertex)
