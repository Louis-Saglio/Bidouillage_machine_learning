from statistics import mean

from fourmi import *


NBR_FOURMIS = 1000
NBR_ITER = 300

graph = create_map(500)
nodes = list(graph)
base = choice(nodes)
while True:
    objectif = choice(nodes)
    if objectif != base:
        break
fourmis = [Fourmi(base, base, objectif) for _ in range(NBR_FOURMIS)]
fourmis[50].afficher = True

for i in range(NBR_ITER):
    for fourmi in fourmis:
        fourmi.run()

nx.draw(graph)
plt.draw()
plt.show()
