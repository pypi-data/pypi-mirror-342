# alqueda.py

class alqueda:
    @staticmethod
    def error_correction_learning_algo():
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
    def memory_based_algo():
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
    def hebbian_learning():
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
    def gate_operation_single_layer():
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
    def mlp_xor_gate():
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
    def xor_with_rbf():
        print("""
import numpy as np
import matplotlib.pyplot as plt

# Gaussian function based on Euclidean distance
def gaussian(v, w):
    return np.exp(-np.linalg.norm(v - w) ** 2)

# XOR input and output
inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
outputs = np.array([0, 1, 1, 0])

# Gaussian centers
w1, w2 = np.array([1, 1]), np.array([0, 0])

# Apply Gaussian functions
f1 = [gaussian(i, w1) for i in inputs]
f2 = [gaussian(i, w2) for i in inputs]

# Plotting
plt.figure(figsize=(6, 6))
plotted_labels = set()
for i in range(len(inputs)):
    marker = 'x' if outputs[i] == 0 else 'o'
    label = f"class {outputs[i]}"
    if label not in plotted_labels:

        plt.scatter(f1[i], f2[i], marker=marker, s=100, edgecolors='k')

# Plot decision boundary (optional)
x = np.linspace(0, 1, 100)
plt.plot(x, -x + 1, label="Decision Boundary")

# Labels and legend
plt.xlabel("Gaussian Output 1 (f1)")
plt.ylabel("Gaussian Output 2 (f2)")
plt.title("XOR Inputs Transformed with Gaussian Functions")
plt.legend()
plt.grid(True)
plt.show()

""")

    @staticmethod
    def hebbian_vs_pca():
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
    def som():
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
    def bptt_rnn():
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
    def hopfield():
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
\    output_pattern = np.array(input_pattern)
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
print("Recovered Pattern:", recovered_pattern)
              """)
    @staticmethod
    def neural_network_mnsit():
        print("""
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# Load and preprocess data
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0  # Normalize
x_train = x_train[..., np.newaxis]  # Add channel dim
x_test = x_test[..., np.newaxis]
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# Build model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D(2, 2),
    Dropout(0.25),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Dropout(0.25),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(10, activation='softmax')
])

# Compile and train
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
history = model.fit(x_train, y_train, epochs=10, batch_size=32, validation_data=(x_test, y_test))

# Evaluate
loss, acc = model.evaluate(x_test, y_test)
print(f"Test Loss: {loss:.4f}, Test Accuracy: {acc:.4f}")

# Plot accuracy
plt.plot(history.history['accuracy'], label='Train Acc')
plt.plot(history.history['val_accuracy'], label='Val Acc')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

""")

    @staticmethod
    def optimization_methods():
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
    def resNet_alexNet_vgg_placenet():
        print("""
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt
import numpy as np

# Load and preprocess MNIST dataset
def get_data():
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train = x_train.reshape(-1, 28, 28, 1).astype('float32') / 255.0
    x_test = x_test.reshape(-1, 28, 28, 1).astype('float32') / 255.0
    x_train = (x_train - 0.5) / 0.5  # Normalize to [-1, 1]
    x_test = (x_test - 0.5) / 0.5
    y_train = to_categorical(y_train, 10)
    y_test = to_categorical(y_test, 10)
    train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train)).shuffle(60000).batch(64)
    test_dataset = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(1000)
    return train_dataset, test_dataset

