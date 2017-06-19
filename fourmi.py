from os import system
from pprint import pprint

from helpers import *


class Fourmi:

    def __init__(self, node: Node, base, objectif):
        self.historique = [node]
        self.position = node
        self.ordre = "Find"
        self.objectif = objectif
        self.base = base
        self.itineraire = None
        self.afficher = False

    def manage_mission(self):
        if self.position == self.objectif:
            self.ordre = "Back"
            self.itineraire = self.historique
        if self.position == self.base:
            self.ordre = "Find"

    def decide(self):
        dirs = []
        for connected in self.position.connected:
            for _ in range(int(connected.pheromone + 1)):
                dirs.append(connected)
        if len(dirs) > 1 and self.position and len(self.historique) > 0 and self.position is not self.historique[-1]:
            dirs.remove(self.historique[-1])
        return choice(dirs)

    def move(self):
        node = self.decide()
        self.historique.append(node)
        self.position = node

    def go_back(self):
        self.position.pheromone += 1
        if len(self.historique) > 0:
            self.position = self.historique.pop(len(self.historique)-1)

    def run(self):
        self.manage_mission()
        if self.afficher and self.itineraire is not None:
            print(len(self.itineraire))
        if self.ordre == "Find":
            self.move()
        elif self.ordre == "Back":
            self.go_back()


if __name__ == '__main__':
    graph = create_map(5)
    nodes = list(graph)
    f1 = Fourmi(nodes[0], nodes[0], nodes[4])
    for i in range(40):
        try:
            f1.run()
        except:
            pprint(f1.__dict__)
            raise Exception
        print('')
    pprint(f1.__dict__)
