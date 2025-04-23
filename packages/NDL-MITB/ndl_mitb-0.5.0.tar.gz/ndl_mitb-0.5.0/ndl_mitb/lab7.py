import numpy as np

class HopfieldNetwork:
    def __init__(self, patterns=None):
        """
        Initialize the Hopfield Network. If patterns are provided, the network will be trained immediately.
        """
        self.weight_matrix = None
        if patterns is not None:
            self.train(patterns)

    def train(self, patterns):
        """
        Train the Hopfield network using the Hebbian learning rule.
        :param patterns: A list of binary patterns to store in the network.
        """
        num_neurons = len(patterns[0])
        self.weight_matrix = np.zeros((num_neurons, num_neurons))

        # Apply the Hebbian learning rule
        for pattern in patterns:
            pattern = np.array(pattern).reshape(-1, 1)  # Convert pattern to column vector
            self.weight_matrix += pattern @ pattern.T

        np.fill_diagonal(self.weight_matrix, 0)  # No self-connections

    def recall(self, input_pattern, max_iterations=10):
        """
        Recall a stored pattern using a noisy input pattern.
        :param input_pattern: The input pattern (can be noisy).
        :param max_iterations: The number of iterations to run the recall process.
        :return: The recalled pattern.
        """
        output_pattern = np.array(input_pattern)

        for _ in range(max_iterations):
            for i in range(len(output_pattern)):
                net_input = np.dot(self.weight_matrix[i], output_pattern)
                output_pattern[i] = 1 if net_input >= 0 else -1

        return output_pattern



# Binary to bipolar conversion
def to_bipolar(p): return [1 if x == 1 else -1 for x in p]
def to_binary(p): return [1 if x > 0 else 0 for x in p]

# Training data
patterns = [to_bipolar([1, 0, 1, 0]), to_bipolar([0, 1, 0, 1])]

# Initialize and train
net = HopfieldNetwork()
net.train(patterns)

# Noisy input
input_pattern = to_bipolar([1, 1, 1, 0])
output_pattern = net.recall(np.array(input_pattern))

print("Input:  ", to_binary(input_pattern))
print("Output: ", to_binary(output_pattern))
