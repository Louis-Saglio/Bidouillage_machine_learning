from random import randint, choice

import networkx as nx
import matplotlib.pyplot as plt


class BadParmetreTypeError(BaseException):
    pass


def get_2d_distance(x: tuple, y: tuple):
    return ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** (1 / 2)


class Nodes(list):

    def show(self):
        graph = nx.Graph()
        for node in self:
            graph.add_node(node)
            for connected in node.connecteds:
                weight = get_2d_distance(node.position, connected.position)
                graph.add_edge(node, connected, weight=weight)
        nx.draw(graph, with_labels=True)
        plt.draw()
        plt.show()

    def auto_connect(self):
        nodes = [node for node in self]
        for node in self:
            if len(nodes) > 2:
                # TODO nettoyer
                other = node.find_nearest(nodes)
                node.connect(other)
                nodes.remove(other)
                other1 = node.find_nearest(nodes)
                node.connect(other1)
                nodes.insert(other.id, other)
                nodes.remove(node)

    def reduce_pheromone(self):
        for node in self:
            if node.pheromone > 0.1:
                node.pheromone -= 0.1
            else:
                node.pheromone = 0.0


class Node:

    # 2D pour une meilleur performance de recherche du plus proche
    nodes = Nodes()

    def __init__(self, x=None, y=None, limits=(100, 100)):
        self.id = len(Node.nodes)
        Node.nodes.append(self)
        self.connecteds = []
        x, y = randint(0, limits[0]) if x is None else x, randint(0, limits[1]) if y is None else y
        self.position = (x, y)
        self.pheromone = 0

    def __str__(self):
        # return str(self.__dict__)
        return str(self.id)

    def __repr__(self):
        return self.__str__()

    def get_distance(self, other):
        x, y = self.position, other.position
        return ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** (1 / 2)

    def find_nearest(self, liste=None):
        if liste is None:
            liste = [node for node in Node.nodes]
        liste.remove(self)
        rep = min(liste, key=self.get_distance)
        liste.insert(self.id, self)
        return rep

    def connect(self, other):
        self.connecteds.append(other)
        other.connecteds.append(self)


class Fourmi:
    fourmis = []

    def __init__(self, depart: Node, base: Node=None, objectif: Node=None):
        Fourmi.fourmis.append(self)
        self.depart = depart
        self.position = depart
        self.base = depart if base is None else base
        self.objectif = objectif
        self.historique = []
        self.check_errors()
        self.ordre = "Find"

    def move(self, node: Node):
        self.historique.append(self.position)
        self.position.pheromone += 1
        self.position = node

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()

    def check_errors(self):
        if not hasattr(self.depart, "connecteds") and not hasattr(self.base, "connecteds")\
                and not (hasattr(self.objectif, "connecteds") or self.objectif is None):
            raise TypeError(f"self.depart and self.base must have an attribute connecteds wich give the "
                            f"connected points in the map")


if __name__ == '__main__':
    for i in range(20):
        Node()
    carte = Node.nodes
    carte.auto_connect()
    base = carte[0]
    obj = carte[-1]
    base.id = "D"
    obj.id = "A"
    f1 = Fourmi(carte[0], objectif=carte[-1])
    for _ in range(3):
        carte.reduce_pheromone()
        f1.move(choice(f1.position.connecteds))
    print(f1)
    carte.show()
