# alqueda.py

class alqueda:
    @staticmethod
    def q1():
        print("""
# NumPy neuron training
import numpy as np
class Neuron:
    def __init__(self,num):
      self.weights=np.random.rand(num)
      self.bias=np.random.rand()
    def activate(self,x):
      return 1/(1+np.exp(-np.dot(x,self.weights)-self.bias))
    def train(self,inputs,targets,lr=0.01,itter=1000):
      for _ in range(itter):
        idx=np.random.randint(len(inputs))
        error=targets[idx]-self.activate(inputs[idx])
        self.weights+=lr*error*inputs[idx]
        self.bias+=lr*error
neuron=Neuron(3)
x_train=np.array([[0,0,1],[0,1,1],[1,0,1],[1,1,1]])
y_train=np.array([0,1,1,1])
neuron.train(x_train,y_train)
for x,y in zip(x_train,y_train):
  print(f"input:{x}, prediction:{neuron.activate(x):.4f},actual:{y}")
""")

    @staticmethod
    def q2():
        print("""
# PyTorch k-NN
import torch
x_train=torch.tensor([[1,2],[2,3],[3,4],[4,5]],dtype=torch.float32)
y_train=torch.tensor([0,0,1,1],dtype=torch.float32)
x_test=torch.tensor([[5,6],[0,1]],dtype=torch.float32)
k=3
y_pred=[]
for x in x_test:
  dist=torch.norm(x_train-x,dim=1)
  neaes_labels=y_train[torch.topk(dist,k,largest=False).indices]
  y_pred.append(torch.mode(neaes_labels).values.item())
print(y_pred)
""")

    @staticmethod
    def q3():
        print("""
import numpy as np
class Neuron:
  def __init__(self,num):
    self.weight=np.random.rand(num)
  def activate(self,inputs):
    out=np.dot(inputs,self.weight)
    return out
  def learn_heabbian(self,inputs,lr=0.01):
    activation=self.activate(inputs)
    self.weight+=lr*activation*inputs
num=3
neuron=Neuron(num)
inputs=np.array([0.5,0.3,0.2])
lr=0.1
for i in range(1000):
  neuron.learn_heabbian(inputs,lr)
print(neuron.weight)
""")

    @staticmethod
    def q4():
        print("""
# Perceptron classifier
import numpy as np

def step_function(x):
    return 1 if x >= 0 else 0

inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
outputs = np.array([0, 0, 0, 1])
weights = np.zeros(2)
bias = 0
lr = 0.1

for _ in range(10):
    for i in range(len(inputs)):
        x = inputs[i]
        y = outputs[i]
        act = step_function(np.dot(weights, x) + bias)
        error = y - act
        weights += lr * error * x
        bias += lr * error  # ✅ FIXED HERE

print("Final Weights:", weights)
print("Final Bias:", bias)

for x in inputs:
    z = np.dot(weights, x) + bias
    output = step_function(z)
    print(f"Input {x} => Output: {output}")
""")

    @staticmethod
    def q5():
        print("""
import tensorflow as tf
import numpy as np

# XOR inputs and outputs
x = np.array([[0,0],[0,1],[1,0],[1,1]])
y = np.array([[0],[1],[1],[0]])

# Build the model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(2, activation='sigmoid'),  # Hidden layer
    tf.keras.layers.Dense(1, activation='sigmoid')   # Output layer
])

# Compile with binary crossentropy loss (for classification)
model.compile(optimizer='adam', loss='binary_crossentropy')

# Train for more epochs
model.fit(x, y, epochs=5000, verbose=0)

# Test predictions
for i in x:
    prediction = model.predict(i.reshape(1, -1), verbose=0)[0][0]
    print(f"Input: {i}, Predicted: {prediction:.2f}")
""")

    @staticmethod
    def q6():
        print("""
import numpy as np
import matplotlib.pyplot as plt
def gaussion(v,w):
  return np.exp(-np.linalg.norm(v-w)**2)
inputs=np.array([[0,0],[0,1],[1,0],[1,1]])
outputs=np.array([0,1,1,0])
w1,w2=np.array([1,1]),np.array([0,0])
f1=[gaussion(i,w1) for i in inputs]
f2=[gaussion(i,w2) for i in inputs]
plt.figure(figsize=(5,5))
for i in range(len(inputs)):
  marker='x' if outputs[i]==0 else 'o'
  label=f"class{outputs[i]}"
  plt.scatter(f1[i],f2[i],marker=marker,label=label)
x=np.linspace(0,1,100)
plt.plot(x,-x+1)
plt.show()
""")

    @staticmethod
    def q7():
        print("""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
data=np.random.multivariate_normal([0,0],[[3,2],[2,2]],1000)
weights=np.random.randn(2)
for x in data:
  weights+=0.01*np.dot(weights,x)*x
weights/=np.linalg.norm(weights)
pca=PCA(n_components=1).fit(data).components_[0]
plt.scatter(data[:,0],data[:,1],alpha=0.3)
plt.quiver(0,0,weights[0],weights[1],scale=3)
plt.quiver(0,0,pca[0],pca[1],color='g',scale=3)
plt.show()
""")

    @staticmethod
    def q8():
        print("""
import numpy as np
import matplotlib.pyplot as plt

class SOM:
    def __init__(self, grid_size, input_dim, learning_rate=0.5, sigma=1.0, iterations=1000):
        self.grid_size = grid_size
        self.input_dim = input_dim
        self.learning_rate = learning_rate
        self.sigma = sigma
        self.iterations = iterations

        # Initialize weights randomly between 0 and 1
        self.weights = np.random.rand(grid_size, grid_size, input_dim)

        # Grid of neuron coordinates (i,j) for each cell in the SOM
        self.neuron_positions = np.array([[np.array([i, j]) for j in range(grid_size)] for i in range(grid_size)])

    def find_bmu(self, sample):
        distances = np.linalg.norm(self.weights - sample, axis=2)  # Euclidean distance
        return np.unravel_index(np.argmin(distances), distances.shape)

    def update_weights(self, sample, bmu, iteration):
        learning_rate = self.learning_rate * (1 - iteration / self.iterations)
        sigma = self.sigma * (1 - iteration / self.iterations)

        # Calculate distance of each neuron to the BMU
        distance_to_bmu = np.linalg.norm(self.neuron_positions - np.array(bmu), axis=2)

        # Gaussian neighborhood function
        neighborhood = np.exp(-(distance_to_bmu**2) / (2 * (sigma**2)))

        # Expand dimensions to match shape for broadcasting
        influence = neighborhood[:, :, np.newaxis]

        # Update rule
        self.weights += learning_rate * influence * (sample - self.weights)

    def train(self, data):
        for i in range(self.iterations):
            sample = data[np.random.randint(0, len(data))]
            bmu = self.find_bmu(sample)
            self.update_weights(sample, bmu, i)

    def plot_weights(self):
        fig, ax = plt.subplots(figsize=(6, 6))
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                color = np.clip(self.weights[i, j], 0, 1)  # Ensure RGB range
                ax.add_patch(plt.Rectangle((j, self.grid_size - i - 1), 1, 1, color=color, ec='black'))
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(0, self.grid_size)
        ax.set_ylim(0, self.grid_size)
        plt.title("Self-Organizing Map (SOM)")
        plt.show()

# Generate random RGB data
np.random.seed(42)
data = np.random.rand(1000, 3)

# Create and train SOM
som = SOM(grid_size=10, input_dim=3, iterations=5000)
som.train(data)

# Plot the result
som.plot_weights()

""")

    @staticmethod
    def q9():
        print("""
import tensorflow as tf

# Define input, hidden, and output sizes
input_size, hidden_size, output_size = 3, 5, 1

# Input layer for RNN (time series input)
inputs = tf.keras.Input(shape=(None, input_size))

# Simple RNN layer
x = tf.keras.layers.SimpleRNN(hidden_size)(inputs)

# Output layer for binary classification (sigmoid gives probabilities)
outputs = tf.keras.layers.Dense(output_size, activation="sigmoid")(x)

# Define the model
model = tf.keras.Model(inputs, outputs)

# Compile the model with binary_crossentropy and accuracy metric
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

# Generate synthetic binary classification data
data = tf.random.normal((2, 4, input_size))
targets = tf.random.uniform((2, output_size), minval=0, maxval=2, dtype=tf.int32)

# Train the model
model.fit(data, targets, epochs=10, verbose=2)

""")

    @staticmethod
    def q10():
        print("""
import numpy as np
def train_hopfield(patterns):
    num_neurons = len(patterns[0])
    weight_matrix = np.zeros((num_neurons, num_neurons))
    for pattern in patterns:
        pattern = np.array(pattern).reshape(-1, 1)
        weight_matrix += pattern @ pattern.T
    np.fill_diagonal(weight_matrix, 0)  # No self-connections
    return weight_matrix
def recall_pattern(weight_matrix, input_pattern, max_iterations=10):
    output_pattern = np.array(input_pattern)
    for _ in range(max_iterations):
        for i in range(len(output_pattern)):
            net_input = np.dot(weight_matrix[i], output_pattern)
            output_pattern[i] = 1 if net_input >= 0 else -1
    return output_pattern
# Original pattern
original_pattern = [-1, 1, -1, -1, -1, -1, -1, 1, -1, 1]
# Train the Hopfield network
weight_matrix = train_hopfield([original_pattern])
# Noisy pattern to recover
noisy_pattern = [-1, -1, -1, 1, -1, -1, -1, 1, -1, -1]
# Recovered pattern
recovered_pattern = recall_pattern(weight_matrix, noisy_pattern)
print("Original Pattern:", original_pattern)
print("Noisy Pattern:", noisy_pattern)
print("Recovered Pattern:", recovered_pattern)""")
    @staticmethod
    def q11():
        print("""
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
#Load the dataset
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
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(10, activation='softmax'))
# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# Train the model
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test,
y_test))
# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print("Loss: ", loss)
print("Accuracy: ", accuracy)
#Extract the accuracy history
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
# Plot the accuracy history
plt.plot(acc)
plt.plot(val_acc)
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()
""")

    @staticmethod
    def q12():
        print("""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Load and preprocess data
def get_data():
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0
    return (x_train, y_train), (x_test, y_test)

# Define model
def build_model():
    model = keras.Sequential([
        layers.Flatten(input_shape=(28, 28)),
        layers.Dense(128, activation='relu'),
        layers.Dense(64, activation='relu'),
        layers.Dense(10)
    ])
    return model

# Train and evaluate with different optimizers
def train_and_evaluate(optimizer):
    model = build_model()
    model.compile(optimizer=optimizer, loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])
    (x_train, y_train), (x_test, y_test) = get_data()
    model.fit(x_train, y_train, epochs=5, batch_size=64, verbose=1)
    loss, accuracy = model.evaluate(x_test, y_test, verbose=0)
    print(f"Accuracy with {optimizer}: {accuracy:.2%}")

optimizers = ['Adagrad', 'RMSprop', 'Adam']
for opt in optimizers:
    train_and_evaluate(opt)
""")

    @staticmethod
    def q13():
        print("""
# Train and evaluate LeNet and AlexNet on MNIST dataset with filter visualization
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import numpy as np

# Load MNIST dataset
def get_data():
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,),
(0.5,))])
    trainset = torchvision.datasets.MNIST(root='./data', train=True, download=True,
transform=transform)
    testset = torchvision.datasets.MNIST(root='./data', train=False, download=True,
transform=transform)
    trainloader = DataLoader(trainset, batch_size=64, shuffle=True)
    testloader = DataLoader(testset, batch_size=1000, shuffle=False)
    return trainloader, testloader

# Define CNN Architectures
class LeNet(nn.Module):
    def __init__(self):
        super(LeNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, kernel_size=5)
        self.conv2 = nn.Conv2d(6, 16, kernel_size=5)
        self.fc1 = nn.Linear(16*4*4, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(2, 2)

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = x.view(-1, 16*4*4)
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

class AlexNet(nn.Module):
    def __init__(self):
        super(AlexNet, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(64, 192, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(192, 384, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(384, 256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.classifier = nn.Sequential(
            nn.Linear(256 * 3 * 3, 4096),
            nn.ReLU(),
            nn.Linear(4096, 4096),
            nn.ReLU(),
            nn.Linear(4096, 10),
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x

# Train and evaluate model
def train_model(model, trainloader, testloader, optimizer_type):
    model = model()
    criterion = nn.CrossEntropyLoss()
    optimizer = optimizer_type(model.parameters(), lr=0.01)

    for epoch in range(5):
        model.train()
        for images, labels in trainloader:
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
        print(f"Epoch {epoch+1} completed")

    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in testloader:
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total
    print(f"Accuracy with {model.__class__.__name__}: {accuracy:.2f}%")
    return model

# Visualization Function
def visualize_filters(model):
    with torch.no_grad():
        for name, param in model.named_parameters():
            if 'conv' in name and param.requires_grad:
                filters = param.cpu().numpy()
                fig, axes = plt.subplots(1, min(6, filters.shape[0]))
                for i, ax in enumerate(axes):
                    ax.imshow(filters[i, 0], cmap='gray')
                    ax.axis('off')
                plt.show()
                break

# Load data
trainloader, testloader = get_data()

# Train models
models = [LeNet, AlexNet]
optimizers = [optim.Adam]
for model in models:
    for opt in optimizers:
        trained_model = train_model(model, trainloader, testloader, opt)
        visualize_filters(trained_model)
""")

    @staticmethod
    def q14():
        print("""
import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import cv2
# Load MNIST Dataset
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
# Preprocess Data
x_train = np.expand_dims(x_train, axis=-1)
x_test = np.expand_dims(x_test, axis=-1)
# Convert grayscale to 3 channels for pretrained models
x_train = np.repeat(x_train, 3, axis=-1)
x_test = np.repeat(x_test, 3, axis=-1)
# Resize images to 32x32 for VGG-16 compatibility
x_train_resized = np.array([cv2.resize(img, (32, 32)) for img in x_train])
x_test_resized = np.array([cv2.resize(img, (32, 32)) for img in x_test])
# Normalize data
x_train_resized, x_test_resized = x_train_resized / 255.0, x_test_resized / 255.0
x_train, x_test = x_train / 255.0, x_test / 255.0
# Convert labels to categorical
y_train_cat = to_categorical(y_train, 10)
y_test_cat = to_categorical(y_test, 10)
# Define VGG-16 Model
base_model_vgg = VGG16(weights='imagenet', include_top=False, input_shape=(32, 32, 3))
for layer in base_model_vgg.layers:
    layer.trainable = False
x = Flatten()(base_model_vgg.output)
x = Dense(256, activation='relu')(x)
x = Dense(10, activation='softmax')(x)
vgg_model = Model(inputs=base_model_vgg.input, outputs=x)
vgg_model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
# Train VGG-16
vgg_model.fit(x_train_resized, y_train_cat, epochs=5, batch_size=64,
validation_data=(x_test_resized, y_test_cat))

# Define PlacesNet-like CNN
input_layer = Input(shape=(28, 28, 3))
x = Conv2D(64, (3,3), activation='relu', padding='same')(input_layer)
x = MaxPooling2D((2,2))(x)
x = Conv2D(128, (3,3), activation='relu', padding='same')(x)
x = MaxPooling2D((2,2))(x)
x = Flatten()(x)
x = Dense(256, activation='relu')(x)
x = Dense(10, activation='softmax')(x)

placesnet_model = Model(inputs=input_layer, outputs=x)
placesnet_model.compile(optimizer=Adam(), loss='categorical_crossentropy',
metrics=['accuracy'])

# Train PlacesNet
placesnet_model.fit(x_train, y_train_cat, epochs=5, batch_size=64, validation_data=(x_test,
y_test_cat))

# Evaluate and Visualize Results
def plot_confusion_matrix(model, x_test, y_test, title):
    y_pred = np.argmax(model.predict(x_test), axis=1)
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title(f'Confusion Matrix: {title}')
    plt.show()

# Confusion Matrices
plot_confusion_matrix(vgg_model, x_test_resized, y_test, "VGG-16")
plot_confusion_matrix(placesnet_model, x_test, y_test, "PlacesNet")

# Display Feature Maps
def visualize_feature_maps(model, x_sample):
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

# Show feature maps of first test image
visualize_feature_maps(vgg_model, x_test_resized[0])
visualize_feature_maps(placesnet_model, x_test[0])
""")
    
        @staticmethod
        def q15():
            print("""
import numpy as np
from numpy.random import randn, seed


def sigmoid(x): return 1 / (1 + np.exp(-x))


def rnn_cell(xt, ht, Wx, Wh, b): return np.tanh(Wx @ xt + Wh @ ht + b)


def rnn_forward(x_seq, h0, Wx, Wh, b):
    h, hs = h0, []
    for xt in x_seq:
        h = rnn_cell(xt, h, Wx, Wh, b)
        hs.append(h)
    return np.stack(hs)


def lstm_cell(xt, ht, ct, Wf, Wi, Wc, Wo, bf, bi, bc, bo):
    xh = np.vstack((ht, xt))
    ft = sigmoid(Wf @ xh + bf)
    it = sigmoid(Wi @ xh + bi)
    c̃t = np.tanh(Wc @ xh + bc)
    ct_next = ft * ct + it * c̃t
    ot = sigmoid(Wo @ xh + bo)
    ht_next = ot * np.tanh(ct_next)
    return ht_next, ct_next


# -------- Sample Test --------
seed(0)
i_size, h_size, seq_len = 2, 2, 2
x_seq = [randn(i_size, 1) for _ in range(seq_len)]
h0 = c0 = np.zeros((h_size, 1))

# RNN weights
Wx, Wh, b = [randn(*s) for s in [(h_size, i_size), (h_size, h_size), (h_size, 1)]]

# LSTM weights and biases
Wf, Wi, Wc, Wo, bf, bi, bc, bo = [randn(h_size, h_size + i_size) for _ in range(4)] + [randn(h_size, 1) for _ in
                                                                                       range(4)]

print("=== RNN Output ===")
print(np.round(rnn_forward(x_seq, h0, Wx, Wh, b).squeeze(), 3))

print("\n=== LSTM Output (1st step) ===")
ht, ct = lstm_cell(x_seq[0], h0, c0, Wf, Wi, Wc, Wo, bf, bi, bc, bo)
print("h:", np.round(ht.squeeze(), 3))
print("c:", np.round(ct.squeeze(), 3))
""")
