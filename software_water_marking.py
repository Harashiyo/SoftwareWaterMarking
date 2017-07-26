# coding: utf-8
u"""Software Water Marking.

"""


def gc(V, E):
    u"""GC Algorithm.
    @param V vertex
    @param E edge
    """
    N = len(V)
    result = [0] * N
    color = 1
    for i in range(N):
        if result[i] == 0:
            result[i] = color
            for j in range(i + 1, N):
                if result[j] == 0 and check_color(result, E, color, j):
                    result[j] = color
            color += 1
    return result


def check_color(V, E, C, N):
    u"""Determine whether vertices can be colored.
    @param V vertex
    @param E edge
    @param c color
    @param N vertex number
    """
    for i in range(N):
        if V[i] == C and [i, N] in E:
            return False
    return True


if __name__ == '__main__':
    V = [1, 2, 3, 4, 5]
    E = [[0, 1], [1, 3], [1, 4], [2, 3], [2, 4]]
    re = gc(V, E)
    print(re)
