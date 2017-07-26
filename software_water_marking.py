# coding: utf-8
u"""Software Water Marking.

"""


class Graph:
    u"""Graph Class."""
    vertex = []
    edge = []
    num = 0

    def __init__(self, num, edge):
        self.num = num
        self.__init__vertex()
        self.edge += edge

    def __init__vertex(self):
        for i in range(self.num):
            self.vertex.append(i + 1)


def gc(graph):
    u"""GC Algorithm.
    """
    result = [0] * graph.num
    color = 1
    for i in range(graph.num):
        if result[i] == 0:
            result[i] = color
            for j in range(i + 1, graph.num):
                if result[j] == 0 and check_color(result, graph.edge, color, j):
                    result[j] = color
            color += 1
    return result


def check_color(vertex, edge, color, num):
    u"""Determine whether vertices can be colored.
    """
    for i in range(num):
        if vertex[i] == color and [i, num] in edge:
            return False
    return True


if __name__ == '__main__':
    e = [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [1, 2], [1, 3],
         [1, 4], [1, 5], [1, 6], [2, 3], [2, 4], [2, 5], [2, 6], [5, 6]]
    g = Graph(7, e)
    g.vertex = gc(g)
    print(g.vertex)
