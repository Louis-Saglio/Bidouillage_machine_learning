from random import randint, choice, sample

import networkx as nx
import matplotlib.pyplot as plt


def get_2d_distance(x: tuple, y: tuple):
    return ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** (1 / 2)


class Node:

    nodes = []

    def __init__(self, h, w):
        self.position = (randint(0, h), randint(0, w))
        self.connected = []
        self.family = ''.join(sample("azertyuiopqsdfghjklmwxcvbn", randint(4, 6)))
        self.pheromone = 0
        Node.nodes.append(self)

    def __str__(self):
        return f"Node_" + str(Node.nodes.index(self))

    def __repr__(self):
        return self.__str__()


def create_map2():
    G = nx.Graph()
    nodes = []
    for i in range(30):
        G.add_node(i)
        nodes.append({"x": randint(0, 100), "y": randint(0, 100)})
    for n in G:
        for _ in range(randint(1, 2)):
            o = choice(list(G))
            weight = get_2d_distance((nodes[o]["x"], nodes[o]["y"]), (nodes[n]["x"], nodes[n]["y"]))
            G.add_edge(n, o, weight=weight)
    nx.draw(G, with_labels=True)
    plt.draw()
    plt.show()


def create_map(nbr=30):
    g = nx.Graph()
    for _ in range(nbr):
        g.add_node(Node(nbr, nbr))
    for node in g:
        for _ in range(2):  # range(1, randint(randint(1, 2), randint(3, 4))):
            other = choice(list(g))
            weight = get_2d_distance(node.position, other.position)
            g.add_edge(node, other, weight=weight)
            if other not in node.connected:
                node.connected.append(other)
            other.family = node.family
            if node not in other.connected:
                other.connected.append(node)
    nodes_to_be_removed = []
    for node in g:
        if len(node.connected) == 0:
            nodes_to_be_removed.append(node)
    for node in nodes_to_be_removed:
        g.remove_node(node)
    # familys = []
    # for family in [node.family for node in g]:
    #     if family not in familys:
    #         familys.append(family)
    # print(familys)
    return g


if __name__ == '__main__':
    assert get_2d_distance((0, 0), (3, 4)) == 5
    create_map()
