import numpy as np

class HebbianNeuron:
    def __init__(self, num_inputs):
        """Initialize weights and bias randomly."""
        self.num_inputs = num_inputs
        self.weights = np.random.rand(num_inputs)
        self.bias = np.random.rand()

    def activation(self, x):
        """Simple step function (binary output)."""
        return 1 if x >= 0 else 0

    def output(self, inputs):
        """Compute the raw output and apply activation."""
        raw_output = np.dot(inputs, self.weights) + self.bias
        return self.activation(raw_output)

    def train(self, X_train, learning_rate=0.01, num_iterations=100):
        """Train the neuron using Hebbian learning."""
        for _ in range(num_iterations):
            for inputs in X_train:
                output = self.output(inputs)
                self.weights += learning_rate * inputs * output
                self.bias += learning_rate * output

    def predict(self, inputs):
        """Predict output for a given input."""
        return self.output(inputs)

    def evaluate(self, test_data):
        """Print predictions for test dataset."""
        for inputs in test_data:
            result = self.predict(inputs)
            print("Input:", inputs, "Predicted Output:", result)

def main():
    # --- Hebbian Learning Neuron Example ---
    print("Training Hebbian Neuron...")

    # Training data (AND logic gate)
    X_train = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])

    # Initialize Hebbian neuron with 2 inputs
    neuron = HebbianNeuron(num_inputs=2)

    # Train the neuron using Hebbian learning
    neuron.train(X_train, learning_rate=0.1, num_iterations=10)

    # Test data (same as training data in this example)
    print("\nEvaluating Hebbian Neuron:")
    neuron.evaluate(X_train)
    print(neuron.weights, neuron.bias)


if __name__ == '__main__':
    main()
