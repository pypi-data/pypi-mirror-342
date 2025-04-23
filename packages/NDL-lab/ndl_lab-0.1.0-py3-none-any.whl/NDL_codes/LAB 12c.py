import numpy as np
def sigmoid(x): return 1/(1+np.exp(-x))
def lstm_cell_forward(x_t, h_prev, c_prev, p):
    concat = np.vstack((h_prev, x_t))
    f = sigmoid(p["W_f"]@concat + p["b_f"])
    i = sigmoid(p["W_i"]@concat + p["b_i"])
    c_ = np.tanh(p["W_c"]@concat + p["b_c"])
    c_next = f*c_prev + i*c_
    o = sigmoid(p["W_o"]@concat + p["b_o"])
    h_next = o * np.tanh(c_next)
    return h_next, c_next
np.random.seed(2)
input_size, hidden_size = 3, 5
x_t = np.random.randn(input_size,1)
h_prev = np.random.randn(hidden_size,1)
c_prev = np.random.randn(hidden_size,1)
p = {k: np.random.randn(hidden_size, hidden_size+input_size) if 'W' in k else np.random.randn(hidden_size,1) for k in ["W_f","b_f","W_i","b_i","W_c","b_c","W_o","b_o"]}
h_next, c_next = lstm_cell_forward(x_t, h_prev, c_prev, p)
print("Next hidden state h_next:\n", h_next)
print("\nNext cell state c_next:\n", c_next)
