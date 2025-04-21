import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.datasets import mnist
from keras.optimizers import AdaGrad, RMSprop, Adam
from keras.utils import to_categorical

class Optimizers:
    def __init__(self, optimizer, learning_rate=0.001, epochs=5, batch_size=64):
        # Store optimizer and hyperparameters
        self.optimizer = optimizer
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.batch_size = batch_size
        
        # Load and preprocess the MNIST dataset
        self.x_train, self.y_train, self.x_test, self.y_test = self.load_and_preprocess_data()
        
        # Build the model with the given optimizer
        self.model = self.build_model()

    def load_and_preprocess_data(self):
        # Load the MNIST dataset
        (x_train, y_train), (x_test, y_test) = mnist.load_data()

        # Normalize the images to the range [0, 1]
        x_train = x_train / 255.0
        x_test = x_test / 255.0

        # Convert labels to categorical (one-hot encoding)
        y_train_cat = to_categorical(y_train, 10)
        y_test_cat = to_categorical(y_test, 10)

        return x_train, y_train_cat, x_test, y_test_cat

    def build_model(self):
        # Define a simple neural network model
        model = Sequential([
            Flatten(input_shape=(28, 28)),  # Flatten the 28x28 images into a vector
            Dense(128, activation='relu'),  # First hidden layer with 128 neurons
            Dense(10, activation='softmax')  # Output layer with 10 classes
        ])
        
        # Compile the model with the given optimizer
        model.compile(optimizer=self.optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
        
        return model

    def train_and_evaluate(self):
        # Train the model
        print(f"\nTraining with {self.optimizer.__class__.__name__} optimizer:")
        self.model.fit(self.x_train, self.y_train, epochs=self.epochs, batch_size=self.batch_size, validation_data=(self.x_test, self.y_test))
        
        # Evaluate the model on test data
        loss, accuracy = self.model.evaluate(self.x_test, self.y_test)
        
        print(f"{self.optimizer.__class__.__name__} Optimizer - Loss: {loss}, Accuracy: {accuracy}")
        return loss, accuracy

# Create instances for each optimizer and train the model

# AdaGrad optimizer
adagrad_optimizer = AdaGrad(learning_rate=0.01)
adagrad_model = MNIST_Model(optimizer=adagrad_optimizer)
adagrad_model.train_and_evaluate()

# RMSProp optimizer
rmsprop_optimizer = RMSprop(learning_rate=0.001)
rmsprop_model = MNIST_Model(optimizer=rmsprop_optimizer)
rmsprop_model.train_and_evaluate()

# Adam optimizer
adam_optimizer = Adam(learning_rate=0.001)
adam_model = MNIST_Model(optimizer=adam_optimizer)
adam_model.train_and_evaluate()
