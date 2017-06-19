from random import randint, choice
from statistics import mean

import networkx as nx
import matplotlib.pyplot as plt
from copy import deepcopy


class InvalidOrder(BaseException):
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
            if node.pheromone > 1.1:
                node.pheromone -= 0.2
            else:
                node.pheromone = 1.0


class Node:

    # 2D pour une meilleur performance de recherche du plus proche
    nodes = Nodes()

    def __init__(self, x=None, y=None, limits=(100, 100)):
        self.id = len(Node.nodes)
        Node.nodes.append(self)
        self.connecteds = []
        x, y = randint(0, limits[0]) if x is None else x, randint(0, limits[1]) if y is None else y
        self.position = (x, y)
        self.pheromone = 1

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


class Fourmis(list):

    @staticmethod
    def auto_create(depart: Node, objectif: Node):
        Fourmi(depart, objectif=objectif)

    def run(self):
        for fourmi in self:
            fourmi.run()

    def moyenne(self):
        return mean([len(fourmi.itineraire) for fourmi in self if fourmi.itineraire is not None])


class Fourmi:
    fourmis = Fourmis()

    def __init__(self, depart: Node, objectif: Node):
        Fourmi.fourmis.append(self)
        self.depart = depart
        self.position = depart
        self.base = depart if base is None else base
        self.objectif = objectif
        self.historique = []
        self.check_errors()
        self.ordre = "Find"
        self.all = []
        self.itineraire = None

    def move(self, node: Node):
        self.all.append(node)
        if self.ordre == "Back":
            self.position.pheromone += 1
        elif self.ordre == "Find":
            self.historique.append(node)
        self.position = node
        if self.position == self.objectif:
            self.ordre = "Back"
            self.itineraire = deepcopy(self.historique)
        elif self.position == self.base:
            self.ordre = "Find"

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()

    def decide(self):
        if self.ordre == "Find":
            possibles = []
            for conn in self.position.connecteds:
                for _ in range(int(conn.pheromone)):
                    possibles.append(conn)
                if len(self.historique) > 1:
                    while self.historique[-2] in possibles:
                        possibles.remove(self.historique[-2])
            return choice(possibles)
        elif self.ordre == "Back":
            if self.objectif in self.historique:
                self.historique.remove(self.objectif)
            return self.historique.pop(-1)
        else:
            raise InvalidOrder(f"Ordre invalid {self.ordre}")

    def check_errors(self):
        if not hasattr(self.depart, "connecteds") and not hasattr(self.base, "connecteds")\
                and not (hasattr(self.objectif, "connecteds") or self.objectif is None):
            raise TypeError(f"self.depart and self.base must have an attribute connecteds wich give the "
                            f"connected points in the map")

    def run(self):
        self.move(self.decide())


if __name__ == '__main__':
    for i in range(20):
        Node()
    carte = Node.nodes
    carte.auto_connect()
    base = carte[0]
    obj = carte[randint(1, len(carte)-1)]
    base.id = "D"
    obj.id = "A"
    f1 = Fourmi(base, objectif=obj)
    for _ in range(200):
        carte.reduce_pheromone()
        f1.move(f1.decide())
    # while f1.position != obj:
    #     carte.reduce_pheromone()
    #     f1.run()
    print(f1)
    carte.show()
