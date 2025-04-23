import numpy as np
class Neuron:
    def __init__(self, n):
        self.w = np.random.rand(n)
        self.b = np.random.rand()
    def activate(self, x):
        s = x @ self.w + self.b
        return 1 / (1 + np.exp(-s))
    def train(self, x, y, lr):
        o = self.activate(x)
        e = y - o
        self.w += lr * e * x
        self.b += lr * e
if __name__ == "__main__":
    X = np.array([[0, 0, 1],
                  [1, 1, 1],
                  [1, 0, 1],
                  [0, 1, 1]])
    y = np.array([0, 1, 1, 0])
    neuron = Neuron(3)
    for _ in range(1000):
        i = np.random.randint(len(X))
        neuron.train(X[i], y[i], .1)
    for x in X:
        print("in:", x, "out:", neuron.activate(x))