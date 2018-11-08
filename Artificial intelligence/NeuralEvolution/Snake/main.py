import network as nw

net = nw.Optimizer(25, 2, [1, 2, 3], [1, 2, 4, 8, 16])
networks = net.createGeneration(1000)

fitness = []
for network in networks:
    fitness.append([net.fitness(network), network])

print(fitness)