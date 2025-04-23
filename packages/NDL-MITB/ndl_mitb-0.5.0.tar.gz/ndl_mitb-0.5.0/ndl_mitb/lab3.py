import numpy as np

class PerceptronGATE:
    def __init__(self, learning_rate=0.1, epochs=10):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = np.zeros(2)  # Since we have 2 inputs
        self.bias = 0

    def activation(self, x):
        """Step activation function."""
        return 1 if x >= 0 else 0

    def predict(self, x):
        """Make a prediction."""
        z = np.dot(x, self.weights) + self.bias
        return self.activation(z)

    def train(self, X, y):
        """Train the perceptron."""
        for epoch in range(self.epochs):
            for xi, target in zip(X, y):
                prediction = self.predict(xi)
                error = target - prediction
                self.weights += self.learning_rate * error * xi
                self.bias += self.learning_rate * error

    def evaluate(self, X):
        """Evaluate on test data."""
        for x in X:
            print(f"Input: {x}, Output: {self.predict(x)}")




import numpy as np

class MLP_XOR:
    def __init__(self, lr=0.1, epochs=10000):
        self.lr = lr
        self.epochs = epochs
        self.X = np.array([[0,0],[0,1],[1,0],[1,1]])
        self.y = np.array([[0],[1],[1],[0]])
        self.w1 = np.random.rand(2,2)
        self.b1 = np.random.rand(1,2)
        self.w2 = np.random.rand(2,1)
        self.b2 = np.random.rand(1,1)

    def sigmoid(self, x): return 1 / (1 + np.exp(-x))
    def sigmoid_deriv(self, x): return x * (1 - x)

    def train(self):
        for e in range(self.epochs):
            h = self.sigmoid(np.dot(self.X, self.w1) + self.b1)
            o = self.sigmoid(np.dot(h, self.w2) + self.b2)
            error = self.y - o
            if e % 1000 == 0: print(f"Epoch {e} | Error: {np.mean(np.abs(error)):.6f}")
            d_o = error * self.sigmoid_deriv(o)
            d_h = d_o.dot(self.w2.T) * self.sigmoid_deriv(h)
            self.w2 += h.T.dot(d_o) * self.lr
            self.b2 += np.sum(d_o, axis=0, keepdims=True) * self.lr
            self.w1 += self.X.T.dot(d_h) * self.lr
            self.b1 += np.sum(d_h, axis=0, keepdims=True) * self.lr

    def predict(self):
        h = self.sigmoid(np.dot(self.X, self.w1) + self.b1)
        o = self.sigmoid(np.dot(h, self.w2) + self.b2)
        for i, x in enumerate(self.X):
            print(f"Input: {x} -> Predicted Output: {round(o[i][0])}")


def main():
    print("---- Perceptron for AND Gate ----")
    # AND Gate Inputs and Outputs
    X = np.array([[0,0], [0,1], [1,0], [1,1]])
    y_and = np.array([0, 0, 0, 1])  # AND gate output

    perceptron_and = PerceptronGATE(learning_rate=0.1, epochs=10)
    perceptron_and.train(X, y_and)

    print("\nEvaluating AND Gate:")
    perceptron_and.evaluate(X)

    print("\n---- Perceptron for OR Gate ----")
    y_or = np.array([0, 1, 1, 1])  # OR gate output

    perceptron_or = PerceptronGATE(learning_rate=0.1, epochs=10)
    perceptron_or.train(X, y_or)

    print("\nEvaluating OR Gate:")
    perceptron_or.evaluate(X)

    print("\n---- MLP for XOR Gate ----")
    mlp_xor = MLP_XOR(lr=0.1, epochs=10000)
    mlp_xor.train()
    
    print("\nEvaluating XOR Gate with MLP:")
    mlp_xor.predict()


if __name__ == "__main__":
    main()
