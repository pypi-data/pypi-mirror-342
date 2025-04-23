import numpy as np
import matplotlib.pyplot as plt

class ActivationFunctions:
    def __init__(self):
        """Initialize the activation functions class."""
        pass
    
    def binary_step(self, x):
        """Binary step function that returns 0 for negative values and 1 for positive values."""
        return np.where(x >= 0, 1, 0)
    
    def relu(self, x):
        """Rectified Linear Unit activation function."""
        return np.maximum(0, x)
    
    def leaky_relu(self, x, alpha=0.01):
        """Leaky ReLU that allows small negative values to pass through."""
        return np.where(x > 0, x, alpha * x)
    
    def sigmoid(self, x):
        """Sigmoid activation function that squashes values between 0 and 1."""
        return 1 / (1 + np.exp(-x))
    
    def tanh(self, x):
        """Hyperbolic tangent activation function."""
        return np.tanh(x)
    
    def softmax(self, x):
        """Softmax function that converts values to probabilities that sum to 1."""
        exp_x = np.exp(x - np.max(x))
        return exp_x / exp_x.sum()
    
    def plot_function(self, function, x_range=(-10, 10), num_points=100, title=None):
        """Plot the activation function for visualization."""
        x = np.linspace(x_range[0], x_range[1], num_points)
        y = function(x)
        
        plt.figure(figsize=(8, 6))
        plt.plot(x, y)
        plt.grid(True)
        plt.title(title if title else function.__name__)
        plt.xlabel("Input")
        plt.ylabel("Output")
        plt.show()
    
    def plot_all(self):
        """Plot all activation functions for comparison."""
        x = np.linspace(-10, 10, 100)
        
        plt.figure(figsize=(15, 10))
        
        plt.subplot(3, 2, 1)
        plt.plot(x, self.relu(x))
        plt.title('ReLU')
        plt.grid(True)
        
        plt.subplot(3, 2, 2)
        plt.plot(x, self.binary_step(x))
        plt.title('Binary Step')
        plt.grid(True)
        
        plt.subplot(3, 2, 3)
        plt.plot(x, self.sigmoid(x))
        plt.title('Sigmoid')
        plt.grid(True)
        
        plt.subplot(3, 2, 4)
        plt.plot(x, self.leaky_relu(x))
        plt.title('Leaky ReLU')
        plt.grid(True)
        
        plt.subplot(3, 2, 5)
        plt.plot(x, self.tanh(x))
        plt.title('Tanh')
        plt.grid(True)
        
        plt.tight_layout()
        plt.show()



class SimpleNeuron:
    def __init__(self, num_inputs):
        """Initialize the neuron with random weights and bias."""
        self.num_inputs = num_inputs
        self.weights = np.random.rand(num_inputs)
        self.bias = np.random.rand()

    def sigmoid(self, x):
        """Sigmoid activation function."""
        return 1 / (1 + np.exp(-x))

    def activate(self, inputs):
        """Compute the neuron's output for given inputs."""
        weighted_sum = np.dot(inputs, self.weights) + self.bias
        return self.sigmoid(weighted_sum)

    def train(self, X_train, y_train, learning_rate=0.1, num_iterations=10000):
        """Train the neuron using error correction learning."""
        for _ in range(num_iterations):
            idx = np.random.randint(len(X_train))
            inputs = X_train[idx]
            target_output = y_train[idx]
            actual_output = self.activate(inputs)
            error = target_output - actual_output
            self.weights += learning_rate * error * inputs
            self.bias += learning_rate * error

    def predict(self, inputs):
        """Predict output for given inputs."""
        return self.activate(inputs)

    def evaluate(self, test_data):
        """Print predictions for test dataset."""
        for inputs in test_data:
            output = self.predict(inputs)
            print("Input:", inputs, "Output:", output)





import numpy as np
from collections import Counter

class MemoryNeuron:
    def __init__(self, k): 
        self.k = k 

    def train(self, X, y): 
        self.X_train, self.y_train = X, y  

    def predict(self, X):  
        return np.array([self._predict(x) for x in X])  

    def _predict(self, x):  
        distances = np.linalg.norm(self.X_train - x, axis=1)  
        k_nearest = self.y_train[np.argsort(distances)[:self.k]]  
        return Counter(k_nearest).most_common(1)[0][0]  
    

def main():
    # --- Part 1: Activation Functions ---
    print("Plotting Activation Functions...")
    activations = ActivationFunctions()
    activations.plot_all()

    # --- Part 2: Simple Neuron ---
    print("\nTraining Simple Neuron...")
    X_train = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y_train = np.array([0, 1, 1, 0])  # XOR (not linearly separable, but still for demo)

    neuron = SimpleNeuron(num_inputs=2)
    neuron.train(X_train, y_train, learning_rate=0.1, num_iterations=10000)

    print("\nSimple Neuron Predictions:")
    neuron.evaluate(X_train)

    # --- Part 3: Memory Neuron (k-NN) ---
    print("\nTesting Memory Neuron (k-NN)...")
    mem_neuron = MemoryNeuron(k=3)
    mem_neuron.train(X_train, y_train)

    test_data = np.array([[0, 0], [1, 1], [0.2, 0.8], [0.8, 0.2]])
    predictions = mem_neuron.predict(test_data)

    for i, x in enumerate(test_data):
        print(f"Input: {x}, Predicted Label: {predictions[i]}")


if __name__ == '__main__':
    main()

    



