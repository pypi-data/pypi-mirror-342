import numpy as np
class Neuron:
    def __init__(self, num_inputs):
        self.weights = np.random.rand(num_inputs)
    def activate(self, inputs):
        return np.dot(inputs, self.weights)
    def learn_hebbian(self, inputs, learning_rate):
        output = self.activate(inputs)
        self.weights += learning_rate * output * inputs
if __name__ == "__main__":
    patterns = np.array([0.5,0.3,0.2])
    neuron = Neuron(num_inputs=3)
    learning_rate = 0.1
    num_epochs = 1000
    for _ in range(num_epochs):
        for p in patterns:
            neuron.learn_hebbian(p, learning_rate)
    print("Learned weights:", neuron.weights)