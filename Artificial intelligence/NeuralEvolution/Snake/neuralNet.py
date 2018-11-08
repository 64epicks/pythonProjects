import numpy as np
import random

class Network:
    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]

    def feedforward(self, a):
        for b, w in zip(self.biases, self.weights):
            a = self.sigmoid(np.dot(w, a)+b)
        return a

    def feedforwardZ(self, a):
        for b, w in zip(self.biases, self.weights):
            a = np.dot(w, a)+b
        return a

    def train(self, training_data, epochs, batch_size, lr,
        test_data=None):
        if test_data: n_test = len(test_data)
        n = len(training_data)
        for j in xrange(epochs):
            random.shuffle(training_data)
            batches = [
                training_data[k:k+batch_size]
                for k in xrange(0, n, batch_size)]
            for batch in batches:
                self.learn(batch, lr)
            if test_data:
                print "Epoch {0}: {1} / {2}".format(
                    j, self.evaluate(test_data), n_test)
            else:
                print "Epoch {0} complete".format(j)
    def learn(self, batch, lr):
        der_b = [np.zeros(b.shape) for b in self.biases]
        der_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in batch:
            delta_der_b, delta_der_w = self.backprop(x, y)
            der_b = [nb+dnb for nb, dnb in zip(der_b, delta_der_b)]
            der_w = [nw+dnw for nw, dnw in zip(der_w, delta_der_w)]
        self.weights = [w-(lr/len(batch))*nw
                        for w, nw in zip(self.weights, der_w)]
        self.biases = [b-(lr/len(batch))*nb
                       for b, nb in zip(self.biases, der_b)]

    def backprop(self, x, y):
        der_b = [np.zeros(b.shape) for b in self.biases]
        der_w = [np.zeros(w.shape) for w in self.weights]
        # feedforward
        activation = x
        activations = [x] # list to store all the activations, layer by layer
        zs = [] # list to store all the z vectors, layer by layer
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation)+b
            zs.append(z)
            activation = self.sigmoid(z)
            activations.append(activation)
        # backward pass
        delta = self.cost_derivative(activations[-1], y) * \
            self.sigmoid_derivative(zs[-1])
        der_b[-1] = delta
        der_w[-1] = np.dot(delta, activations[-2].transpose())
        # Note that the variable l in the loop below is used a little
        # differently to the notation in Chapter 2 of the book.  Here,
        # l = 1 means the last layer of neurons, l = 2 is the
        # second-last layer, and so on.  It's a renumbering of the
        # scheme in the book, used here to take advantage of the fact
        # that Python can use negative indices in lists.
        for l in xrange(2, self.num_layers):
            z = zs[-l]
            sp = self.sigmoid_derivative(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            der_b[-l] = delta
            der_w[-l] = np.dot(delta, activations[-l-1].transpose())
        return (der_b, der_w)

    def evaluate(self, test_data):
        test_results = [(np.argmax(self.feedforward(x)), y) for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)
    #Tools (math functions etc)
    def sigmoid(self, x):
        return 1.0 / (1 + np.exp(-x))
    def cost_derivative(self, output_activations, y):
        return (output_activations-y)
    def sigmoid_derivative(self, z):
        return self.sigmoid(z)*(1-self.sigmoid(z))