def dl():
    '''
    # class McCullochPittsNeuron:
    #     def __init__(self, weights, threshold):
    #         self.weights = weights
    #         self.threshold = threshold

    #     def activate(self, inputs):
    #         weighted_sum = sum(x * w for x, w in zip(inputs, self.weights))
    #         return weighted_sum >= self.threshold

    # if __name__ == "__main__":
    #     # AND Gate
    #     and_weights = [1, 1]
    #     and_threshold = 2
    #     and_neuron = McCullochPittsNeuron(and_weights, and_threshold)

    #     # OR Gate
    #     or_weights = [1, 1]
    #     or_threshold = 1
    #     or_neuron = McCullochPittsNeuron(or_weights, or_threshold)

    #     # NOT Gate
    #     not_weights = [-1]
    #     not_threshold = 0
    #     not_neuron = McCullochPittsNeuron(not_weights, not_threshold)

    #     # Test Inputs
    #     inputs = [
    #         [0, 0],  # Input 1
    #         [0, 1],  # Input 2
    #         [1, 0],  # Input 3
    #         [1, 1]   # Input 4
    #     ]

    #     print("AND Gate:")
    #     for input in inputs:
    #         output = and_neuron.activate(input)
    #         print(f"Input: {input}, Output: {output}")

    #     print("\nOR Gate:")
    #     for input in inputs:
    #         output = or_neuron.activate(input)
    #         print(f"Input: {input}, Output: {output}")

    #     print("\nNOT Gate:")
    #     single_inputs = [0, 1]
    #     for input in single_inputs:
    #         output = not_neuron.activate([input])
    #         print(f"Input: {input}, Output: {output}")

    # class McCullochPittsNeuron:
    #     def __init__(self, weights, threshold):
    #         self.weights = weights
    #         self.threshold = threshold

    #     def activate(self, inputs):
    #         weighted_sum = sum(x * w for x, w in zip(inputs, self.weights))
    #         return weighted_sum >= self.threshold

    # if __name__ == "__main__":
    #     # AND Gate
    #     and_weights = [1, 1]
    #     and_threshold = 2
    #     and_neuron = McCullochPittsNeuron(and_weights, and_threshold)

    #     # OR Gate
    #     or_weights = [1, 1]
    #     or_threshold = 1
    #     or_neuron = McCullochPittsNeuron(or_weights, or_threshold)

    #     # NOT Gate (can be implemented with a single input)
    #     not_weights = [-1]  # Invert the input
    #     not_threshold = 0
    #     not_neuron = McCullochPittsNeuron(not_weights, not_threshold)

    #     # Test Inputs
    #     inputs = [
    #         [0, 0],  # Input 1
    #         [0, 1],  # Input 2
    #         [1, 0],  # Input 3
    #         [1, 1]   # Input 4
    #     ]

    #     print("AND Gate:")
    #     print("| Input 1 | Input 2 | Output |")
    #     print("|---|---|---|")
    #     for input in inputs:
    #         output = and_neuron.activate(input)
    #         print(f"| {input[0]} | {input[1]} | {output} |")

    #     print("\nOR Gate:")
    #     print("| Input 1 | Input 2 | Output |")
    #     print("|---|---|---|")
    #     for input in inputs:
    #         output = or_neuron.activate(input)
    #         print(f"| {input[0]} | {input[1]} | {output} |")

    #     print("\nNOT Gate:")
    #     print("| Input | Output |")
    #     print("|---|---|")
    #     single_inputs = [0, 1]  # Test inputs for NOT gate
    #     for input in single_inputs:
    #         output = not_neuron.activate([input])  # Pass a single input in a list
    #         print(f"| {input} | {output} |")

    # """# Expt2 (Perceptron Algorithm)"""

    # import numpy as np

    # class Perceptron:
    #     def __init__(self, input_size, lr=0.1, epochs=100):
    #         self.weights = np.zeros(input_size + 1)
    #         self.lr, self.epochs = lr, epochs

    #     def activation(self, x):
    #         return 1 if x >= 0 else 0

    #     def predict(self, inputs):
    #         return self.activation(np.dot(inputs, self.weights[1:]) + self.weights[0])

    #     def train(self, X, y):
    #         for _ in range(self.epochs):
    #             for inputs, label in zip(X, y):
    #                 error = label - self.predict(inputs)
    #                 self.weights[1:] += self.lr * error * inputs
    #                 self.weights[0] += self.lr * error

    # # AND, OR, NOT Gates
    # training_data = {
    #     "AND": (np.array([[0, 0], [0, 1], [1, 0], [1, 1]]), np.array([0, 0, 0, 1])),
    #     "OR": (np.array([[0, 0], [0, 1], [1, 0], [1, 1]]), np.array([0, 1, 1, 1])),
    #     "NOT": (np.array([[0], [1]]), np.array([1, 0]))
    # }

    # for gate, (X, y) in training_data.items():
    #     p = Perceptron(input_size=X.shape[1])
    #     p.train(X, y)
    #     print(f"{gate} Gate:")
    #     for inputs in X:
    #         print(f"{inputs} -> {p.predict(inputs)}")

    # class MLP:
    #     def __init__(self, input_size, hidden_size, output_size, lr=0.1, epochs=1000):
    #         self.weights = [np.random.rand(input_size, hidden_size), np.random.rand(hidden_size, output_size)]
    #         self.biases = [np.random.rand(hidden_size), np.random.rand(output_size)]
    #         self.lr, self.epochs = lr, epochs

    #     def sigmoid(self, x):
    #         return 1 / (1 + np.exp(-x))

    #     def train(self, X, y):
    #         for _ in range(self.epochs):
    #             for inputs, label in zip(X, y):
    #                 # Forward pass
    #                 hidden = self.sigmoid(np.dot(inputs, self.weights[0]) + self.biases[0])
    #                 output = self.sigmoid(np.dot(hidden, self.weights[1]) + self.biases[1])
    #                 # Backward pass
    #                 error = label - output
    #                 d_output = error * output * (1 - output)
    #                 d_hidden = d_output.dot(self.weights[1].T) * hidden * (1 - hidden)
    #                 # Update weights and biases
    #                 self.weights[1] += hidden.reshape(-1, 1).dot(d_output.reshape(1, -1)) * self.lr
    #                 self.weights[0] += inputs.reshape(-1, 1).dot(d_hidden.reshape(1, -1)) * self.lr
    #                 self.biases[1] += d_output * self.lr
    #                 self.biases[0] += d_hidden * self.lr

    #     def predict(self, inputs):
    #         hidden = self.sigmoid(np.dot(inputs, self.weights[0]) + self.biases[0])
    #         output = self.sigmoid(np.dot(hidden, self.weights[1]) + self.biases[1])
    #         return 1 if output >= 0.5 else 0

    # # XOR Gate
    # X, y = np.array([[0, 0], [0, 1], [1, 0], [1, 1]]), np.array([0, 1, 1, 0])
    # mlp = MLP(input_size=2, hidden_size=2, output_size=1)
    # mlp.train(X, y)
    # print("XOR Gate:")
    # for inputs in X:
    #     print(f"{inputs} -> {mlp.predict(inputs)}")

    # import numpy as np

    # class Perceptron:
    #     def __init__(self, input_size, learning_rate=0.01, epochs=100):
    #         self.weights = np.zeros(input_size + 1)  # +1 for the bias
    #         self.lr = learning_rate
    #         self.epochs = epochs

    #     def predict(self, inputs):
    #         return 1 if np.dot(inputs, self.weights[1:]) + self.weights[0] > 0 else 0

    #     def train(self, X, y):
    #         for _ in range(self.epochs):
    #             for inputs, label in zip(X, y):
    #                 prediction = self.predict(inputs)
    #                 self.weights[1:] += self.lr * (label - prediction) * inputs
    #                 self.weights[0] += self.lr * (label - prediction)

    #     def accuracy(self, X, y):
    #         return np.mean([self.predict(x) == l for x, l in zip(X, y)])


    # class MLP:
    #     def __init__(self, input_size, hidden_size, output_size, lr=0.01, epochs=50000):
    #         self.w1 = np.random.randn(input_size + 1, hidden_size) * 0.1  # +1 for bias
    #         self.w2 = np.random.randn(hidden_size + 1, output_size) * 0.1  # +1 for bias
    #         self.lr = lr
    #         self.epochs = epochs

    #     def sigmoid(self, x):
    #         return 1 / (1 + np.exp(-x))

    #     def forward(self, x):
    #         x = np.insert(x, 0, 1)
    #         a1 = self.sigmoid(np.dot(x, self.w1))
    #         a1 = np.insert(a1, 0, 1)
    #         a2 = self.sigmoid(np.dot(a1, self.w2))
    #         return a1, a2

    #     def backward(self, x, a1, a2, t):
    #         delta2 = (a2 - t) * a2 * (1 - a2)
    #         delta1 = np.dot(delta2, self.w2[1:].T) * a1[1:] * (1 - a1[1:])
    #         self.w2 -= self.lr * np.outer(a1, delta2)
    #         x = np.insert(x, 0, 1)
    #         self.w1 -= self.lr * np.outer(x, delta1)

    #     def train(self, X, y):
    #         for _ in range(self.epochs):
    #             for x, t in zip(X, y):
    #                 a1, a2 = self.forward(x)
    #                 self.backward(x, a1, a2, t)

    #     def predict(self, X):
    #         return np.array([1 if self.forward(x)[1] > 0.5 else 0 for x in X])

    # # AND gate
    # X_and = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    # y_and = np.array([0, 0, 0, 1])
    # p_and = Perceptron(2)
    # p_and.train(X_and, y_and)
    # print("AND:", [p_and.predict(x) for x in X_and])

    # # OR gate
    # X_or = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    # y_or = np.array([0, 1, 1, 1])
    # p_or = Perceptron(2)
    # p_or.train(X_or, y_or)
    # print("OR:", [p_or.predict(x) for x in X_or])

    # # XOR gate
    # X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    # y_xor = np.array([0, 1, 1, 0])
    # mlp_xor = MLP(2, 4, 1)  # 2 inputs, 4 hidden, 1 output
    # mlp_xor.train(X_xor, y_xor)
    # print("XOR:", mlp_xor.predict(X_xor))

    # """# Expt 3 (Implement a basic feedforward neural network using a deep learning framework of your choice.)"""

    # import torch
    # import torch.nn as nn
    # import torch.optim as optim
    # from torch.utils.data import DataLoader
    # from torchvision import datasets, transforms
    # import matplotlib.pyplot as plt

    # # Load dataset and create DataLoader
    # transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
    # trainloader = DataLoader(datasets.MNIST('./data', train=True, download=True, transform=transform), batch_size=64, shuffle=True)
    # testloader = DataLoader(datasets.MNIST('./data', train=False, download=True, transform=transform), batch_size=64, shuffle=False)

    # # Define model, loss, and optimizer
    # class FeedForwardNN(nn.Module):
    #     def __init__(self):
    #         super().__init__()
    #         self.fc1, self.fc2, self.fc3 = nn.Linear(28*28, 128), nn.Linear(128, 64), nn.Linear(64, 10)
    #     def forward(self, x):
    #         return self.fc3(torch.relu(self.fc2(torch.relu(self.fc1(x.view(-1, 28*28))))))

    # model, criterion, optimizer = FeedForwardNN(), nn.CrossEntropyLoss(), optim.Adam(FeedForwardNN().parameters(), lr=0.001)

    # # Training loop
    # for epoch in range(5):
    #     model.train()
    #     total_loss = 0
    #     for images, labels in trainloader:
    #         optimizer.zero_grad()
    #         loss = criterion(model(images), labels)
    #         loss.backward()
    #         optimizer.step()
    #         total_loss += loss.item()
    #     print(f'Epoch {epoch+1}, Loss: {total_loss/len(trainloader):.4f}')

    # # Evaluate
    # model.eval()
    # correct = sum((torch.argmax(model(images), 1) == labels).sum().item() for images, labels in testloader)
    # accuracy = 100 * correct / len(testloader.dataset)
    # print(f'Accuracy: {accuracy:.2f}%')

    # # Visualization
    # images, labels = next(iter(testloader))
    # predicted = torch.argmax(model(images), 1)
    # fig, axes = plt.subplots(1, 10, figsize=(15, 5))
    # for i in range(10):
    #     axes[i].imshow(images[i].squeeze(), cmap='gray')
    #     axes[i].set_title(f'{predicted[i].item()}')
    #     axes[i].axis('off')
    # plt.show()

    # import torch
    # import torch.nn as nn
    # import torch.optim as optim
    # from torch.utils.data import DataLoader
    # from torchvision import datasets, transforms
    # import matplotlib.pyplot as plt

    # # Step 1: Define transformations and load datasets

    # # Transform to normalize the images to a range of (-1, 1)
    # transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])

    # # Load training and test datasets directly from torchvision
    # trainset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
    # testset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)

    # # Create DataLoader for batch processing
    # trainloader = DataLoader(trainset, batch_size=64, shuffle=True)
    # testloader = DataLoader(testset, batch_size=64, shuffle=False)

    # # Step 2: Define the FeedForward Neural Network

    # class FeedForwardNN(nn.Module):
    #     def __init__(self):
    #         super(FeedForwardNN, self).__init__()
    #         # Define a simple fully connected network with ReLU activations
    #         self.fc1 = nn.Linear(28 * 28, 128)  # Input layer (28x28 = 784, flattened)
    #         self.fc2 = nn.Linear(128, 64)       # Hidden layer
    #         self.fc3 = nn.Linear(64, 10)        # Output layer (10 classes: 0-9)

    #     def forward(self, x):
    #         x = x.view(-1, 28 * 28)  # Flatten the input (28x28 pixels)
    #         x = torch.relu(self.fc1(x))  # ReLU activation for the first hidden layer
    #         x = torch.relu(self.fc2(x))  # ReLU activation for the second hidden layer
    #         x = self.fc3(x)  # Output layer (no activation here, we'll use softmax during loss calculation)
    #         return x

    # # Step 3: Initialize Model, Loss Function, and Optimizer

    # model = FeedForwardNN()

    # # Loss function: Cross-Entropy (suitable for multi-class classification)
    # criterion = nn.CrossEntropyLoss()

    # # Optimizer: Adam (works well for most cases)
    # optimizer = optim.Adam(model.parameters(), lr=0.001)

    # # Step 4: Train the Model

    # epochs = 5  # Number of epochs to train

    # for epoch in range(epochs):
    #     running_loss = 0.0
    #     for images, labels in trainloader:
    #         # Zero the gradients
    #         optimizer.zero_grad()

    #         # Forward pass
    #         outputs = model(images)

    #         # Calculate the loss
    #         loss = criterion(outputs, labels)

    #         # Backpropagation
    #         loss.backward()

    #         # Update weights
    #         optimizer.step()

    #         # Track the loss
    #         running_loss += loss.item()

    #     print(f'Epoch [{epoch+1}/{epochs}], Loss: {running_loss / len(trainloader):.4f}')

    # # Step 5: Evaluate the Model

    # correct = 0
    # total = 0

    # # Set the model to evaluation mode and disable gradients
    # model.eval()
    # with torch.no_grad():
    #     for images, labels in testloader:
    #         outputs = model(images)
    #         _, predicted = torch.max(outputs.data, 1)
    #         total += labels.size(0)
    #         correct += (predicted == labels).sum().item()

    # accuracy = 100 * correct / total
    # print(f'Accuracy of the model on the test dataset: {accuracy:.2f}%')

    # # Step 6: Visualize Some Test Results

    # # Get the first batch of test data
    # dataiter = iter(testloader)
    # images, labels = next(dataiter)

    # # Get the model's predictions
    # outputs = model(images)
    # _, predicted = torch.max(outputs, 1)

    # # Plot first 10 images and the predicted labels
    # fig, axes = plt.subplots(1, 10, figsize=(15, 5))
    # for idx in range(10):
    #     axes[idx].imshow(images[idx].numpy().squeeze(), cmap='gray')
    #     axes[idx].set_title(f'Pred: {predicted[idx].item()}')
    #     axes[idx].axis('off')
    # plt.show()

    # import torch
    # import torch.nn as nn
    # import torch.optim as optim
    # from torch.utils.data import DataLoader
    # from torchvision import datasets, transforms
    # import matplotlib.pyplot as plt

    # # datasets
    # transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
    # trainloader = DataLoader(datasets.MNIST('./data', train=True, download=True, transform=transform), batch_size=64, shuffle=True)
    # testloader = DataLoader(datasets.MNIST('./data', train=False, download=True, transform=transform), batch_size=64, shuffle=False)

    # # Model definition
    # class FeedForwardNN(nn.Module):
    #     def __init__(self):
    #         super().__init__()
    #         self.fc1, self.fc2, self.fc3 = nn.Linear(28*28, 128), nn.Linear(128, 64), nn.Linear(64, 10)
    #     def forward(self, x):
    #         return self.fc3(torch.relu(self.fc2(torch.relu(self.fc1(x.view(-1, 28*28))))))

    # # Initialize model, loss, and optimizer
    # model = FeedForwardNN()
    # criterion = nn.CrossEntropyLoss()
    # optimizer = optim.Adam(model.parameters(), lr=0.001)

    # # Training loop
    # for epoch in range(5):
    #     model.train()
    #     running_loss = sum(criterion(model(images), labels).item() for images, labels in trainloader)
    #     print(f'Epoch {epoch+1}, Loss: {running_loss / len(trainloader):.4f}')

    # # Evaluate the model
    # model.eval()
    # correct = sum((torch.argmax(model(images), 1) == labels).sum().item() for images, labels in testloader)
    # accuracy = 100 * correct / len(testloader.dataset)
    # print(f'Accuracy: {accuracy:.2f}%')

    # # Visualize predictions
    # images, labels = next(iter(testloader))
    # predicted = torch.argmax(model(images), 1)
    # fig, axes = plt.subplots(1, 10, figsize=(15, 5))
    # for i in range(10):
    #     axes[i].imshow(images[i].squeeze(), cmap='gray')
    #     axes[i].set_title(f'{predicted[i].item()}')
    #     axes[i].axis('off')
    # plt.show()

    # # iris dataset
    # import torch
    # import torch.nn as nn
    # import torch.optim as optim
    # from sklearn import datasets
    # from sklearn.model_selection import train_test_split
    # from sklearn.preprocessing import StandardScaler
    # from sklearn.metrics import accuracy_score
    # import numpy as np

    # # Step 1: Load the Iris dataset
    # iris = datasets.load_iris()
    # X = iris.data
    # y = iris.target

    # # Step 2: Preprocess the data (standardize the features)
    # scaler = StandardScaler()
    # X_scaled = scaler.fit_transform(X)

    # # Step 3: Split the dataset into training and testing sets
    # X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # # Step 4: Convert the data into PyTorch tensors
    # X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    # X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    # y_train_tensor = torch.tensor(y_train, dtype=torch.long)
    # y_test_tensor = torch.tensor(y_test, dtype=torch.long)

    # # Step 5: Define a simple feedforward neural network model
    # class FeedforwardNN(nn.Module):
    #     def __init__(self):
    #         super(FeedforwardNN, self).__init__()
    #         self.fc1 = nn.Linear(4, 10)  # 4 input features, 10 hidden units
    #         self.fc2 = nn.Linear(10, 3)  # 3 output classes (Setosa, Versicolor, Virginica)
    #         self.relu = nn.ReLU()

    #     def forward(self, x):
    #         x = self.relu(self.fc1(x))  # Apply ReLU after the first layer
    #         x = self.fc2(x)  # Output layer
    #         return x

    # # Step 6: Initialize the model, loss function, and optimizer
    # model = FeedforwardNN()
    # criterion = nn.CrossEntropyLoss()  # For multi-class classification
    # optimizer = optim.SGD(model.parameters(), lr=0.01)

    # # Step 7: Train the model
    # num_epochs = 100
    # for epoch in range(num_epochs):
    #     # Forward pass
    #     outputs = model(X_train_tensor)
    #     loss = criterion(outputs, y_train_tensor)

    #     # Backward pass and optimization
    #     optimizer.zero_grad()  # Zero the gradients
    #     loss.backward()        # Backpropagation
    #     optimizer.step()       # Optimize the weights

    #     if (epoch + 1) % 10 == 0:
    #         print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

    # # Step 8: Evaluate the model
    # with torch.no_grad():
    #     # Test the model
    #     outputs = model(X_test_tensor)
    #     _, predicted = torch.max(outputs, 1)
    #     accuracy = accuracy_score(y_test, predicted.numpy())
    #     print(f'Accuracy on test set: {accuracy * 100:.2f}%')

    # import torch
    # import torch.nn as nn
    # import torch.optim as optim
    # import torchvision
    # import torchvision.transforms as transforms
    # from torch.utils.data import DataLoader
    # from sklearn.metrics import accuracy_score

    # # Step 1: Define transformations (normalizing the dataset)
    # transform = transforms.Compose([
    #     transforms.ToTensor(),
    #     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))  # Normalize RGB channels
    # ])

    # # Step 2: Load CIFAR-10 dataset
    # trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
    # testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)

    # trainloader = DataLoader(trainset, batch_size=64, shuffle=True)
    # testloader = DataLoader(testset, batch_size=64, shuffle=False)

    # # Step 3: Define the Feedforward Neural Network Model
    # class FeedforwardNN(nn.Module):
    #     def __init__(self):
    #         super(FeedforwardNN, self).__init__()
    #         self.fc1 = nn.Linear(3 * 32 * 32, 500)  # 3 channels x 32x32 image size
    #         self.fc2 = nn.Linear(500, 10)  # 10 classes (CIFAR-10)

    #     def forward(self, x):
    #         x = x.view(-1, 3 * 32 * 32)  # Flatten the image to a vector
    #         x = torch.relu(self.fc1(x))  # Apply ReLU activation after the first layer
    #         x = self.fc2(x)  # Output layer
    #         return x

    # # Step 4: Initialize the model, loss function, and optimizer
    # model = FeedforwardNN()
    # criterion = nn.CrossEntropyLoss()  # For multi-class classification
    # optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

    # # Step 5: Train the model
    # num_epochs = 10
    # for epoch in range(num_epochs):
    #     running_loss = 0.0
    #     for inputs, labels in trainloader:
    #         # Zero the parameter gradients
    #         optimizer.zero_grad()

    #         # Forward pass
    #         outputs = model(inputs)
    #         loss = criterion(outputs, labels)

    #         # Backward pass and optimization
    #         loss.backward()
    #         optimizer.step()

    #         running_loss += loss.item()

    #     print(f"Epoch [{epoch + 1}/{num_epochs}], Loss: {running_loss/len(trainloader):.4f}")

    # # Step 6: Evaluate the model on the test set
    # correct = 0
    # total = 0
    # with torch.no_grad():
    #     for inputs, labels in testloader:
    #         outputs = model(inputs)
    #         _, predicted = torch.max(outputs, 1)
    #         total += labels.size(0)
    #         correct += (predicted == labels).sum().item()

    # accuracy = 100 * correct / total
    # print(f"Accuracy on the test set: {accuracy:.2f}%")

    # """# Expt 4 (Design and implement a fully connected deep neural network with at least 2 hidden layers for a classification application.)"""

    # import torch
    # import torch.nn as nn
    # import torch.optim as optim
    # from torch.utils.data import DataLoader
    # from torchvision import datasets, transforms
    # import matplotlib.pyplot as plt

    # # Step 1: Load and preprocess the MNIST dataset
    # transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])

    # trainloader = DataLoader(datasets.MNIST('./data', train=True, download=True, transform=transform), batch_size=64, shuffle=True)
    # testloader = DataLoader(datasets.MNIST('./data', train=False, download=True, transform=transform), batch_size=64, shuffle=False)

    # # Step 2: Define the Deep Neural Network model with 2 hidden layers
    # class DeepNN(nn.Module):
    #     def __init__(self):
    #         super(DeepNN, self).__init__()
    #         self.fc1 = nn.Linear(28*28, 512)  # First hidden layer (784 -> 512)
    #         self.fc2 = nn.Linear(512, 256)    # Second hidden layer (512 -> 256)
    #         self.fc3 = nn.Linear(256, 10)     # Output layer (256 -> 10, for 10 digits)

    #     def forward(self, x):
    #         x = x.view(-1, 28*28)  # Flatten the input
    #         x = torch.relu(self.fc1(x))  # Apply ReLU activation
    #         x = torch.relu(self.fc2(x))  # Apply ReLU activation
    #         x = self.fc3(x)  # Output layer (no activation, we'll use softmax during loss calculation)
    #         return x

    # # Step 3: Initialize model, loss function, and optimizer
    # model = DeepNN()
    # criterion = nn.CrossEntropyLoss()  # Cross-entropy loss for multi-class classification
    # optimizer = optim.Adam(model.parameters(), lr=0.001)  # Adam optimizer

    # # Step 4: Train the model
    # epochs = 5
    # for epoch in range(epochs):
    #     model.train()
    #     running_loss = 0.0
    #     for images, labels in trainloader:
    #         optimizer.zero_grad()  # Zero the gradients

    #         # Forward pass
    #         outputs = model(images)

    #         # Calculate the loss
    #         loss = criterion(outputs, labels)

    #         # Backpropagation
    #         loss.backward()

    #         # Update weights
    #         optimizer.step()

    #         # Track the loss
    #         running_loss += loss.item()

    #     print(f'Epoch {epoch+1}/{epochs}, Loss: {running_loss / len(trainloader):.4f}')

    # # Step 5: Evaluate the model
    # model.eval()  # Set the model to evaluation mode
    # correct = 0
    # total = 0
    # with torch.no_grad():  # Disable gradient calculation
    #     for images, labels in testloader:
    #         outputs = model(images)
    #         _, predicted = torch.max(outputs.data, 1)  # Get the predicted class
    #         total += labels.size(0)
    #         correct += (predicted == labels).sum().item()

    # accuracy = 100 * correct / total
    # print(f'Accuracy of the model on the test dataset: {accuracy:.2f}%')

    # # Step 6: Visualize predictions
    # images, labels = next(iter(testloader))
    # outputs = model(images)
    # _, predicted = torch.max(outputs, 1)

    # # Plot the first 10 images with predicted labels
    # fig, axes = plt.subplots(1, 10, figsize=(15, 5))
    # for i in range(10):
    #     axes[i].imshow(images[i].squeeze(), cmap='gray')
    #     axes[i].set_title(f'{predicted[i].item()}')
    #     axes[i].axis('off')
    # plt.show()

    # import torch
    # import torch.nn as nn
    # import torch.optim as optim
    # from torch.utils.data import DataLoader
    # from torchvision import datasets, transforms
    # import matplotlib.pyplot as plt

    # # Step 1: Load and preprocess the CIFAR-10 dataset
    # transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    # trainloader = DataLoader(datasets.CIFAR10('./data', train=True, download=True, transform=transform), batch_size=64, shuffle=True)
    # testloader = DataLoader(datasets.CIFAR10('./data', train=False, download=True, transform=transform), batch_size=64, shuffle=False)

    # # Step 2: Define the Deep Neural Network model with 2 hidden layers
    # class DeepNN(nn.Module):
    #     def __init__(self):
    #         super(DeepNN, self).__init__()
    #         self.fc1 = nn.Linear(3*32*32, 1024)  # First hidden layer (3 channels x 32x32 pixels -> 1024 neurons)
    #         self.fc2 = nn.Linear(1024, 512)       # Second hidden layer (1024 -> 512 neurons)
    #         self.fc3 = nn.Linear(512, 10)         # Output layer (512 -> 10 classes)

    #     def forward(self, x):
    #         x = x.view(-1, 3*32*32)  # Flatten the input (3 channels x 32x32 pixels)
    #         x = torch.relu(self.fc1(x))  # Apply ReLU activation for the first hidden layer
    #         x = torch.relu(self.fc2(x))  # Apply ReLU activation for the second hidden layer
    #         x = self.fc3(x)  # Output layer (no activation, we'll use softmax during loss calculation)
    #         return x

    # # Step 3: Initialize model, loss function, and optimizer
    # model = DeepNN()
    # criterion = nn.CrossEntropyLoss()  # Cross-entropy loss for multi-class classification
    # optimizer = optim.Adam(model.parameters(), lr=0.001)  # Adam optimizer

    # # Step 4: Train the model
    # epochs = 5
    # for epoch in range(epochs):
    #     model.train()
    #     running_loss = 0.0
    #     for images, labels in trainloader:
    #         optimizer.zero_grad()  # Zero the gradients

    #         # Forward pass
    #         outputs = model(images)

    #         # Calculate the loss
    #         loss = criterion(outputs, labels)

    #         # Backpropagation
    #         loss.backward()

    #         # Update weights
    #         optimizer.step()

    #         # Track the loss
    #         running_loss += loss.item()

    #     print(f'Epoch {epoch+1}/{epochs}, Loss: {running_loss / len(trainloader):.4f}')

    # # Step 5: Evaluate the model
    # model.eval()  # Set the model to evaluation mode
    # correct = 0
    # total = 0
    # with torch.no_grad():  # Disable gradient calculation
    #     for images, labels in testloader:
    #         outputs = model(images)
    #         _, predicted = torch.max(outputs.data, 1)  # Get the predicted class
    #         total += labels.size(0)
    #         correct += (predicted == labels).sum().item()

    # accuracy = 100 * correct / total
    # print(f'Accuracy of the model on the test dataset: {accuracy:.2f}%')

    # # Step 6: Visualize predictions
    # images, labels = next(iter(testloader))
    # outputs = model(images)
    # _, predicted = torch.max(outputs, 1)

    # # Plot the first 10 images with predicted labels
    # fig, axes = plt.subplots(1, 10, figsize=(15, 5))
    # for i in range(10):
    #     axes[i].imshow(images[i].permute(1, 2, 0) / 2 + 0.5)  # Rescale the image from [-1, 1] to [0, 1]
    #     axes[i].set_title(f'{predicted[i].item()}')
    #     axes[i].axis('off')
    # plt.show()

    # import torch
    # import torch.nn as nn
    # import torch.optim as optim
    # from torch.utils.data import DataLoader
    # from torchvision import datasets, transforms
    # import matplotlib.pyplot as plt

    # transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    # trainloader = DataLoader(datasets.CIFAR10('./data', train=True, download=True, transform=transform), batch_size=64, shuffle=True)
    # testloader = DataLoader(datasets.CIFAR10('./data', train=False, download=True, transform=transform), batch_size=64, shuffle=False)

    # class DeepNN(nn.Module):
    #     def __init__(self):
    #         super(DeepNN, self).__init__()
    #         self.fc1 = nn.Linear(3*32*32, 1024)
    #         self.fc2 = nn.Linear(1024, 512)
    #         self.fc3 = nn.Linear(512, 10)

    #     def forward(self, x):
    #         x = x.view(-1, 3*32*32)
    #         x = torch.relu(self.fc1(x))
    #         x = torch.relu(self.fc2(x))
    #         x = self.fc3(x)
    #         return x

    # model = DeepNN()
    # criterion = nn.CrossEntropyLoss()
    # optimizer = optim.Adam(model.parameters(), lr=0.001)

    # epochs = 5
    # for epoch in range(epochs):
    #     model.train()
    #     running_loss = 0.0
    #     for images, labels in trainloader:
    #         optimizer.zero_grad()
    #         outputs = model(images)
    #         loss = criterion(outputs, labels)
    #         loss.backward()
    #         optimizer.step()
    #         running_loss += loss.item()

    #     print(f'Epoch {epoch+1}/{epochs}, Loss: {running_loss / len(trainloader):.4f}')

    # model.eval()
    # correct = 0
    # total = 0
    # with torch.no_grad():
    #     for images, labels in testloader:
    #         outputs = model(images)
    #         _, predicted = torch.max(outputs.data, 1)
    #         total += labels.size(0)
    #         correct += (predicted == labels).sum().item()

    # accuracy = 100 * correct / total
    # print(f'Accuracy of the model on the test dataset: {accuracy:.2f}%')

    # images, labels = next(iter(testloader))
    # outputs = model(images)
    # _, predicted = torch.max(outputs, 1)

    # fig, axes = plt.subplots(1, 10, figsize=(15, 5))
    # for i in range(10):
    #     axes[i].imshow(images[i].permute(1, 2, 0) / 2 + 0.5)
    #     axes[i].set_title(f'{predicted[i].item()}')
    #     axes[i].axis('off')
    # plt.show()

    # import torch
    # import torch.nn as nn
    # import torch.optim as optim
    # from torch.utils.data import DataLoader
    # from torchvision import datasets, transforms
    # import matplotlib.pyplot as plt

    # # Load and preprocess the MNIST dataset
    # transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
    # trainloader = DataLoader(datasets.MNIST('./data', train=True, download=True, transform=transform), batch_size=64, shuffle=True)
    # testloader = DataLoader(datasets.MNIST('./data', train=False, download=True, transform=transform), batch_size=64)

    # # Define the model with 2 hidden layers
    # class DeepNN(nn.Module):
    #     def __init__(self):
    #         super().__init__()
    #         self.fc1, self.fc2, self.fc3 = nn.Linear(28*28, 512), nn.Linear(512, 256), nn.Linear(256, 10)
    #     def forward(self, x):
    #         x = x.view(-1, 28*28)
    #         x = torch.relu(self.fc1(x))
    #         x = torch.relu(self.fc2(x))
    #         return self.fc3(x)

    # # Initialize model, loss, and optimizer
    # model = DeepNN()
    # criterion, optimizer = nn.CrossEntropyLoss(), optim.Adam(model.parameters(), lr=0.001)

    # # Train the model
    # for epoch in range(5):
    #     model.train()
    #     running_loss = sum(criterion(model(images), labels).item() for images, labels in trainloader)
    #     print(f'Epoch {epoch+1}, Loss: {running_loss / len(trainloader):.4f}')

    # # Evaluate the model
    # model.eval()
    # correct = sum((torch.argmax(model(images), 1) == labels).sum().item() for images, labels in testloader)
    # print(f'Accuracy: {100 * correct / len(testloader.dataset):.2f}%')

    # # Visualize predictions
    # images, labels = next(iter(testloader))
    # outputs = model(images)
    # _, predicted = torch.max(outputs, 1)
    # fig, axes = plt.subplots(1, 10, figsize=(15, 5))
    # for i in range(10):
    #     axes[i].imshow(images[i].squeeze(), cmap='gray')
    #     axes[i].set_title(f'{predicted[i].item()}')
    #     axes[i].axis('off')
    # plt.show()

    # import torch
    # import torch.nn as nn
    # import torch.optim as optim
    # from torch.utils.data import DataLoader
    # from torchvision import datasets, transforms
    # import matplotlib.pyplot as plt

    # # Load and preprocess the MNIST dataset
    # transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
    # trainloader = DataLoader(datasets.MNIST('./data', train=True, download=True, transform=transform), batch_size=64, shuffle=True)
    # testloader = DataLoader(datasets.MNIST('./data', train=False, download=True, transform=transform), batch_size=64)

    # # Define the model with 4 hidden layers
    # class DeepNN(nn.Module):
    #     def __init__(self):
    #         super().__init__()
    #         self.fc1, self.fc2, self.fc3, self.fc4, self.fc5 = nn.Linear(28*28, 1024), nn.Linear(1024, 512), nn.Linear(512, 256), nn.Linear(256, 128), nn.Linear(128, 10)
    #     def forward(self, x):
    #         x = x.view(-1, 28*28)
    #         x = torch.relu(self.fc1(x))
    #         x = torch.relu(self.fc2(x))
    #         x = torch.relu(self.fc3(x))
    #         x = torch.relu(self.fc4(x))
    #         return self.fc5(x)

    # # Initialize model, loss, and optimizer
    # model = DeepNN()
    # criterion, optimizer = nn.CrossEntropyLoss(), optim.Adam(model.parameters(), lr=0.001)

    # # Train the model
    # for epoch in range(5):
    #     model.train()
    #     running_loss = sum(criterion(model(images), labels).item() for images, labels in trainloader)
    #     print(f'Epoch {epoch+1}, Loss: {running_loss / len(trainloader):.4f}')

    # # Evaluate the model
    # model.eval()
    # correct = sum((torch.argmax(model(images), 1) == labels).sum().item() for images, labels in testloader)
    # print(f'Accuracy: {100 * correct / len(testloader.dataset):.2f}%')

    # # Class names (for MNIST, it's just digits 0-9)
    # class_names = [str(i) for i in range(10)]

    # # Visualize predictions
    # images, labels = next(iter(testloader))
    # outputs = model(images)
    # _, predicted = torch.max(outputs, 1)

    # fig, axes = plt.subplots(1, 10, figsize=(15, 5))
    # for i in range(10):
    #     axes[i].imshow(images[i].squeeze(), cmap='gray')
    #     axes[i].set_title(f'{class_names[predicted[i].item()]} ({predicted[i].item()})')
    #     axes[i].axis('off')
    # plt.show()

    # """# Expt 5 (Design the architecture and implement the autoencoder model for Image Compression.)"""

    # import torch
    # import torch.nn as nn
    # import torch.optim as optim
    # from torchvision import datasets, transforms
    # from torch.utils.data import DataLoader
    # import matplotlib.pyplot as plt

    # # Define the autoencoder architecture
    # class Autoencoder(nn.Module):
    #     def __init__(self, latent_dim=32):
    #         super(Autoencoder, self).__init__()
    #         # Encoder
    #         self.encoder = nn.Sequential(
    #             nn.Linear(28 * 28, 512),
    #             nn.ReLU(),
    #             nn.Linear(512, 256),
    #             nn.ReLU(),
    #             nn.Linear(256, latent_dim)
    #         )
    #         # Decoder
    #         self.decoder = nn.Sequential(
    #             nn.Linear(latent_dim, 256),
    #             nn.ReLU(),
    #             nn.Linear(256, 512),
    #             nn.ReLU(),
    #             nn.Linear(512, 28 * 28),
    #             nn.Tanh()  # Output should be in the range [-1, 1]
    #         )

    #     def forward(self, x):
    #         encoded = self.encoder(x)
    #         decoded = self.decoder(encoded)
    #         return decoded

    # # Load MNIST dataset
    # transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
    # train_dataset = datasets.MNIST('./data', train=True, download=True, transform=transform)
    # train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

    # # Initialize the autoencoder, loss function, and optimizer
    # model = Autoencoder()
    # criterion = nn.MSELoss()
    # optimizer = optim.Adam(model.parameters(), lr=1e-3)

    # # Training loop
    # num_epochs = 10
    # device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # model.to(device)

    # for epoch in range(num_epochs):
    #     for data in train_loader:
    #         img, _ = data
    #         img = img.view(img.size(0), -1).to(device)
    #         optimizer.zero_grad()
    #         output = model(img)
    #         loss = criterion(output, img)
    #         loss.backward()
    #         optimizer.step()
    #     print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')


    # # Test the model
    # with torch.no_grad():
    #     # Take a batch of images from the test data
    #     images, labels = next(iter(testloader))
    #     images = images.view(images.size(0), -1).to(device)  # Flatten the images
    #     outputs = model(images)

    #     # Visualize original and reconstructed images
    #     fig, axes = plt.subplots(2, 10, figsize=(15, 5))
    #     for i in range(10):
    #         axes[0, i].imshow(images[i].cpu().view(28, 28).numpy(), cmap='gray')
    #         axes[0, i].set_title('Original')
    #         axes[0, i].axis('off')
    #         axes[1, i].imshow(outputs[i].cpu().view(28, 28).numpy(), cmap='gray')
    #         axes[1, i].set_title('Recons')
    #         axes[1, i].axis('off')
    # plt.show()

    # """_________________________________________________________"""

    # import numpy as np
    # import matplotlib.pyplot as plt
    # import tensorflow as tf
    # from tensorflow.keras.datasets import cifar10
    # from tensorflow.keras.models import Model
    # from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D

    # # Load CIFAR-10 dataset
    # (x_train, _), (x_test, _) = cifar10.load_data()

    # # Normalize the images to the range [0, 1]
    # x_train = x_train.astype('float32') / 255.0
    # x_test = x_test.astype('float32') / 255.0

    # # Define the size of the encoded representations
    # encoding_dim = 32

    # # Input placeholder
    # input_img = Input(shape=(32, 32, 3))

    # # Encoder
    # x = Conv2D(32, (3, 3), activation='relu', padding='same')(input_img)
    # x = MaxPooling2D((2, 2), padding='same')(x)
    # x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    # x = MaxPooling2D((2, 2), padding='same')(x)
    # encoded = Conv2D(encoding_dim, (3, 3), activation='relu', padding='same')(x)

    # # Decoder
    # x = Conv2D(64, (3, 3), activation='relu', padding='same')(encoded)
    # x = UpSampling2D((2, 2))(x)
    # x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
    # x = UpSampling2D((2, 2))(x)
    # decoded = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)

    # # Autoencoder model
    # autoencoder = Model(input_img, decoded)
    # autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

    # # Train the autoencoder
    # autoencoder.fit(x_train, x_train,
    #                 epochs=50,
    #                 batch_size=256,
    #                 shuffle=True,
    #                 validation_data=(x_test, x_test))


    # # Encode and decode some images from the test set
    # decoded_imgs = autoencoder.predict(x_test)

    # # Plot original and reconstructed images
    # n = 10
    # plt.figure(figsize=(20, 4))
    # for i in range(n):
    #     # Display original
    #     ax = plt.subplot(2, n, i + 1)
    #     plt.imshow(x_test[i])
    #     ax.get_xaxis().set_visible(False)
    #     ax.get_yaxis().set_visible(False)

    #     # Display reconstruction
    #     ax = plt.subplot(2, n, i + 1 + n)
    #     plt.imshow(decoded_imgs[i])
    #     ax.get_xaxis().set_visible(False)
    #     ax.get_yaxis().set_visible(False)
    # plt.show()

    # """# Expt 6 (Design the architecture and implement the autoencoder model for Image denoising)"""

    # !pip install tensorflow-datasets

    # import numpy as np
    # import matplotlib.pyplot as plt
    # import tensorflow as tf
    # import tensorflow_datasets as tfds
    # from tensorflow.keras.models import Model
    # from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D


    # # Load STL-10 dataset
    # def preprocess(data):
    #     image = data['image']
    #     image = tf.cast(image, tf.float32) / 255.0
    #     return image

    # # Load the dataset
    # dataset, metadata = tfds.load('stl10', split='train', with_info=True, as_supervised=False)
    # dataset = dataset.map(preprocess)

    # # Convert to numpy arrays
    # x_train = np.array([example.numpy() for example in dataset])

    # # Add noise to the images
    # noise_factor = 0.2
    # x_train_noisy = x_train + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=x_train.shape)
    # x_train_noisy = np.clip(x_train_noisy, 0., 1.)


    # # Input placeholder
    # input_img = Input(shape=(96, 96, 3))

    # # Encoder
    # x = Conv2D(32, (3, 3), activation='relu', padding='same')(input_img)
    # x = MaxPooling2D((2, 2), padding='same')(x)
    # x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    # encoded = MaxPooling2D((2, 2), padding='same')(x)

    # # Decoder
    # x = Conv2D(64, (3, 3), activation='relu', padding='same')(encoded)
    # x = UpSampling2D((2, 2))(x)
    # x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
    # x = UpSampling2D((2, 2))(x)
    # decoded = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)

    # # Autoencoder model
    # autoencoder = Model(input_img, decoded)
    # autoencoder.compile(optimizer='adam', loss='binary_crossentropy')


    # # Train the autoencoder
    # autoencoder.fit(x_train_noisy, x_train,
    #                 epochs=50,
    #                 batch_size=256,
    #                 shuffle=True)


    # # Encode and decode some images from the test set
    # decoded_imgs = autoencoder.predict(x_train_noisy)

    # # Plot noisy and denoised images
    # n = 10
    # plt.figure(figsize=(20, 6))
    # for i in range(n):
    #     # Display noisy
    #     ax = plt.subplot(3, n, i + 1)
    #     plt.imshow(x_train_noisy[i])
    #     ax.get_xaxis().set_visible(False)
    #     ax.get_yaxis().set_visible(False)

    #     # Display original
    #     ax = plt.subplot(3, n, i + 1 + n)
    #     plt.imshow(x_train[i])
    #     ax.get_xaxis().set_visible(False)
    #     ax.get_yaxis().set_visible(False)

    #     # Display reconstruction
    #     ax = plt.subplot(3, n, i + 1 + 2*n)
    #     plt.imshow(decoded_imgs[i])
    #     ax.get_xaxis().set_visible(False)
    #     ax.get_yaxis().set_visible(False)
    # plt.show()

    # import tensorflow as tf
    # from tensorflow.keras import layers, Model
    # import numpy as np
    # import matplotlib.pyplot as plt

    # def create_autoencoder(input_shape=(28, 28, 1)): #Corrected input shape
    #     """Creates an autoencoder for image denoising."""

    #     input_img = layers.Input(shape=input_shape)

    #     # Encoder
    #     x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(input_img)
    #     x = layers.MaxPooling2D((2, 2), padding='same')(x)
    #     x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    #     x = layers.MaxPooling2D((2, 2), padding='same')(x)
    #     x = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
    #     encoded = layers.MaxPooling2D((2, 2), padding='same')(x)

    #     # Decoder
    #     x = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(encoded)
    #     x = layers.UpSampling2D((2, 2))(x)
    #     x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    #     x = layers.UpSampling2D((2, 2))(x)
    #     x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(x)
    #     x = layers.UpSampling2D((2, 2))(x)
    #     decoded = layers.Conv2D(input_shape[2], (3, 3), activation='sigmoid', padding='same')(x)

    #     # Cropping to match input dimensions
    #     decoded = layers.Cropping2D(cropping=((2, 2), (2, 2)))(decoded) # Cropping from 32x32 to 28x28

    #     autoencoder = Model(input_img, decoded)
    #     return autoencoder


    # def add_noise(images, noise_factor=0.2):
    #     """Adds Gaussian noise to images."""
    #     noisy_images = images + noise_factor * tf.random.normal(shape=tf.shape(images))
    #     noisy_images = tf.clip_by_value(noisy_images, 0., 1.)
    #     return noisy_images

    # # Example Usage:
    # (x_train, _), (x_test, _) = tf.keras.datasets.mnist.load_data() #example dataset.

    # x_train = x_train.astype('float32') / 255.
    # x_test = x_test.astype('float32') / 255.

    # x_train = np.reshape(x_train, (len(x_train), 28, 28, 1))
    # x_test = np.reshape(x_test, (len(x_test), 28, 28, 1))

    # noise_factor = 0.2
    # x_train_noisy = add_noise(x_train, noise_factor)
    # x_test_noisy = add_noise(x_test, noise_factor)

    # autoencoder = create_autoencoder((28, 28, 1))
    # autoencoder.compile(optimizer='adam', loss='mse')

    # autoencoder.fit(x_train_noisy, x_train, epochs=50, batch_size=128, shuffle=True, validation_data=(x_test_noisy, x_test))

    # # Visualize Results (Example)
    # decoded_imgs = autoencoder.predict(x_test_noisy)

    # n = 10
    # plt.figure(figsize=(20, 4))
    # for i in range(n):
    #     # Original Noisy Images
    #     ax = plt.subplot(2, n, i + 1)
    #     plt.imshow(tf.squeeze(x_test_noisy[i]))
    #     plt.gray()
    #     ax.get_xaxis().set_visible(False)
    #     ax.get_yaxis().set_visible(False)

    #     # Denoised Images
    #     ax = plt.subplot(2, n, i + 1 + n)
    #     plt.imshow(tf.squeeze(decoded_imgs[i]))
    #     plt.gray()
    #     ax.get_xaxis().set_visible(False)
    #     ax.get_yaxis().set_visible(False)
    # plt.show()

    # # prompt: Design the architecture and implement the autoencoder model for Image
    # # denoising, aalso use any image dataset to show the results

    # import numpy as np
    # import matplotlib.pyplot as plt
    # import tensorflow as tf
    # from tensorflow.keras import layers, Model

    # # Define the autoencoder architecture
    # def create_autoencoder(input_shape=(28, 28, 1)):
    #     input_img = layers.Input(shape=input_shape)

    #     # Encoder
    #     x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(input_img)
    #     x = layers.MaxPooling2D((2, 2), padding='same')(x)
    #     x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    #     encoded = layers.MaxPooling2D((2, 2), padding='same')(x)

    #     # Decoder
    #     x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(encoded)
    #     x = layers.UpSampling2D((2, 2))(x)
    #     x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(x)
    #     x = layers.UpSampling2D((2, 2))(x)
    #     decoded = layers.Conv2D(1, (3, 3), activation='sigmoid', padding='same')(x)

    #     autoencoder = Model(input_img, decoded)
    #     return autoencoder

    # def add_noise(images, noise_factor=0.2):
    #     noisy_images = images + noise_factor * tf.random.normal(shape=tf.shape(images))
    #     noisy_images = tf.clip_by_value(noisy_images, 0., 1.)
    #     return noisy_images

    # # Load MNIST dataset
    # (x_train, _), (x_test, _) = tf.keras.datasets.mnist.load_data()

    # x_train = x_train.astype('float32') / 255.
    # x_test = x_test.astype('float32') / 255.
    # x_train = np.reshape(x_train, (len(x_train), 28, 28, 1))
    # x_test = np.reshape(x_test, (len(x_test), 28, 28, 1))

    # noise_factor = 0.2
    # x_train_noisy = add_noise(x_train, noise_factor)
    # x_test_noisy = add_noise(x_test, noise_factor)

    # # Create and compile the autoencoder
    # autoencoder = create_autoencoder()
    # autoencoder.compile(optimizer='adam', loss='mse')

    # # Train the autoencoder
    # autoencoder.fit(x_train_noisy, x_train, epochs=10, batch_size=128, shuffle=True, validation_data=(x_test_noisy, x_test))

    # # Predict on noisy test data
    # decoded_imgs = autoencoder.predict(x_test_noisy)

    # # Visualize results
    # n = 10
    # plt.figure(figsize=(20, 4))
    # for i in range(n):
    #     ax = plt.subplot(2, n, i + 1)
    #     plt.imshow(tf.squeeze(x_test_noisy[i]))
    #     plt.gray()
    #     ax.get_xaxis().set_visible(False)
    #     ax.get_yaxis().set_visible(False)

    #     ax = plt.subplot(2, n, i + 1 + n)
    #     plt.imshow(tf.squeeze(decoded_imgs[i]))
    #     plt.gray()
    #     ax.get_xaxis().set_visible(False)
    #     ax.get_yaxis().set_visible(False)
    # plt.show()

    # import torch
    # import torch.nn as nn
    # import torch.optim as optim
    # from torchvision import datasets, transforms
    # from torch.utils.data import DataLoader
    # import matplotlib.pyplot as plt

    # # Define the autoencoder architecture
    # class Autoencoder(nn.Module):
    #     def __init__(self, latent_dim=32):  # Adjust latent_dim as needed
    #         super(Autoencoder, self).__init__()
    #         # Encoder
    #         self.encoder = nn.Sequential(
    #             nn.Linear(28 * 28, 512),  # Adjust input size if needed
    #             nn.ReLU(),
    #             nn.Linear(512, 256),
    #             nn.ReLU(),
    #             nn.Linear(256, latent_dim)  # Adjust latent_dim as needed
    #         )
    #         # Decoder
    #         self.decoder = nn.Sequential(
    #             nn.Linear(latent_dim, 256),  # Adjust latent_dim as needed
    #             nn.ReLU(),
    #             nn.Linear(256, 512),
    #             nn.ReLU(),
    #             nn.Linear(512, 28 * 28),  # Adjust output size if needed
    #             nn.Tanh()  # Output should be in the range [-1, 1]
    #         )

    #     def forward(self, x):
    #         encoded = self.encoder(x)
    #         decoded = self.decoder(encoded)
    #         return decoded

    # # Load and preprocess the Fashion-MNIST dataset
    # transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])

    # train_dataset = datasets.FashionMNIST('./data', train=True, download=True, transform=transform)
    # train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

    # test_dataset = datasets.FashionMNIST('./data', train=False, download=True, transform=transform)
    # test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

    # # Initialize the autoencoder, loss function, and optimizer
    # model = Autoencoder()
    # criterion = nn.MSELoss()
    # optimizer = optim.Adam(model.parameters(), lr=1e-3)

    # # Training loop
    # num_epochs = 100  # Adjust as needed
    # device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # model.to(device)

    # for epoch in range(num_epochs):
    #     for data in train_loader:
    #         img, _ = data
    #         img = img.view(img.size(0), -1).to(device)  # Flatten the images
    #         optimizer.zero_grad()
    #         output = model(img)
    #         loss = criterion(output, img)
    #         loss.backward()
    #         optimizer.step()
    #     print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

    # # Test the model and visualize results
    # with torch.no_grad():
    #     images, labels = next(iter(test_loader))
    #     images = images.view(images.size(0), -1).to(device)  # Flatten the images
    #     outputs = model(images)

    #     # Class names for Fashion-MNIST
    #     class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Shirt', 'Dress', 'Coat',
    #                 'Sandal', 'Sneaker', 'Bag', 'Ankle boot']

    #     # Visualize original and reconstructed images
    #     fig, axes = plt.subplots(2, 10, figsize=(15, 5))
    #     for i in range(10):
    #         axes[0, i].imshow(images[i].cpu().view(28, 28).numpy(), cmap='gray')
    #         axes[0, i].set_title(f'Og - {class_names[labels[i]]}')
    #         axes[0, i].axis('off')
    #         axes[1, i].imshow(outputs[i].cpu().view(28, 28).numpy(), cmap='gray')
    #         axes[1, i].set_title('Recons')
    #         axes[1, i].axis('off')
    # plt.show()

    # """# Expt 7: Develop an RNN-based model for sentiment analysis and apply it to a text dataset."""

    # !pip install datasets

    # import pandas as pd
    # import numpy as np
    # import re
    # from nltk.corpus import stopwords
    # from tensorflow.keras.preprocessing.text import Tokenizer
    # from tensorflow.keras.preprocessing.sequence import pad_sequences
    # from sklearn.model_selection import train_test_split
    # from tensorflow.keras.models import Sequential
    # from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
    # import matplotlib.pyplot as plt
    # from datasets import load_dataset

    # # Download stopwords if not already downloaded
    # import nltk
    # try:
    #     stopwords.words('english')
    # except LookupError:
    #     nltk.download('stopwords')

    # # --- Data Loading and Preprocessing using Hugging Face datasets ---
    # try:
    #     dataset = load_dataset("sentiment140")
    #     train_df = dataset['train'].to_pandas()
    #     train_df = train_df[['text', 'sentiment']]
    #     train_df['sentiment'] = train_df['sentiment'].replace({0: 0, 4: 1})
    #     df = train_df
    #     print("Dataset loaded successfully using Hugging Face datasets.")
    # except Exception as e:
    #     print(f"Error loading dataset via Hugging Face: {e}. Please ensure you have the 'datasets' library installed (pip install datasets) and an internet connection.")
    #     exit()

    # # Preprocessing function
    # stop_words = set(stopwords.words('english'))
    # def preprocess_text(text):
    #     text = re.sub(r'http\S+', '', text) # Remove URLs
    #     text = re.sub(r'@\S+', '', text)   # Remove mentions
    #     text = re.sub(r'#\S+', '', text)   # Remove hashtags
    #     text = text.lower()
    #     text = ' '.join([word for word in text.split() if word not in stop_words])
    #     text = re.sub(r'[^a-zA-Z\s]', '', text) # Remove punctuation
    #     return text

    # df['processed_text'] = df['text'].apply(preprocess_text)

    # # Split data
    # X = df['processed_text']
    # y = df['sentiment']
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # # Tokenization
    # MAX_WORDS = 10000
    # tokenizer = Tokenizer(num_words=MAX_WORDS, oov_token="<unk>")
    # tokenizer.fit_on_texts(X_train)
    # X_train_sequences = tokenizer.texts_to_sequences(X_train)
    # X_test_sequences = tokenizer.texts_to_sequences(X_test)

    # # Padding
    # MAX_SEQUENCE_LENGTH = 150
    # X_train_padded = pad_sequences(X_train_sequences, maxlen=MAX_SEQUENCE_LENGTH, padding='post', truncating='post')
    # X_test_padded = pad_sequences(X_test_sequences, maxlen=MAX_SEQUENCE_LENGTH, padding='post', truncating='post')

    # VOCAB_SIZE = len(tokenizer.word_index) + 1

    # # Model Building
    # EMBEDDING_DIM = 100
    # model = Sequential([
    #     Embedding(VOCAB_SIZE, EMBEDDING_DIM, input_length=MAX_SEQUENCE_LENGTH),
    #     LSTM(128, return_sequences=True),
    #     LSTM(64),
    #     Dropout(0.5),
    #     Dense(1, activation='sigmoid')
    # ])

    # model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # # Training
    # EPOCHS = 5
    # BATCH_SIZE = 128
    # history = model.fit(X_train_padded, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_data=(X_test_padded, y_test))

    # # Evaluation
    # loss, accuracy = model.evaluate(X_test_padded, y_test)
    # print(f"Test Loss: {loss:.4f}")
    # print(f"Test Accuracy: {accuracy:.4f}")

    # # Plotting training history
    # plt.figure(figsize=(12, 4))
    # plt.subplot(1, 2, 1)
    # plt.plot(history.history['accuracy'], label='Train Accuracy')
    # plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    # plt.legend()
    # plt.title('Accuracy over Epochs')
    # plt.subplot(1, 2, 2)
    # plt.plot(history.history['loss'], label='Train Loss')
    # plt.plot(history.history['val_loss'], label='Validation Loss')
    # plt.legend()
    # plt.title('Loss over Epochs')
    # plt.show()

    # # --- Prediction Function ---
    # def predict_sentiment(text):
    #     processed_text = preprocess_text(text)
    #     sequence = tokenizer.texts_to_sequences([processed_text])
    #     padded_sequence = pad_sequences(sequence, maxlen=MAX_SEQUENCE_LENGTH, padding='post', truncating='post')
    #     prediction = model.predict(padded_sequence)[0]
    #     sentiment = "Positive" if prediction > 0.5 else "Negative"
    #     probability = prediction[0] if prediction > 0.5 else 1 - prediction[0]
    #     return sentiment, probability

    # # Example predictions
    # new_tweets = [
    #     "I love this new phone! It's amazing.",
    #     "This movie was absolutely terrible and boring.",
    #     "The weather is okay today.",
    #     "Feeling so happy and grateful.",
    #     "What a disappointing experience."
    # ]

    # for tweet in new_tweets:
    #     sentiment, probability = predict_sentiment(tweet)
    #     print(f"Tweet: '{tweet}' - Sentiment: {sentiment} (Probability: {probability:.4f})")

    # """# Expt 8: To study and implement a CNN Model for Digit Recognition application"""

    # import tensorflow as tf
    # from tensorflow.keras import layers, models
    # from tensorflow.keras.datasets import mnist
    # from tensorflow.keras.utils import to_categorical

    # # 1. Load and Preprocess the Data
    # (train_images, train_labels), (test_images, test_labels) = mnist.load_data()

    # # Normalize pixel values to be between 0 and 1
    # train_images = train_images.astype('float32') / 255.0
    # test_images = test_images.astype('float32') / 255.0

    # # Reshape images to include the channel dimension (28, 28, 1)
    # train_images = train_images.reshape((60000, 28, 28, 1))
    # test_images = test_images.reshape((10000, 28, 28, 1))

    # # One-hot encode the labels
    # train_labels = to_categorical(train_labels)
    # test_labels = to_categorical(test_labels)

    # # 2. Build the CNN Model
    # model = models.Sequential()
    # model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
    # model.add(layers.MaxPooling2D((2, 2)))
    # model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    # model.add(layers.MaxPooling2D((2, 2)))
    # model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    # model.add(layers.Flatten())
    # model.add(layers.Dense(64, activation='relu'))
    # model.add(layers.Dropout(0.5))
    # model.add(layers.Dense(10, activation='softmax'))

    # # Model Summary
    # model.summary()

    # # 3. Compile the Model
    # model.compile(optimizer='adam',
    #             loss='categorical_crossentropy',
    #             metrics=['accuracy'])

    # # 4. Train the Model
    # epochs = 10
    # batch_size = 64
    # history = model.fit(train_images, train_labels, epochs=epochs, batch_size=batch_size, validation_split=0.2)

    # # 5. Evaluate the Model
    # test_loss, test_accuracy = model.evaluate(test_images, test_labels, verbose=0)
    # print(f"Test Loss: {test_loss:.4f}")
    # print(f"Test Accuracy: {test_accuracy:.4f}")

    # # Plot training history
    # plt.figure(figsize=(12, 4))
    # plt.subplot(1, 2, 1)
    # plt.plot(history.history['accuracy'], label='Train Accuracy')
    # plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    # plt.legend()
    # plt.title('Accuracy over Epochs')

    # plt.subplot(1, 2, 2)
    # plt.plot(history.history['loss'], label='Train Loss')
    # plt.plot(history.history['val_loss'], label='Validation Loss')
    # plt.legend()
    # plt.title('Loss over Epochs')
    # plt.show()

    # # 6. Make Predictions (Example)
    # import matplotlib.pyplot as plt

    # predictions = model.predict(test_images[:10])
    # predicted_labels = np.argmax(predictions, axis=1)
    # true_labels = np.argmax(test_labels[:10], axis=1)

    # plt.figure(figsize=(10, 5))
    # for i in range(10):
    #     plt.subplot(2, 5, i + 1)
    #     plt.imshow(test_images[i].reshape(28, 28), cmap='gray')
    #     plt.title(f"Predicted: {predicted_labels[i]}\nTrue: {true_labels[i]}")
    #     plt.axis('off')
    # plt.tight_layout()
    # plt.show()
    '''
    print("Your welcome chiggas")
    