# Define LeNet architecture
def create_lenet():
    model = models.Sequential([
        layers.Conv2D(6, (5, 5), activation='relu', input_shape=(28, 28, 1)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(16, (5, 5), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(120, activation='relu'),
        layers.Dense(84, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    return model

# Define AlexNet architecture (adapted for MNIST)
def create_alexnet():
    model = models.Sequential([
        layers.Conv2D(64, (3, 3), strides=(1, 1), padding='same', activation='relu', input_shape=(28, 28, 1)),
        layers.MaxPooling2D((2, 2), strides=2),
        layers.Conv2D(192, (3, 3), padding='same', activation='relu'),
        layers.MaxPooling2D((2, 2), strides=2),
        layers.Conv2D(384, (3, 3), padding='same', activation='relu'),
        layers.Conv2D(256, (3, 3), padding='same', activation='relu'),
        layers.Conv2D(256, (3, 3), padding='same', activation='relu'),
        layers.MaxPooling2D((2, 2), strides=2),
        layers.Flatten(),
        layers.Dense(4096, activation='relu'),
        layers.Dense(4096, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    return model

# Define VGG architecture (simplified VGG16 for MNIST)
def create_vgg():
    model = models.Sequential([
        layers.Conv2D(64, (3, 3), padding='same', activation='relu', input_shape=(28, 28, 1)),
        layers.Conv2D(64, (3, 3), padding='same', activation='relu'),
        layers.MaxPooling2D((2, 2), strides=2),
        layers.Conv2D(128, (3, 3), padding='same', activation='relu'),
        layers.Conv2D(128, (3, 3), padding='same', activation='relu'),
        layers.MaxPooling2D((2, 2), strides=2),
        layers.Conv2D(256, (3, 3), padding='same', activation='relu'),
        layers.Conv2D(256, (3, 3), padding='same', activation='relu'),
        layers.MaxPooling2D((2, 2), strides=2),
        layers.Flatten(),
        layers.Dense(512, activation='relu'),
        layers.Dense(512, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    return model

# Define Places365-CNN architecture (simplified for MNIST)
def create_placesnet():
    model = models.Sequential([
        layers.Conv2D(96, (7, 7), strides=(2, 2), padding='valid', activation='relu', input_shape=(28, 28, 1)),
        layers.MaxPooling2D((2, 2), strides=2),
        layers.Conv2D(256, (5, 5), padding='same', activation='relu'),
        layers.MaxPooling2D((2, 2), strides=2),
        layers.Conv2D(384, (3, 3), padding='same', activation='relu'),
        layers.Conv2D(384, (3, 3), padding='same', activation='relu'),
        layers.Conv2D(256, (3, 3), padding='same', activation='relu'),
        layers.MaxPooling2D((2, 2), strides=2),
        layers.Flatten(),
        layers.Dense(4096, activation='relu'),
        layers.Dense(4096, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    return model

# Train and evaluate model
def train_model(model_fn, train_dataset, test_dataset, optimizer_type):
    model = model_fn()
    model.compile(optimizer=optimizer_type(learning_rate=0.001),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    for epoch in range(5):
        model.fit(train_dataset, epochs=1, verbose=0)
        print(f"Epoch {epoch+1} completed for {model_fn.__name__.replace('create_', '')}")

    loss, accuracy = model.evaluate(test_dataset, verbose=0)
    print(f"Accuracy with {model_fn.__name__.replace('create_', '')}: {accuracy*100:.2f}%")
    return model

# Visualization function
def visualize_filters(model, model_name):
    for layer in model.layers:
        if isinstance(layer, layers.Conv2D):
            weights = layer.get_weights()[0]  # Shape: (height, width, in_channels, out_channels)
            filters = weights[:, :, 0, :]  # Take first input channel
            num_filters = min(6, filters.shape[-1])
            fig, axes = plt.subplots(1, num_filters)
            if num_filters == 1:
                axes = [axes]
            for i, ax in enumerate(axes):
                ax.imshow(filters[:, :, i], cmap='gray')
                ax.axis('off')
            plt.suptitle(f"First Conv Layer Filters - {model_name}")
            plt.savefig(f'{model_name}_filters.png')
            plt.close()
            break

# Load data
train_dataset, test_dataset = get_data()

# Train and visualize models
model_fns = [create_lenet, create_alexnet, create_vgg, create_placesnet]  # Renamed to avoid conflict
optimizers = [tf.keras.optimizers.Adam]
for model_fn in model_fns:
    for opt in optimizers:
        trained_model = train_model(model_fn, train_dataset, test_dataset, opt)
        visualize_filters(trained_model, model_fn.__name__.replace('create_', ''))
""")

    @staticmethod
    def vgg():
        print("""
import numpy as np
import cv2
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Input
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import confusion_matrix

# Load and preprocess MNIST
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_train = np.repeat(x_train[..., np.newaxis], 3, axis=-1)  # To 3 channels
x_test = np.repeat(x_test[..., np.newaxis], 3, axis=-1)
x_train_resized = np.array([cv2.resize(img, (32, 32)) for img in x_train])
x_test_resized = np.array([cv2.resize(img, (32, 32)) for img in x_test])
x_train_resized = x_train_resized / 255.0
x_test_resized = x_test_resized / 255.0
x_train = x_train / 255.0
x_test = x_test / 255.0

# One-hot encode labels
y_train_cat = to_categorical(y_train, 10)
y_test_cat = to_categorical(y_test, 10)

# VGG-16 model
vgg_base = VGG16(weights='imagenet', include_top=False, input_shape=(32, 32, 3))
for layer in vgg_base.layers:
    layer.trainable = False

x = Flatten()(vgg_base.output)
x = Dense(256, activation='relu')(x)
output = Dense(10, activation='softmax')(x)
vgg_model = Model(inputs=vgg_base.input, outputs=output)
vgg_model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

# Train VGG-16
vgg_model.fit(x_train_resized, y_train_cat, epochs=5, batch_size=64, validation_data=(x_test_resized, y_test_cat))

# Custom CNN (PlacesNet-style)
inputs = Input(shape=(28, 28, 3))
x = Conv2D(64, (3,3), activation='relu', padding='same')(inputs)
x = MaxPooling2D((2,2))(x)
x = Conv2D(128, (3,3), activation='relu', padding='same')(x)
x = MaxPooling2D((2,2))(x)
x = Flatten()(x)
x = Dense(256, activation='relu')(x)
outputs = Dense(10, activation='softmax')(x)

placesnet_model = Model(inputs, outputs)
placesnet_model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

# Train PlacesNet
placesnet_model.fit(x_train, y_train_cat, epochs=5, batch_size=64, validation_data=(x_test, y_test_cat))

# Confusion matrix plot function
def plot_conf_matrix(model, x_data, y_true, title):
    preds = np.argmax(model.predict(x_data), axis=1)
    cm = confusion_matrix(y_true, preds)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Confusion Matrix: {title}')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.show()

# Plot confusion matrices
plot_conf_matrix(vgg_model, x_test_resized, y_test, "VGG-16")
plot_conf_matrix(placesnet_model, x_test, y_test, "PlacesNet")

# Feature map visualization
def show_feature_maps(model, image, title):
    conv_layers = [l.output for l in model.layers if isinstance(l, Conv2D)]
    feature_model = Model(inputs=model.input, outputs=conv_layers)
    feature_maps = feature_model.predict(np.expand_dims(image, axis=0))

    for i, fmap in enumerate(feature_maps[:3]):  # Show first 3 layers
        plt.figure(figsize=(10, 3))
        for j in range(min(fmap.shape[-1], 6)):  # First 6 filters
            plt.subplot(1, 6, j+1)
            plt.imshow(fmap[0, :, :, j], cmap='viridis')
            plt.axis('off')
        plt.suptitle(f"{title} - Layer {i+1}")
        plt.show()

# Show sample feature maps
show_feature_maps(vgg_model, x_test_resized[0], "VGG-16")
show_feature_maps(placesnet_model, x_test[0], "PlacesNet")

""")
    
    @staticmethod
    def rnn_lstm():
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
