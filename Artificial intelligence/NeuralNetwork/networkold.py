import numpy as np
import random

class Network:
    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [[random.random() for i in range(sizes[t])] for t in range(self.num_layers)[1:]]
        self.weights = [[[random.random() for i in range(sizes[d - 1])] for t in range(sizes[d])] for d in range(self.num_layers)[1:]]

    def feedforward(self, x):
        self.activations = [[0 for n in range(self.sizes[t])] for t in range(len(self.sizes))]
        self.activations[0] = x
        for i in range(self.num_layers)[1:]:
            for t in range(self.sizes[i]):
                self.activations[i][t] = self.sigmoid(np.dot(self.activations[i - 1], self.weights[i - 1][t]) + self.biases[i - 1][t])
        return self.activations

    def feedforwardZ(self, x):
        self.activations = [[0 for n in range(self.sizes[t])] for t in range(len(self.sizes))]
        self.activations[0] = x
        for i in range(self.num_layers)[1:]:
            for t in range(self.sizes[i]):
                self.activations[i][t] = np.dot(self.activations[i - 1], self.weights[i - 1][t]) + self.biases[i - 1][t]
        return self.activations

    def train(self, training_data, epochs, batch_size, lr,
            test_data=None):
            if test_data: n_test = len(test_data)
            n = len(training_data)
            for e in xrange(epochs):
                random.shuffle(training_data)
                batches = [
                training_data[k:k+batch_size]
                for k in xrange(0, n, batch_size)]

                for batch in batches:
                    self.updateParameters(batch, lr)
                if test_data:
                    print "Epoch {0}: {1} / {2}".format(
                        e, self.evaluate(test_data), n_test)
                else:
                    print "Epoch {0} complete".format(e)

    def updateParameters(self, batch, lr):
        self.biases1d = np.array([[bias] for i in self.biases for bias in i])
        self.weights1d = np.array([[weight] for i in self.weights for weight in i])

        weightDerivative = [np.zeros(w.shape) for w in self.weights1d]
        biasDerivative = [np.zeros(b.shape) for b in self.biases1d]

        for x,y in batch:
            delta_biasDerivative, delta_weightDerivative = self.backprop(x, y)

            biasDerivative = [nb+dnb for nb, dnb in zip(biasDerivative, delta_biasDerivative)]
            weightDerivative = [nw+dnw for nw, dnw in zip(weightDerivative, delta_weightDerivative)]
            self.weights1d = [w-(lr/len(batch))*nw for w, nw in zip(self.weights1d, weightDerivative)]
            self.biases1d = [b-(lr/len(batch))*nb for b, nb in zip(self.biases1d, biasDerivative)]
    
    def backprop(self, x, y):
        der_b = [0 for b in self.biases1d]
        der_w = [0 for w in self.weights1d]

        # feedforward
        activations = self.feedforward(x.transpose()[0])[-1]
        zs = self.feedforwardZ(x.transpose()[0])[-1]

        # Backpropagate
        delta = self.cost_derivative(activations[-1], y) * \
            self.sigmoid_derivative(zs[-1])
        der_b[-1] = delta
        der_w[-1] = np.dot(delta, np.array(activations[-2]).transpose())

        for l in xrange(3, self.num_layers):
            z = zs[-l]
            sp = self.sigmoid_derivative(z)
            delta = np.dot(np.array(self.weights1d[-l+1][0]).transpose(), delta) * sp
            der_b[-l] = delta
            der_w[-l] = np.dot(delta, activations[-l-1].transpose())
        return (der_b, der_w)
    
    def evaluate(self, test_data):
        test_results = [(np.argmax(self.feedforward(x)[-1]), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)

    #Tools (math functions etc)
    def sigmoid(self, x):
        return 1.0 / (1 + np.exp(-x))
    def cost_derivative(self, output_activations, y):
        return (output_activations-y)
    def sigmoid_derivative(self, z):
        return self.sigmoid(z)*(1-self.sigmoid(z))