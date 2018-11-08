import numpy as np
import game
import neuralNet as nn
import random

class Optimizer(object):
    def __init__(self, firstLayerLength, lastLayerLength, layerLengths, neuronLengths, compressionMethod=['relu', 'elu', 'tanh', 'sigmoid'], retain=0.4, random_select=0.1, mutate_chance=0.2):
        self.firstLayerLength = firstLayerLength
        self.lastLayerLength = lastLayerLength
        self.neuronLengths = neuronLengths
        self.layerLengths = layerLengths
        self.compressionMethod = compressionMethod
        self.retain = retain
        self.random_select = random_select
        self.mutate_chance = mutate_chance
        self.snakeSize = 5
    def createGeneration(self, length):
        networks = []
        for i in range(length):
            self.layers = [self.firstLayerLength]
            midLayerLength = random.choice(self.layerLengths)
            for l in range(midLayerLength):
                self.layers.append(random.choice(self.neuronLengths))
            self.layers.append(self.lastLayerLength)
            net = nn.Network(self.layers)
            networks.append(net)
        print(networks[-1].sizes)
        return networks
    def fitness(self, network):
        g = game.SnakeGame(self.snakeSize, 1)
        steps = 0
        totalSteps = 0
        while g.go == False and steps < 60:
            if totalSteps > 0:
                prevLength = len(g.pos)
            a = [t for i in g.board for t in i]
            activations = network.feedforward(a)
            x = activations[-1][0]
            y = activations[-1][1]
            
            if (x < 0.5 and y < 0.5 and x >= y) or (x < 0.5 and y >= 0.5 and x >= (y - 0.5)):
                step = [-1, 0]
            elif (x >= 0.5 and y >= 0.5 and x >= y) or (x >= 0.5 and y < 0.5 and x >= (y + 0.5)):
                step = [1, 0]
            elif (y < 0.5 and x < 0.5 and y > x) or (y < 0.5 and x >= 0.5 and y > (x - 0.5)):
                step = [0, -1] 
            else:
                step = [0, 1]
            
            g.step(step)

            if totalSteps > 0:
                if prevLength == len(g.pos):
                    steps = steps + 1
                if len(g.pos) > prevLength:
                    steps = 0
            totalSteps = totalSteps + 1
        return len(g.pos)