import numpy as np

def sigmoid(x):
  return 1.0 / (1 + np.exp(-x))

class Network:
    def __init__(self, layers, layerLengths):
        self.biases = np.zeros((layers, 4))
        print(self.biases)
        #self.weights = np.random.rand(layers, 1, 1)
        for i in range(layers):
            self.biases[i].shape = (layerLengths[i])
            self.biases[i] = np.random.rand(layerLengths[i])
            self.weights[i] = np.random.rand(layerLengths[i], layerLengths[i - 1])
        self.output = np.zeros(layerLengths[len(layerLengths) - 1])

    def executeNetwork(self, x):
        self.activations[0] = x
        for i in range(len(self.weights))[0:]:
            self.activations[i] = sigmoid(np.dot(self.activations[i - 1], self.weights[i]))
        return self.activations