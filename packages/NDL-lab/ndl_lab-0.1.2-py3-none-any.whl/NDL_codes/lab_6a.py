import numpy as np 
import matplotlib.pyplot as plt 
class SelfOrganizingMap: 
    def __init__(self, input_dim, grid_size, learning_rate=0.1, radius=None, epochs=1000): 
        self.input_dim = input_dim 
        self.grid_size = grid_size 
        self.learning_rate = learning_rate 
        self.epochs = epochs 
        self.radius = radius if radius else max(grid_size) / 2 
        self.weights = np.random.rand(grid_size[0], grid_size[1], input_dim) 
    def find_bmu(self, sample): 
        distances = np.linalg.norm(self.weights - sample, axis=2) 
        return np.unravel_index(np.argmin(distances), distances.shape) 
    def update_weights(self, sample, bmu, iteration):
        for i in range(self.grid_size[0]): 
            for j in range(self.grid_size[1]): 
                dist_to_bmu = np.linalg.norm(np.array([i, j]) - np.array(bmu)) 
                if dist_to_bmu <= self.radius: 
                    influence = np.exp(-dist_to_bmu**2 / (2 * (self.radius**2))) 
                    self.weights[i, j] += self.learning_rate * influence * (sample - self.weights[i, j]) 
    def train(self, data): 
        for epoch in range(self.epochs): 
            for sample in data: 
                bmu = self.find_bmu(sample) 
                self.update_weights(sample, bmu, epoch)  
        self.learning_rate *= 0.995 
        self.radius *= 0.995 
    def visualize(self):
        plt.imshow(self.weights.reshape(self.grid_size[0], self.grid_size[1], self.input_dim)) 
        plt.title("Self-Organizing Map") 
        plt.show() 
if __name__ == "__main__": 
    data = np.random.rand(100, 3)  # 100 samples, 3 features 
    som = SelfOrganizingMap(input_dim=3, grid_size=(10, 10)) 
    som.train(data) 
    som.visualize() 