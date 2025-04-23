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

    def update_weights(self, sample, bmu):
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                dist_to_bmu = np.linalg.norm(np.array([i, j]) - np.array(bmu))
                if dist_to_bmu <= self.radius:
                    influence = np.exp(-dist_to_bmu ** 2 / (2 * (self.radius ** 2)))
                    self.weights[i, j] += self.learning_rate * influence * (sample - self.weights[i, j])

    def train(self, data):
        for epoch in range(self.epochs):
            for sample in data:
                bmu = self.find_bmu(sample)
                self.update_weights(sample, bmu)

            # Decay learning rate and radius
            self.learning_rate *= 0.995
            self.radius *= 0.995

    def visualize(self):
        plt.imshow(self.weights.reshape(self.grid_size[0], self.grid_size[1], self.input_dim))
        plt.title("Self-Organizing Map (SOM)")
        plt.axis('off')
        plt.show()


class RecurrentNeuralNetwork:
    def __init__(self, input_dim, hidden_dim, output_dim, learning_rate=0.001, time_steps=5):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.learning_rate = learning_rate
        self.time_steps = time_steps

        # Weight initialization
        self.Wxh = np.random.randn(hidden_dim, input_dim) * 0.01
        self.Whh = np.random.randn(hidden_dim, hidden_dim) * 0.01
        self.Why = np.random.randn(output_dim, hidden_dim) * 0.01
        self.bh = np.zeros((hidden_dim, 1))
        self.by = np.zeros((output_dim, 1))

    def forward(self, inputs):
        h = np.zeros((self.hidden_dim, 1))
        self.h_states = {-1: h}
        self.outputs = {}

        for t in range(self.time_steps):
            h = np.tanh(np.dot(self.Wxh, inputs[t]) + np.dot(self.Whh, self.h_states[t - 1]) + self.bh)
            y = np.dot(self.Why, h) + self.by
            self.h_states[t] = h
            self.outputs[t] = y

        return self.outputs

    def backward(self, inputs, targets):
        dWxh, dWhh, dWhy = np.zeros_like(self.Wxh), np.zeros_like(self.Whh), np.zeros_like(self.Why)
        dbh, dby = np.zeros_like(self.bh), np.zeros_like(self.by)
        dh_next = np.zeros((self.hidden_dim, 1))

        for t in reversed(range(self.time_steps)):
            dy = self.outputs[t] - targets[t]
            dWhy += np.dot(dy, self.h_states[t].T)
            dby += dy

            dh = np.dot(self.Why.T, dy) + dh_next
            dh_raw = (1 - self.h_states[t] ** 2) * dh
            dbh += dh_raw
            dWxh += np.dot(dh_raw, inputs[t].T)
            dWhh += np.dot(dh_raw, self.h_states[t - 1].T)
            dh_next = np.dot(self.Whh.T, dh_raw)

        # Gradient clipping
        for dparam in [dWxh, dWhh, dWhy, dbh, dby]:
            np.clip(dparam, -5, 5, out=dparam)

        # Parameter update
        for param, dparam in zip([self.Wxh, self.Whh, self.Why, self.bh, self.by],
                                 [dWxh, dWhh, dWhy, dbh, dby]):
            param -= self.learning_rate * dparam

    def train(self, data, labels, epochs=100):
        for epoch in range(epochs):
            loss = 0
            for inputs, targets in zip(data, labels):
                outputs = self.forward(inputs)
                self.backward(inputs, targets)
                loss += np.sum((outputs[self.time_steps - 1] - targets[self.time_steps - 1]) ** 2) / 2

            
            print(f"Epoch {epoch}, Loss: {loss:.4f}")




print("Training SOM...")
data = np.random.rand(100, 3)  # RGB data
som = SelfOrganizingMap(input_dim=3, grid_size=(10, 10))
som.train(data)
som.visualize()


print("\nTraining RNN...")
seq_len = 5
input_dim = 3
output_dim = 1
data = [[np.random.rand(input_dim, 1) for _ in range(seq_len)] for _ in range(50)]
labels = [[np.array([[1.0]]) for _ in range(seq_len)] for _ in range(50)]

rnn = RecurrentNeuralNetwork(input_dim=3, hidden_dim=8, output_dim=1, time_steps=5)
rnn.train(data, labels, epochs=50)

