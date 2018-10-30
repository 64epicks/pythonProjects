import numpy as np
#import network as nw

#arr1 = [1, 2, 3]
# arr2 = [3, 2, 1]

# print([x + y for x, y in zip(arr1, arr2)])
#print(arr1[-1])

#nn = nw.Network([3, 4, 4])
#print(nn.feedforward([1, 0, 1]))
#nn = nw.Network([784, 30, 10])

import mnist_loader
training_data, validation_data, test_data = mnist_loader.load_data_wrapper()

import network as nw
nn = nw.Network([784, 30, 10])
nn.train(training_data, 10, 10, 3.0, test_data=test_data)