
def dl():
    '''
class McCullochPittsNeuron:
    def __init__(self, weights, threshold):
        self.weights = weights
        self.threshold = threshold

    def activate(self, inputs):
        weighted_sum = sum(x * w for x, w in zip(inputs, self.weights))
        return weighted_sum >= self.threshold

if __name__ == "__main__":
    # AND Gate
    and_weights = [1, 1]
    and_threshold = 2
    and_neuron = McCullochPittsNeuron(and_weights, and_threshold)

    # OR Gate
    or_weights = [1, 1]
    or_threshold = 1
    or_neuron = McCullochPittsNeuron(or_weights, or_threshold)

    # NOT Gate
    not_weights = [-1]
    not_threshold = 0
    not_neuron = McCullochPittsNeuron(not_weights, not_threshold)

    # Test Inputs
    inputs = [
        [0, 0],  # Input 1
        [0, 1],  # Input 2
        [1, 0],  # Input 3
        [1, 1]   # Input 4
    ]

    print("AND Gate:")
    for input in inputs:
        output = and_neuron.activate(input)
        print(f"Input: {input}, Output: {output}")

    print("\nOR Gate:")
    for input in inputs:
        output = or_neuron.activate(input)
        print(f"Input: {input}, Output: {output}")

    print("\nNOT Gate:")
    single_inputs = [0, 1]
    for input in single_inputs:
        output = not_neuron.activate([input])
        print(f"Input: {input}, Output: {output}")

class McCullochPittsNeuron:
    def __init__(self, weights, threshold):
        self.weights = weights
        self.threshold = threshold

    def activate(self, inputs):
        weighted_sum = sum(x * w for x, w in zip(inputs, self.weights))
        return weighted_sum >= self.threshold

if __name__ == "__main__":
    # AND Gate
    and_weights = [1, 1]
    and_threshold = 2
    and_neuron = McCullochPittsNeuron(and_weights, and_threshold)

    # OR Gate
    or_weights = [1, 1]
    or_threshold = 1
    or_neuron = McCullochPittsNeuron(or_weights, or_threshold)

    # NOT Gate (can be implemented with a single input)
    not_weights = [-1]  # Invert the input
    not_threshold = 0
    not_neuron = McCullochPittsNeuron(not_weights, not_threshold)

    # Test Inputs
    inputs = [
        [0, 0],  # Input 1
        [0, 1],  # Input 2
        [1, 0],  # Input 3
        [1, 1]   # Input 4
    ]

    print("AND Gate:")
    print("| Input 1 | Input 2 | Output |")
    print("|---|---|---|")
    for input in inputs:
        output = and_neuron.activate(input)
        print(f"| {input[0]} | {input[1]} | {output} |")

    print("\nOR Gate:")
    print("| Input 1 | Input 2 | Output |")
    print("|---|---|---|")
    for input in inputs:
        output = or_neuron.activate(input)
        print(f"| {input[0]} | {input[1]} | {output} |")

    print("\nNOT Gate:")
    print("| Input | Output |")
    print("|---|---|")
    single_inputs = [0, 1]  # Test inputs for NOT gate
    for input in single_inputs:
        output = not_neuron.activate([input])  # Pass a single input in a list
        print(f"| {input} | {output} |")

"""# Expt2 (Perceptron Algorithm)"""

import numpy as np

class Perceptron:
    def __init__(self, input_size, lr=0.1, epochs=100):
        self.weights = np.zeros(input_size + 1)
        self.lr, self.epochs = lr, epochs

    def activation(self, x):
        return 1 if x >= 0 else 0

    def predict(self, inputs):
        return self.activation(np.dot(inputs, self.weights[1:]) + self.weights[0])

    def train(self, X, y):
        for _ in range(self.epochs):
            for inputs, label in zip(X, y):
                error = label - self.predict(inputs)
                self.weights[1:] += self.lr * error * inputs
                self.weights[0] += self.lr * error

# AND, OR, NOT Gates
training_data = {
    "AND": (np.array([[0, 0], [0, 1], [1, 0], [1, 1]]), np.array([0, 0, 0, 1])),
    "OR": (np.array([[0, 0], [0, 1], [1, 0], [1, 1]]), np.array([0, 1, 1, 1])),
    "NOT": (np.array([[0], [1]]), np.array([1, 0]))
}

for gate, (X, y) in training_data.items():
    p = Perceptron(input_size=X.shape[1])
    p.train(X, y)
    print(f"{gate} Gate:")
    for inputs in X:
        print(f"{inputs} -> {p.predict(inputs)}")

class MLP:
    def __init__(self, input_size, hidden_size, output_size, lr=0.1, epochs=1000):
        self.weights = [np.random.rand(input_size, hidden_size), np.random.rand(hidden_size, output_size)]
        self.biases = [np.random.rand(hidden_size), np.random.rand(output_size)]
        self.lr, self.epochs = lr, epochs

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def train(self, X, y):
        for _ in range(self.epochs):
            for inputs, label in zip(X, y):
                # Forward pass
                hidden = self.sigmoid(np.dot(inputs, self.weights[0]) + self.biases[0])
                output = self.sigmoid(np.dot(hidden, self.weights[1]) + self.biases[1])
                # Backward pass
                error = label - output
                d_output = error * output * (1 - output)
                d_hidden = d_output.dot(self.weights[1].T) * hidden * (1 - hidden)
                # Update weights and biases
                self.weights[1] += hidden.reshape(-1, 1).dot(d_output.reshape(1, -1)) * self.lr
                self.weights[0] += inputs.reshape(-1, 1).dot(d_hidden.reshape(1, -1)) * self.lr
                self.biases[1] += d_output * self.lr
                self.biases[0] += d_hidden * self.lr

    def predict(self, inputs):
        hidden = self.sigmoid(np.dot(inputs, self.weights[0]) + self.biases[0])
        output = self.sigmoid(np.dot(hidden, self.weights[1]) + self.biases[1])
        return 1 if output >= 0.5 else 0

# XOR Gate
X, y = np.array([[0, 0], [0, 1], [1, 0], [1, 1]]), np.array([0, 1, 1, 0])
mlp = MLP(input_size=2, hidden_size=2, output_size=1)
mlp.train(X, y)
print("XOR Gate:")
for inputs in X:
    print(f"{inputs} -> {mlp.predict(inputs)}")

import numpy as np

class Perceptron:
    def __init__(self, input_size, learning_rate=0.01, epochs=100):
        self.weights = np.zeros(input_size + 1)  # +1 for the bias
        self.lr = learning_rate
        self.epochs = epochs

    def predict(self, inputs):
        return 1 if np.dot(inputs, self.weights[1:]) + self.weights[0] > 0 else 0

    def train(self, X, y):
        for _ in range(self.epochs):
            for inputs, label in zip(X, y):
                prediction = self.predict(inputs)
                self.weights[1:] += self.lr * (label - prediction) * inputs
                self.weights[0] += self.lr * (label - prediction)

    def accuracy(self, X, y):
        return np.mean([self.predict(x) == l for x, l in zip(X, y)])


class MLP:
    def __init__(self, input_size, hidden_size, output_size, lr=0.01, epochs=50000):
        self.w1 = np.random.randn(input_size + 1, hidden_size) * 0.1  # +1 for bias
        self.w2 = np.random.randn(hidden_size + 1, output_size) * 0.1  # +1 for bias
        self.lr = lr
        self.epochs = epochs

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def forward(self, x):
        x = np.insert(x, 0, 1)
        a1 = self.sigmoid(np.dot(x, self.w1))
        a1 = np.insert(a1, 0, 1)
        a2 = self.sigmoid(np.dot(a1, self.w2))
        return a1, a2

    def backward(self, x, a1, a2, t):
        delta2 = (a2 - t) * a2 * (1 - a2)
        delta1 = np.dot(delta2, self.w2[1:].T) * a1[1:] * (1 - a1[1:])
        self.w2 -= self.lr * np.outer(a1, delta2)
        x = np.insert(x, 0, 1)
        self.w1 -= self.lr * np.outer(x, delta1)

    def train(self, X, y):
        for _ in range(self.epochs):
            for x, t in zip(X, y):
                a1, a2 = self.forward(x)
                self.backward(x, a1, a2, t)

    def predict(self, X):
        return np.array([1 if self.forward(x)[1] > 0.5 else 0 for x in X])

# AND gate
X_and = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_and = np.array([0, 0, 0, 1])
p_and = Perceptron(2)
p_and.train(X_and, y_and)
print("AND:", [p_and.predict(x) for x in X_and])

# OR gate
X_or = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_or = np.array([0, 1, 1, 1])
p_or = Perceptron(2)
p_or.train(X_or, y_or)
print("OR:", [p_or.predict(x) for x in X_or])

# XOR gate
X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_xor = np.array([0, 1, 1, 0])
mlp_xor = MLP(2, 4, 1)  # 2 inputs, 4 hidden, 1 output
mlp_xor.train(X_xor, y_xor)
print("XOR:", mlp_xor.predict(X_xor))

"""# Expt 3 (Implement a basic feedforward neural network using a deep learning framework of your choice.)"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

# Load the Iris dataset
iris = load_iris()
X = iris.data  # Features (4)
y = iris.target  # Labels (3 classes)

# One-hot encode the target labels
encoder = OneHotEncoder(sparse_output=False)
y = encoder.fit_transform(y.reshape(-1, 1))

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build the model
model = Sequential([
    Dense(8, activation='relu', input_shape=(4,)),  # Input layer (4 features) and a hidden layer with 8 neurons
    Dense(3, activation='softmax')  # Output layer (3 classes) with softmax activation
])

# Compile the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=50)

# Evaluate the model on the test set
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"Test accuracy: {test_acc}")

"""# Expt 4 (Design and implement a fully connected deep neural network with at least 2 hidden layers for a classification application.)"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

# Load the Iris dataset
iris = load_iris()
X = iris.data  # Features (4)
y = iris.target  # Labels (3 classes)

# One-hot encode the target labels
encoder = OneHotEncoder(sparse_output=False)
y = encoder.fit_transform(y.reshape(-1, 1))

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build the model
model = Sequential([
    Dense(16, activation='relu', input_shape=(4,)),
    Dense(32, activation='relu'),
    Dense(16, activation='relu'),
    Dense(3, activation='softmax')  # Output layer (3 classes) with softmax activation
])

# Compile the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=50)

# Evaluate the model on the test set
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"Test accuracy: {test_acc}")

"""# Expt 5 (Design the architecture and implement the autoencoder model for Image Compression.)

_________________________________________________________
"""

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D

# Load CIFAR-10 dataset
(x_train, _), (x_test, _) = cifar10.load_data()

# Normalize the images to the range [0, 1]
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

# Define the size of the encoded representations
encoding_dim = 32

# Input placeholder
input_img = Input(shape=(32, 32, 3))

# Encoder
x = Conv2D(32, (3, 3), activation='relu', padding='same')(input_img)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
x = MaxPooling2D((2, 2), padding='same')(x)
encoded = Conv2D(encoding_dim, (3, 3), activation='relu', padding='same')(x)

# Decoder
x = Conv2D(64, (3, 3), activation='relu', padding='same')(encoded)
x = UpSampling2D((2, 2))(x)
x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)
decoded = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)

# Autoencoder model
autoencoder = Model(input_img, decoded)
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

# Train the autoencoder
autoencoder.fit(x_train, x_train,
                epochs=50,
                batch_size=256,
                shuffle=True,
                validation_data=(x_test, x_test))


# Encode and decode some images from the test set
decoded_imgs = autoencoder.predict(x_test)

# Plot original and reconstructed images
n = 10
plt.figure(figsize=(20, 4))
for i in range(n):
    # Display original
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(x_test[i])
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # Display reconstruction
    ax = plt.subplot(2, n, i + 1 + n)
    plt.imshow(decoded_imgs[i])
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.show()

"""# Expt 6 (Design the architecture and implement the autoencoder model for Image denoising)"""

!pip install tensorflow-datasets

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D


# Load STL-10 dataset
def preprocess(data):
    image = data['image']
    image = tf.cast(image, tf.float32) / 255.0
    return image

# Load the dataset
dataset, metadata = tfds.load('stl10', split='train', with_info=True, as_supervised=False)
dataset = dataset.map(preprocess)

# Convert to numpy arrays
x_train = np.array([example.numpy() for example in dataset])

# Add noise to the images
noise_factor = 0.2
x_train_noisy = x_train + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=x_train.shape)
x_train_noisy = np.clip(x_train_noisy, 0., 1.)


# Input placeholder
input_img = Input(shape=(96, 96, 3))

# Encoder
x = Conv2D(32, (3, 3), activation='relu', padding='same')(input_img)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
encoded = MaxPooling2D((2, 2), padding='same')(x)

# Decoder
x = Conv2D(64, (3, 3), activation='relu', padding='same')(encoded)
x = UpSampling2D((2, 2))(x)
x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)
decoded = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)

# Autoencoder model
autoencoder = Model(input_img, decoded)
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')


# Train the autoencoder
autoencoder.fit(x_train_noisy, x_train,
                epochs=50,
                batch_size=256,
                shuffle=True)


# Encode and decode some images from the test set
decoded_imgs = autoencoder.predict(x_train_noisy)

# Plot noisy and denoised images
n = 10
plt.figure(figsize=(20, 6))
for i in range(n):
    # Display noisy
    ax = plt.subplot(3, n, i + 1)
    plt.imshow(x_train_noisy[i])
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # Display original
    ax = plt.subplot(3, n, i + 1 + n)
    plt.imshow(x_train[i])
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # Display reconstruction
    ax = plt.subplot(3, n, i + 1 + 2*n)
    plt.imshow(decoded_imgs[i])
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.show()

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

# Define the autoencoder architecture
class Autoencoder(nn.Module):
    def __init__(self, latent_dim=32):  # Adjust latent_dim as needed
        super(Autoencoder, self).__init__()
        # Encoder
        self.encoder = nn.Sequential(
            nn.Linear(28 * 28, 512),  # Adjust input size if needed
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, latent_dim)  # Adjust latent_dim as needed
        )
        # Decoder
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 256),  # Adjust latent_dim as needed
            nn.ReLU(),
            nn.Linear(256, 512),
            nn.ReLU(),
            nn.Linear(512, 28 * 28),  # Adjust output size if needed
            nn.Tanh()  # Output should be in the range [-1, 1]
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

# Load and preprocess the Fashion-MNIST dataset
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])

train_dataset = datasets.FashionMNIST('./data', train=True, download=True, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

test_dataset = datasets.FashionMNIST('./data', train=False, download=True, transform=transform)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

# Initialize the autoencoder, loss function, and optimizer
model = Autoencoder()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

# Training loop
num_epochs = 100  # Adjust as needed
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

for epoch in range(num_epochs):
    for data in train_loader:
        img, _ = data
        img = img.view(img.size(0), -1).to(device)  # Flatten the images
        optimizer.zero_grad()
        output = model(img)
        loss = criterion(output, img)
        loss.backward()
        optimizer.step()
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# Test the model and visualize results
with torch.no_grad():
    images, labels = next(iter(test_loader))
    images = images.view(images.size(0), -1).to(device)  # Flatten the images
    outputs = model(images)

    # Class names for Fashion-MNIST
    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Shirt', 'Dress', 'Coat',
                   'Sandal', 'Sneaker', 'Bag', 'Ankle boot']

    # Visualize original and reconstructed images
    fig, axes = plt.subplots(2, 10, figsize=(15, 5))
    for i in range(10):
        axes[0, i].imshow(images[i].cpu().view(28, 28).numpy(), cmap='gray')
        axes[0, i].set_title(f'Og - {class_names[labels[i]]}')
        axes[0, i].axis('off')
        axes[1, i].imshow(outputs[i].cpu().view(28, 28).numpy(), cmap='gray')
        axes[1, i].set_title('Recons')
        axes[1, i].axis('off')
plt.show()

"""# Expt 7: Develop an RNN-based model for sentiment analysis and apply it to a text dataset."""

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SimpleRNN, Dense, Dropout
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

# Step 1: Load the IMDB dataset (train/test split)
max_words = 10000  # Use the top 10,000 most frequent words
max_len = 100  # Maximum sequence length (reviews will be truncated or padded to this length)

# Load the data
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=max_words)

# Step 2: Preprocess the data
# Pad sequences to ensure uniform input size
x_train = pad_sequences(x_train, maxlen=max_len)
x_test = pad_sequences(x_test, maxlen=max_len)

# Convert labels to categorical (binary in this case: 0 or 1)
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# Step 3: Build the RNN-based model
model = Sequential()

# Embedding layer: turns positive integers into dense vectors of fixed size
model.add(Embedding(input_dim=max_words, output_dim=128, input_length=max_len))

# Simple RNN layer
model.add(SimpleRNN(128, activation='relu'))

# Dropout for regularization
model.add(Dropout(0.5))

# Fully connected layer with one unit (for binary classification)
model.add(Dense(2, activation='softmax'))  # 2 because we're using binary classification (0 or 1)

# Step 4: Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Step 5: Train the model
history = model.fit(x_train, y_train, epochs=5, batch_size=64, validation_data=(x_test, y_test))

# Step 6: Evaluate the model
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"Test Accuracy: {test_acc:.4f}")

# Optionally, you can plot the training history if you'd like to visualize the performance
import matplotlib.pyplot as plt

# Plot training and validation accuracy
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()



"""# Expt 8: To study and implement a CNN Model for Digit Recognition application"""

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

# 1. Load and Preprocess the Data
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# Normalize pixel values to be between 0 and 1
train_images = train_images.astype('float32') / 255.0
test_images = test_images.astype('float32') / 255.0

# Reshape images to include the channel dimension (28, 28, 1)
train_images = train_images.reshape((60000, 28, 28, 1))
test_images = test_images.reshape((10000, 28, 28, 1))

# One-hot encode the labels
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

# 2. Build the CNN Model
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(10, activation='softmax'))

# Model Summary
model.summary()

# 3. Compile the Model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# 4. Train the Model
epochs = 10
batch_size = 64
history = model.fit(train_images, train_labels, epochs=epochs, batch_size=batch_size, validation_split=0.2)

# 5. Evaluate the Model
test_loss, test_accuracy = model.evaluate(test_images, test_labels, verbose=0)
print(f"Test Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")

# Plot training history
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend()
plt.title('Accuracy over Epochs')

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend()
plt.title('Loss over Epochs')
plt.show()

# 6. Make Predictions (Example)
import matplotlib.pyplot as plt

predictions = model.predict(test_images[:10])
predicted_labels = np.argmax(predictions, axis=1)
true_labels = np.argmax(test_labels[:10], axis=1)

plt.figure(figsize=(10, 5))
for i in range(10):
    plt.subplot(2, 5, i + 1)
    plt.imshow(test_images[i].reshape(28, 28), cmap='gray')
    plt.title(f"Predicted: {predicted_labels[i]}\nTrue: {true_labels[i]}")
    plt.axis('off')
plt.tight_layout()
plt.show()
'''
    print("I gotchu man!")
