from typing import List


class Graph:
    def __init__(self):
        self.nodes: List['Node'] = []

    def add(self, value):
        if value not in self.nodes:
            self.nodes.append(Node(value))

    def remove(self, value):
        n = self[value]
        self.nodes.remove(n)
        for neighbour in n.neighbours:
            n - neighbour

    def __getitem__(self, item):
        for n in self.nodes:
            if n.value == item:
                return n
        raise IndexError

    def __contains__(self, item):
        for n in self.nodes:
            if n.value == item:
                return True
        return False

    def __str__(self):
        return 'Graph: %s' % str(self.nodes)

    __repr__ = __str__


class Node:
    def __init__(self, value, neighbours: List['Node'] = None):
        if neighbours is None:
            neighbours = []
        self.value = value
        self.neighbours: List['Node'] = neighbours

    def __add__(self, other: 'Node'):
        self.neighbours.append(other)
        other.neighbours.append(self)

    def __sub__(self, other: 'Node'):
        self.neighbours.remove(other)
        other.neighbours.remove(self)

    def __str__(self):
        return 'Node: %s' % str(self.value)

    __repr__ = __str__


def graph_format(n: 'Node', depth=3, done=None):
    if done is None:
        done = []
    out = ['└─> ' + str(n.value)]
    done.append(n)
    if len(n.neighbours) > 0 and depth > 0:
        for c in n.neighbours:
            if c not in done:
                out += ['\t' + x for x in graph_format(c, depth-1, done[:])]
    return out


def format_to_string(n: 'Node', depth=3) -> str:
    return '\n'.join(graph_format(n, depth))


g = Graph()
g.add(1)
g.add(2)
g.add(3)
g.add(4)
g.add(5)
g[1] + g[2]
g[2] + g[3]
g[2] + g[4]
g[4] + g[5]