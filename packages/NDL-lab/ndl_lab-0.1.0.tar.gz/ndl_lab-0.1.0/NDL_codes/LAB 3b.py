import numpy as np

def sigmoid(x): return 1 / (1 + np.exp(-x))
def sigmoid_derivative(x): return x * (1 - x)

inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
outputs = np.array([[0], [1], [1], [0]])
learning_rates = [0.01, 0.1, 0.5]
epochs = 10000

for lr in learning_rates:
    print(f"Training with Learning Rate: {lr}")
    hidden_weights = np.random.uniform(-1, 1, (2, 2))
    hidden_bias = np.random.uniform(-1, 1, (1, 2))
    output_weights = np.random.uniform(-1, 1, (2, 1))
    output_bias = np.random.uniform(-1, 1, (1, 1))
    for epoch in range(epochs):
        h_in = inputs @ hidden_weights + hidden_bias
        h_out = sigmoid(h_in)
        o_in = h_out @ output_weights + output_bias
        pred = sigmoid(o_in)
        err = outputs - pred
        mse = np.mean(err**2)
        d_pred = err * sigmoid_derivative(pred)
        d_h = (d_pred @ output_weights.T) * sigmoid_derivative(h_out)
        output_weights += h_out.T @ d_pred * lr
        output_bias += np.sum(d_pred, axis=0, keepdims=True) * lr
        hidden_weights += inputs.T @ d_h * lr
        hidden_bias += np.sum(d_h, axis=0, keepdims=True) * lr
        if epoch % 1000 == 0: print(f"Epoch {epoch}, MSE: {mse}")
    print(f"Final Mean Squared Error: {mse}\n")

print("\nXOR Gate Results:")
for inp in inputs:
    h_in = inp @ hidden_weights + hidden_bias
    h_out = sigmoid(h_in)
    o_in = h_out @ output_weights + output_bias
    out = sigmoid(o_in)
    print(f"Input: {inp} -> Output: {out}")
