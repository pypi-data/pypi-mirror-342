import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from keras.datasets import mnist
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

class MNIST_CNN:
    def __init__(self, epochs=10, batch_size=32):
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = self.build_model()
        self.history = None

    def load_and_preprocess_data(self):
        # Load the MNIST dataset
        (X_train, y_train), (X_test, y_test) = mnist.load_data()

        # Pre-process the data
        X_train = X_train.astype(np.float32) / 255.0
        X_test = X_test.astype(np.float32) / 255.0

        # Reshape the data to add a channel dimension
        X_train = np.expand_dims(X_train, axis=-1)
        X_test = np.expand_dims(X_test, axis=-1)

        # One-hot encode the labels
        y_train = to_categorical(y_train, num_classes=10)
        y_test = to_categorical(y_test, num_classes=10)

        return X_train, y_train, X_test, y_test

    def build_model(self):
        model = Sequential()

        # First convolutional layer with 32 filters of size 3x3, followed by max pooling
        model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        # Second convolutional layer with 64 filters of size 3x3, followed by max pooling
        model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        # Flatten the 2D output into a 1D vector
        model.add(Flatten())

        # Fully connected layer with 128 units
        model.add(Dense(128, activation='relu'))

        # Output layer with 10 units (one for each class) using softmax activation
        model.add(Dense(10, activation='softmax'))

        # Compile the model
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        return model

    def train(self, X_train, y_train, X_test, y_test):
        # Train the model
        self.history = self.model.fit(X_train, y_train, epochs=self.epochs, batch_size=self.batch_size, validation_data=(X_test, y_test))

    def evaluate(self, X_test, y_test):
        # Evaluate the model
        loss, accuracy = self.model.evaluate(X_test, y_test)
        print("Loss: ", loss)
        print("Accuracy: ", accuracy)

    def plot_accuracy(self):
        # Extract the accuracy history
        acc = self.history.history['accuracy']
        val_acc = self.history.history['val_accuracy']

        # Plot the accuracy history
        plt.plot(acc)
        plt.plot(val_acc)
        plt.title('Model Accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Test'], loc='upper left')
        plt.show()


if __name__ == "__main__":
    cnn = MNIST_CNN(epochs=5, batch_size=64)

    X_train, y_train, X_test, y_test = cnn.load_and_preprocess_data()
    cnn.train(X_train, y_train, X_test, y_test)
    cnn.evaluate(X_test, y_test)
    cnn.plot_accuracy()
