# coding: utf-8
u"""Software Water Marking.

"""


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


if __name__ == '__main__':
    e = [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [1, 2], [1, 3],
         [1, 4], [1, 5], [1, 6], [2, 3], [2, 4], [2, 5], [2, 6], [5, 6]]
    g = Graph(7, e)
    gra = gc(g)
    print(gra.vertex)
