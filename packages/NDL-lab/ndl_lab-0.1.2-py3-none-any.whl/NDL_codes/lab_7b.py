import numpy as np
import matplotlib.pyplot as plt

# Activation functions: Sigmoid and its derivative.
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    s = sigmoid(x)
    return s * (1 - s)

# Network architecture parameters.
input_dim = 1    # Input is a scalar.
hidden_dim = 50  # Number of neurons in the hidden layer.
output_dim = 1   # Output is a scalar.

# Initialize weights and biases.
np.random.seed(42)
W1 = np.random.randn(hidden_dim, input_dim) * 0.1  # Shape: (hidden_dim, 1)
b1 = np.zeros((hidden_dim, 1))                     # Shape: (hidden_dim, 1)
W2 = np.random.randn(output_dim, hidden_dim) * 0.1   # Shape: (1, hidden_dim)
b2 = np.zeros((output_dim, 1))                     # Shape: (1, 1)

# Hyperparameters.
learning_rate = 0.01
num_epochs = 20000

# Generate training data.
N = 1000
X_train = np.random.uniform(-np.pi, np.pi, (1, N))  # Shape: (1, N)
y_train = np.sin(X_train)                           # Shape: (1, N)

losses = []

# Training loop using gradient descent.
for epoch in range(num_epochs):
    # Forward pass.
    Z1 = np.dot(W1, X_train) + b1      # (hidden_dim, N)
    A1 = sigmoid(Z1)                   # Hidden layer activation.
    Z2 = np.dot(W2, A1) + b2           # (1, N)
    A2 = Z2                          # Linear activation for output.
    
    # Compute mean squared error loss.
    loss = np.mean((A2 - y_train) ** 2)
    losses.append(loss)
    
    # Backward pass.
    dA2 = 2 * (A2 - y_train) / N       # (1, N)
    # Gradients for output layer.
    dW2 = np.dot(dA2, A1.T)            # (1, hidden_dim)
    db2 = np.sum(dA2, axis=1, keepdims=True)  # (1, 1)
    
    # Gradients for hidden layer.
    dA1 = np.dot(W2.T, dA2)            # (hidden_dim, N)
    dZ1 = dA1 * sigmoid_derivative(Z1) # (hidden_dim, N)
    dW1 = np.dot(dZ1, X_train.T)       # (hidden_dim, 1)
    db1 = np.sum(dZ1, axis=1, keepdims=True)  # (hidden_dim, 1)
    
    # Update weights and biases.
    W2 -= learning_rate * dW2
    b2 -= learning_rate * db2
    W1 -= learning_rate * dW1
    b1 -= learning_rate * db1
    
    if epoch % 2000 == 0:
        print(f"Epoch {epoch}, Loss: {loss:.6f}")

# Evaluate the network on test data.
X_test = np.linspace(-np.pi, np.pi, 100).reshape(1, -1)
Z1_test = np.dot(W1, X_test) + b1
A1_test = sigmoid(Z1_test)
Z2_test = np.dot(W2, A1_test) + b2
y_pred = Z2_test

# Plot the training loss history.
plt.figure(figsize=(10, 4))
plt.plot(losses, label='Training Loss')
plt.xlabel("Epoch")
plt.ylabel("MSE Loss")
plt.title("Training Loss History")
plt.legend()
plt.show()

# Plot the network approximation against the true sine function.
plt.figure(figsize=(8, 4))
plt.plot(X_test.flatten(), np.sin(X_test).flatten(), label='True sin(x)')
plt.plot(X_test.flatten(), y_pred.flatten(), '--', label='NN Approximation')
plt.xlabel("x")
plt.ylabel("sin(x)")
plt.title("Neural Network Approximation of sin(x)")
plt.legend()
plt.show()
