import numpy as np
import random

class Network:
    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [[random.uniform(-1, 1) for i in range(sizes[t])] for t in range(self.num_layers)[1:]]
        self.weights = [[[random.uniform(-1, 1) for i in range(sizes[d - 1])] for t in range(sizes[d])] for d in range(self.num_layers)[1:]]

    def feedforward(self, x):
        self.activations = [[0 for n in range(self.sizes[t])] for t in range(len(self.sizes))]
        self.activations[0] = x
        for i in range(self.num_layers)[1:]:
            for t in range(self.sizes[i]):
                self.activations[i][t] = self.sigmoid(np.dot(self.activations[i - 1], self.weights[i - 1][t]) + self.biases[i - 1][t])
        return self.activations
    #Tools (math functions etc)
    def sigmoid(self, x):
        return 1.0 / (1 + np.exp(-x))
    def cost_derivative(self, output_activations, y):
        return (output_activations-y)
    def sigmoid_derivative(self, z):
        return self.sigmoid(z)*(1-self.sigmoid(z))