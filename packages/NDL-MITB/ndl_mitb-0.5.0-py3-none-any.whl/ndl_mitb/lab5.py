import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

class HebbianPCA:
    def __init__(self, input_dim=2, learning_rate=1e-5, samples=1000, epochs=100):
        self.input_dim = input_dim
        self.lr = learning_rate
        self.samples = samples
        self.epochs = epochs
        self.weights = np.random.rand(input_dim)
        self.data = self._generate_data()
        self.centered_data = self._center_data()

    def _generate_data(self):
        x = np.random.randint(0, 100, self.samples)
        noise = np.random.normal(2, 50, x.shape)
        y = 3 * x + 2 + noise
        return np.column_stack((x, y))

    def _center_data(self):
        mean = np.mean(self.data, axis=0)
        return self.data - mean

    def _activate(self, x):
        return np.dot(self.weights, x)

    def train(self):
        for _ in range(self.epochs):
            for x in self.centered_data:
                self.weights += self.lr * self._activate(x) * x
        norm = np.linalg.norm(self.weights)
        if norm > 0:
            self.weights /= norm

    def _get_principal_component(self):
        pca = PCA(n_components=1)
        pca.fit(self.centered_data)
        return pca.components_[0]

    def visualize(self):
        self.train()
        hebbian_vector = self.weights
        pca_vector = self._get_principal_component() 
        origin = np.array([0, 0])

        plt.scatter(self.centered_data[:, 0], self.centered_data[:, 1], alpha=0.3, label="Input Data")
        plt.quiver(*origin, *hebbian_vector, color="r", scale=3, label="Hebbian Direction")
        plt.quiver(*origin, *pca_vector, color="g", scale=3, label="PCA Direction")
        plt.legend()
        plt.title("Principal Component via Hebbian Learning vs PCA")
        plt.xlabel("X1")
        plt.ylabel("X2")
        plt.grid(True)
        plt.axis('equal')
        plt.show()


if __name__ == "__main__":
    model = HebbianPCA()
    model.visualize()