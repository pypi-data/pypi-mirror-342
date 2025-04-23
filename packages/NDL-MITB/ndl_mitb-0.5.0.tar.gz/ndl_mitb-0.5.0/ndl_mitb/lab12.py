import numpy as np

class BasicRNNCell:
    def __init__(self, input_size, hidden_size, seed=None):
        """
        Initialize weights and biases for the RNN cell.
        """
        self.input_size = input_size
        self.hidden_size = hidden_size

        if seed is not None:
            np.random.seed(seed)

        self.W_x = np.random.randn(hidden_size, input_size)
        self.W_h = np.random.randn(hidden_size, hidden_size)
        self.b = np.random.randn(hidden_size, 1)

    def forward(self, x_t, h_prev):
        """
        Perform a single forward step of a basic RNN cell.

        Arguments:
        x_t -- input at time step t (shape: input_size, 1)
        h_prev -- hidden state at time step t-1 (shape: hidden_size, 1)

        Returns:
        h_t -- next hidden state (shape: hidden_size, 1)
        """
        h_t = np.tanh(np.dot(self.W_x, x_t) + np.dot(self.W_h, h_prev) + self.b)
        return h_t



import numpy as np

class SequenceRNN:
    def __init__(self, input_size, hidden_size, output_size, seed=None):
        """
        Initializes weights and biases for sequence-level RNN.
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        if seed is not None:
            np.random.seed(seed)

        # Initialize weights
        self.W_x = np.random.randn(hidden_size, input_size)
        self.W_h = np.random.randn(hidden_size, hidden_size)
        self.b_h = np.random.randn(hidden_size, 1)

        self.W_y = np.random.randn(output_size, hidden_size)
        self.b_y = np.random.randn(output_size, 1)

    def forward(self, X, h0):
        """
        Forward propagation for the entire sequence.

        Arguments:
        X -- input data for every time-step (shape: time_steps, input_size)
        h0 -- initial hidden state (shape: hidden_size, 1)

        Returns:
        h -- hidden states for every time-step (shape: time_steps, hidden_size, 1)
        y -- outputs for every time-step (shape: time_steps, output_size, 1)
        """
        time_steps = X.shape[0]
        h = np.zeros((time_steps, self.hidden_size, 1))
        y = np.zeros((time_steps, self.output_size, 1))

        h_prev = h0

        for t in range(time_steps):
            x_t = X[t].reshape(-1, 1)
            h_t = np.tanh(np.dot(self.W_x, x_t) + np.dot(self.W_h, h_prev) + self.b_h)
            y_t = np.dot(self.W_y, h_t) + self.b_y

            h[t] = h_t
            y[t] = y_t
            h_prev = h_t

        return h, y
    






class LSTMCell:
    def __init__(self, input_size, hidden_size, seed=None):
        """
        Initialize the LSTM cell with random weights and biases.
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.concat_size = input_size + hidden_size

        if seed is not None:
            np.random.seed(seed)

        # Initialize weights and biases
        self.parameters = {
            "W_f": np.random.randn(hidden_size, self.concat_size),
            "b_f": np.random.randn(hidden_size, 1),
            "W_i": np.random.randn(hidden_size, self.concat_size),
            "b_i": np.random.randn(hidden_size, 1),
            "W_c": np.random.randn(hidden_size, self.concat_size),
            "b_c": np.random.randn(hidden_size, 1),
            "W_o": np.random.randn(hidden_size, self.concat_size),
            "b_o": np.random.randn(hidden_size, 1),
        }
    
    def sigmoid(self , x):
        return 1 / (1 + np.exp(-x))

    def forward(self, x_t, h_prev, c_prev):
        """
        Perform one forward pass of the LSTM cell.

        Arguments:
        x_t -- Input at time t (input_size, 1)
        h_prev -- Previous hidden state (hidden_size, 1)
        c_prev -- Previous cell state (hidden_size, 1)

        Returns:
        h_next -- Next hidden state (hidden_size, 1)
        c_next -- Next cell state (hidden_size, 1)
        """
        W_f = self.parameters["W_f"]
        b_f = self.parameters["b_f"]
        W_i = self.parameters["W_i"]
        b_i = self.parameters["b_i"]
        W_c = self.parameters["W_c"]
        b_c = self.parameters["b_c"]
        W_o = self.parameters["W_o"]
        b_o = self.parameters["b_o"]

        # Concatenate h_prev and x_t
        concat = np.vstack((h_prev, x_t))

        # Forget gate
        f_t = self.sigmoid(np.dot(W_f, concat) + b_f)

        # Input gate
        i_t = self.sigmoid(np.dot(W_i, concat) + b_i)

        # Candidate memory
        c_tilde = np.tanh(np.dot(W_c, concat) + b_c)

        # Update cell state
        c_next = f_t * c_prev + i_t * c_tilde

        # Output gate
        o_t = self.sigmoid(np.dot(W_o, concat) + b_o)

        # Next hidden state
        h_next = o_t * np.tanh(c_next)

        return h_next, c_next



import numpy as np

def main():
    input_size = 4
    hidden_size = 5
    time_steps = 6
    np.random.seed(42)
    X = np.random.randn(time_steps, input_size)

    print("\n-- Basic RNN --")
    rnn = BasicRNNCell(input_size, hidden_size)
    h = np.zeros((hidden_size, 1))
    for t in range(time_steps):
        x_t = X[t].reshape(-1, 1)
        h = rnn.forward(x_t, h)
        print(f"Step {t}: h =\n{h}\n")

    print("\n-- LSTM --")
    lstm = LSTMCell(input_size, hidden_size)
    h = np.zeros((hidden_size, 1))
    c = np.zeros((hidden_size, 1))
    for t in range(time_steps):
        x_t = X[t].reshape(-1, 1)
        h, c = lstm.forward(x_t, h, c)
        print(f"Step {t}: h =\n{h}\n")

main()