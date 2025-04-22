# alqueda.py

class alqueda:
    @staticmethod
    def q1():
        print("""
# NumPy neuron training
import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def train_neuron(X, y, epochs=1000, lr=0.01):
    m = X.shape[0]
    w = np.zeros(X.shape[1])
    b = 0

    for _ in range(epochs):
        y_pred = sigmoid(np.dot(X, w) + b)
        dw = (1/m) * np.dot(X.T, (y_pred - y))
        db = (1/m) * np.sum(y_pred - y)

        w -= lr * dw
        b -= lr * db

    return w, b

# Test the function
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([0, 0, 0, 1])

w, b = train_neuron(X, y)
print("Weights:", w)
print("Bias:", b)
""")

    @staticmethod
    def q2():
        print("""
# PyTorch k-NN
import torch
import torch.nn as nn
import torch.optim as optim

class KNN(nn.Module):
    def __init__(self, k=3):
        super(KNN, self).__init__()
        self.k = k

    def forward(self, X_train, X_test):
        distances = torch.cdist(X_test, X_train)
        _, indices = torch.topk(distances, self.k, largest=False)
        return indices

# Test the function
X_train = torch.tensor([[1.0, 2.0], [2.0, 3.0], [3.0, 4.0]])
X_test = torch.tensor([[1.5, 2.5]])

knn = KNN(k=2)
neighbors = knn(X_train, X_test)
print("Neighbors' indices:", neighbors)
""")

    @staticmethod
    def q3():
        print("""
# Hebbian learning
import numpy as np

def hebbian_learning(X, learning_rate=0.1, epochs=1000):
    W = np.zeros((X.shape[1], X.shape[1]))

    for _ in range(epochs):
        for x in X:
            W += learning_rate * np.outer(x, x)

    return W

# Test the function
X = np.array([[1, 2], [3, 4], [5, 6]])
W = hebbian_learning(X)
print("Hebbian learning matrix:\n", W)
""")

    @staticmethod
    def q4():
        print("""
# Perceptron classifier
import numpy as np

class Perceptron:
    def __init__(self, input_size, learning_rate=0.01, epochs=1000):
        self.lr = learning_rate
        self.epochs = epochs
        self.weights = np.zeros(input_size)
        self.bias = 0

    def predict(self, X):
        return np.dot(X, self.weights) + self.bias > 0

    def train(self, X, y):
        for _ in range(self.epochs):
            for xi, target in zip(X, y):
                update = self.lr * (target - self.predict(xi))
                self.weights += update * xi
                self.bias += update

# Test the function
X = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
y = np.array([0, 0, 1, 1])

model = Perceptron(input_size=2)
model.train(X, y)
predictions = model.predict(X)
print("Predictions:", predictions)
""")

    @staticmethod
    def q5():
        print("""
# TensorFlow XOR
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

def create_xor_model():
    model = Sequential([
        Dense(10, input_dim=2, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# Test the function
X = [[0, 0], [0, 1], [1, 0], [1, 1]]
y = [0, 1, 1, 0]

model = create_xor_model()
model.fit(X, y, epochs=5000, verbose=0)
predictions = model.predict(X)
print("Predictions:", predictions)
""")

    @staticmethod
    def q6():
        print("""
# Gaussian RBF visualization
import numpy as np
import matplotlib.pyplot as plt

def gaussian_rbf(x, center, sigma):
    return np.exp(-np.linalg.norm(x - center) ** 2 / (2 * sigma ** 2))

# Test the function
x = np.array([[i, j] for i in np.linspace(-3, 3, 100) for j in np.linspace(-3, 3, 100)])
center = np.array([0, 0])
sigma = 1.0
z = np.array([gaussian_rbf(xi, center, sigma) for xi in x])

plt.scatter(x[:, 0], x[:, 1], c=z, cmap='viridis')
plt.colorbar()
plt.title("Gaussian RBF Visualization")
plt.show()
""")

    @staticmethod
    def q7():
        print("""
# Hebbian vs PCA vector
import numpy as np
from sklearn.decomposition import PCA

def hebbian_learning(X, learning_rate=0.1, epochs=1000):
    W = np.zeros((X.shape[1], X.shape[1]))

    for _ in range(epochs):
        for x in X:
            W += learning_rate * np.outer(x, x)

    return W

def pca(X, n_components=2):
    pca_model = PCA(n_components=n_components)
    return pca_model.fit_transform(X)

# Test the function
X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
hebbian_matrix = hebbian_learning(X)
pca_result = pca(X)
print("Hebbian Learning Matrix:\n", hebbian_matrix)
print("PCA Result:\n", pca_result)
""")

    @staticmethod
    def q8():
        print("""
# Self-Organizing Map (SOM)
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class SOM:
    def __init__(self, m, n, dim, lr=0.1, radius=1):
        self.m, self.n, self.dim = m, n, dim
        self.lr, self.radius = lr, radius
        self.weights = np.random.rand(m, n, dim)

    def find_bmu(self, x):
        dists = np.linalg.norm(self.weights - x, axis=2)
        return np.unravel_index(np.argmin(dists), dists.shape)

    def train(self, X, epochs):
        for _ in range(epochs):
            for x in X:
                bmu = self.find_bmu(x)
                self.weights[bmu] += self.lr * (x - self.weights[bmu])

# Test the function
X = np.array([[0.1, 0.2], [0.4, 0.5], [0.7, 0.8]])
som = SOM(2, 2, 2)
som.train(X, epochs=10)
print("SOM weights:\n", som.weights)
""")

    @staticmethod
    def q9():
        print("""
# TensorFlow RNN binary classifier
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense

def create_rnn_model(input_shape):
    model = Sequential([
        SimpleRNN(10, input_shape=input_shape, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# Test the function
X = np.array([[[0], [1]], [[1], [0]], [[0], [1]], [[1], [0]]])
y = np.array([1, 0, 0, 1])

model = create_rnn_model(input_shape=(2, 1))
model.fit(X, y, epochs=100, verbose=0)
predictions = model.predict(X)
print("Predictions:", predictions)
""")

    @staticmethod
    def q10():
        print("""
# Hopfield network with Hebbian learning
import numpy as np

class Hopfield:
    def __init__(self, size):
        self.size = size
        self.weights = np.zeros((size, size))

    def train(self, patterns):
        for p in patterns:
            self.weights += np.outer(p, p)
        np.fill_diagonal(self.weights, 0)

    def predict(self, input_pattern):
        output = input_pattern
        while True:
            new_output = np.sign(np.dot(self.weights, output))
            if np.array_equal(new_output, output):
                break
            output = new_output
        return output

# Test the function
patterns = np.array([[1, -1, 1], [-1, 1, -1]])
hopfield = Hopfield(size=3)
hopfield.train(patterns)
result = hopfield.predict(np.array([1, 1, -1]))
print("Hopfield network output:", result)
""")

    @staticmethod
    def q11():
        print("""
# CNN model on MNIST dataset
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

def create_cnn_model():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# Test the function
model = create_cnn_model()
model.summary()
""")

    @staticmethod
    def q12():
        print("""
# Train and evaluate different optimizers on MNIST dataset
import tensorflow as tf
from tensorflow.keras.optimizers import SGD, Adam, RMSprop
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.datasets import mnist

def create_model(optimizer):
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(10, activation='softmax')
    ])
    model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# Test the function
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train[..., np.newaxis] / 255.0, x_test[..., np.newaxis] / 255.0

optimizers = [SGD(), Adam(), RMSprop()]

for optimizer in optimizers:
    print(f"\nTraining with {optimizer.get_config()['name']} optimizer:")
    model = create_model(optimizer)
    model.fit(x_train, y_train, epochs=1, batch_size=64, verbose=1)
    model.evaluate(x_test, y_test, verbose=1)
""")

    @staticmethod
    def q13():
        print("""
# Train and evaluate LeNet and AlexNet on MNIST dataset with filter visualization
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
import matplotlib.pyplot as plt

def create_lenet_model():
    model = Sequential([
        Conv2D(6, (5, 5), activation='tanh', input_shape=(28, 28, 1)),
        MaxPooling2D((2, 2)),
        Conv2D(16, (5, 5), activation='tanh'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(120, activation='tanh'),
        Dense(84, activation='tanh'),
        Dense(10, activation='softmax')
    ])
    return model

# Visualize filters
def visualize_filters(model):
    for layer in model.layers:
        if isinstance(layer, Conv2D):
            filters = layer.get_weights()[0]
            print(filters.shape)
            plt.figure(figsize=(10, 10))
            for i in range(filters.shape[-1]):
                plt.subplot(4, 4, i+1)
                plt.imshow(filters[:, :, 0, i], cmap='gray')
                plt.axis('off')
            plt.show()

# Test the function
model = create_lenet_model()
visualize_filters(model)
""")

    @staticmethod
    def q14():
        print("""
# VGG-16 vs PlacesNet on MNIST with confusion matrix and feature map visualization
import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

def create_vgg16_model():
    model = VGG16(weights='imagenet', include_top=False, input_shape=(28, 28, 3))
    model.trainable = False
    return model

def plot_confusion_matrix(cm):
    plt.figure(figsize=(10, 7))
    plt.imshow(cm, cmap='Blues')
    plt.colorbar()
    plt.title('Confusion Matrix')
    plt.show()

# Test the function
model = create_vgg16_model()
model.summary()
""")
