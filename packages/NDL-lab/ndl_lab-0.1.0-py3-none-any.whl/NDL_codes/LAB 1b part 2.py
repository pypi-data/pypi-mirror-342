import numpy as np
from collections import Counter

class Neuron:
    def __init__(self, k): self.k = k
    def train(self, X, y): self.X, self.y = X, y
    def predict(self, X): return np.array([self._pred(x) for x in X])
    def _pred(self, x):
        idx = np.argsort([np.linalg.norm(x - t) for t in self.X])[:self.k]
        return Counter(self.y[i] for i in idx).most_common(1)[0][0]

if __name__ == "__main__":
    n = Neuron(3)
    n.train(np.array([[1,2],[2,3],[3,4],[4,5]]), np.array([0,0,1,1]))
    print(n.predict(np.array([[5,6],[0,1]])))
