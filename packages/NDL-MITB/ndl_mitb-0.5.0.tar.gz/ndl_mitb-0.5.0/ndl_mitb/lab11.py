import tensorflow as tf
from keras.models import Model
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Input
from keras.optimizers import Adam
from keras.utils import to_categorical
import numpy as np
import cv2
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns

class DeepCNNOnMNIST:
    def __init__(self):
        # Load MNIST data
        self.x_train, self.y_train, self.x_test, self.y_test = self.load_data()
        
        # Preprocess Data
        self.x_train_resized, self.x_test_resized = self.preprocess_data()

        # Convert labels to categorical
        self.y_train_cat = to_categorical(self.y_train, 10)
        self.y_test_cat = to_categorical(self.y_test, 10)

    def load_data(self):
        (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
        return x_train, y_train, x_test, y_test

    def preprocess_data(self):
        # Add channel dimension for grayscale images
        x_train = np.expand_dims(self.x_train, axis=-1)
        x_test = np.expand_dims(self.x_test, axis=-1)

        # Normalize data
        x_train = x_train / 255.0
        x_test = x_test / 255.0

        # Resize images to 28x28 if necessary
        x_train_resized = np.array([cv2.resize(img, (28, 28)) for img in x_train])
        x_test_resized = np.array([cv2.resize(img, (28, 28)) for img in x_test])

        return x_train_resized, x_test_resized


    def create_lenet_model(self):
        model = tf.keras.Sequential([
            Conv2D(6, (5, 5), activation='relu', input_shape=(28, 28, 1)),
            MaxPooling2D(pool_size=(2, 2)),
            Conv2D(16, (5, 5), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Flatten(),
            Dense(120, activation='relu'),
            Dense(84, activation='relu'),
            Dense(10, activation='softmax')
        ])
        model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
        return model


    def create_alexnet_model(self):
        model = tf.keras.Sequential([
            Conv2D(96, (11, 11), strides=(4, 4), padding='valid', activation='relu', input_shape=(227, 227, 3)),
            MaxPooling2D(pool_size=(3, 3), strides=(2, 2)),
            Conv2D(256, (5, 5), padding='same', activation='relu'),
            MaxPooling2D(pool_size=(3, 3), strides=(2, 2)),
            Conv2D(384, (3, 3), padding='same', activation='relu'),
            Conv2D(384, (3, 3), padding='same', activation='relu'),
            Conv2D(256, (3, 3), padding='same', activation='relu'),
            MaxPooling2D(pool_size=(3, 3), strides=(2, 2)),
            Flatten(),
            Dense(4096, activation='relu'),
            Dense(4096, activation='relu'),
            Dense(10, activation='softmax')
        ])
        model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
        return model


    def create_vgg_model(self):
        base_model_vgg = tf.keras.applications.VGG16(weights='imagenet', include_top=False, input_shape=(32, 32, 3))
        for layer in base_model_vgg.layers:
            layer.trainable = False
        x = Flatten()(base_model_vgg.output)
        x = Dense(256, activation='relu')(x)
        x = Dense(10, activation='softmax')(x)
        vgg_model = Model(inputs=base_model_vgg.input, outputs=x)
        vgg_model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
        return vgg_model

    def create_placesnet_model(self):
        input_layer = Input(shape=(28, 28, 3))
        x = Conv2D(64, (3,3), activation='relu', padding='same')(input_layer)
        x = MaxPooling2D((2,2))(x)
        x = Conv2D(128, (3,3), activation='relu', padding='same')(x)
        x = MaxPooling2D((2,2))(x)
        x = Flatten()(x)
        x = Dense(256, activation='relu')(x)
        x = Dense(10, activation='softmax')(x)
        placesnet_model = Model(inputs=input_layer, outputs=x)
        placesnet_model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
        return placesnet_model

    def train_model(self, model, x_train, y_train, x_test, y_test, epochs=5, batch_size=64):
        model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_test, y_test))
        return model

    def plot_confusion_matrix(self, model, x_test, y_test, title):
        y_pred = np.argmax(model.predict(x_test), axis=1)
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.xlabel('Predicted')
        plt.ylabel('True')
        plt.title(f'Confusion Matrix: {title}')
        plt.show()

    def visualize_feature_maps(self, model, x_sample):
        layer_outputs = [layer.output for layer in model.layers if isinstance(layer, Conv2D)]
        activation_model = Model(inputs=model.input, outputs=layer_outputs)
        activations = activation_model.predict(np.expand_dims(x_sample, axis=0))
        for i, activation in enumerate(activations[:3]):  # Show first 3 layers
            plt.figure(figsize=(10, 5))
            for j in range(min(activation.shape[-1], 6)):  # Show first 6 filters
                plt.subplot(1, 6, j+1)
                plt.imshow(activation[0, :, :, j], cmap='viridis')
                plt.axis('off')
            plt.show()

    def run(self):
        models = {
            "LeNet": self.create_lenet_model(),
            "AlexNet": self.create_alexnet_model(),
            "VGG": self.create_vgg_model(),
            "PlacesNet": self.create_placesnet_model()
        }

        for model_name, model in models.items():
            print(f"Training {model_name} Model")
            if model_name == "VGG":
                model = self.train_model(model, self.x_train_resized, self.y_train_cat, self.x_test_resized, self.y_test_cat)
            else:
                model = self.train_model(model, self.x_train, self.y_train_cat, self.x_test, self.y_test_cat)
            
            # Evaluate and Visualize Results
            self.plot_confusion_matrix(model, self.x_test_resized if model_name == "VGG" else self.x_test, self.y_test, model_name)
            self.visualize_feature_maps(model, self.x_test_resized[0] if model_name == "VGG" else self.x_test[0])


if __name__ == "__main__":
    deep_cnn = DeepCNNOnMNIST()
    deep_cnn.run()
