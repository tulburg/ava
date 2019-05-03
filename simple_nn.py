from numpy import exp, array, random, dot
import math
import numpy as np

class NeuralNetwork():
    def __init__(self):
        random.seed(1)
        self.synaptic_weights = 2 * random.random((3, 1)) - 1

    def __sigmoid(self, x):
        return 1 / (1 + exp(-x))

    def __sigmoid_derivative(self, x):
        return x * (1 - x)

    def __atan(self, x) :
        return math.atan(x)

    def __atan_derivative(self, x):
        return 1 / (math.pow(x, 2) + 1)

    def __soft_plus(self, x):
        return math.log(1 + exp(x))

    def __soft_plus_derivative(self, x) :
        return self.__sigmoid(x)

    def train(self, training_set_inputs, training_set_outputs, number_of_training_iterations):
        for iteration in xrange(number_of_training_iterations):
            output = self.think(training_set_inputs)
            error = training_set_outputs - output
            # v__atan_derivative = np.vectorize(self.__atan_derivative)
            # adjustment = dot(training_set_inputs.T, error * v__atan_derivative(output))
            # --------
            adjustment = dot(training_set_inputs.T, error * self.__sigmoid_derivative(output))
            # v__soft_plus_derivative = np.vectorize(self.__soft_plus_derivative)
            # adjustment = dot(training_set_inputs.T, error * v__soft_plus_derivative(output))
            self.synaptic_weights += adjustment

    def think(self, inputs):
        return self.__sigmoid(dot(inputs, self.synaptic_weights))
        # -----
        # v__atan = np.vectorize(self.__atan)
        # return v__atan(dot(inputs, self.synaptic_weights))
        # v__soft_plus = np.vectorize(self.__soft_plus)
        # return v__soft_plus(dot(inputs, self.synaptic_weights))
    def check(self, inputs):
        synaptic_weights = [[-6.00499799],[ 9.79535786], [10.19754596]]
        return self.__sigmoid(dot(inputs, synaptic_weights));



if __name__ == "__main__":
    neural_network = NeuralNetwork()

    print "Random starting synaptic weights: "
    print neural_network.synaptic_weights
    # training_set_inputs = array([[0, 0, 1], [1, 1, 1], [1, 0, 1], [0, 1, 1]])
    training_set_inputs = array([[9, 4, 1], [1, 1, 0], [1, 0, 1], [9, 1, 1]])
    training_set_outputs = array([[0, 1, 1, 0]]).T
    neural_network.train(training_set_inputs, training_set_outputs, 10000)

    print "New synaptic weights after training: "
    print neural_network.synaptic_weights

    print "Considering new situation [1, 0, 0] -> ?: "
    print neural_network.think(array([1, 0, 0]))
    print neural_network.check(array([1, 0, 0]))
