import numpy as np
def rnn_forward(X, h0, W_x, W_h, b_h, W_y, b_y):
    t = X.shape[0]
    h = np.zeros((t, h0.shape[0], 1))
    y = np.zeros((t, W_y.shape[0], 1))
    h_prev = h0
    for i in range(t):
        x = X[i].reshape(-1,1)
        h_t = np.tanh(W_x@x + W_h@h_prev + b_h)
        y_t = W_y@h_t + b_y
        h[i], y[i], h_prev = h_t, y_t, h_t
    return h, y

np.random.seed(1)
t,i,hid,out = 4,3,5,2
X = np.random.randn(t,i)
h0 = np.zeros((hid,1))
W_x = np.random.randn(hid,i)
W_h = np.random.randn(hid,hid)
b_h = np.random.randn(hid,1)
W_y = np.random.randn(out,hid)
b_y = np.random.randn(out,1)
h, y = rnn_forward(X, h0, W_x, W_h, b_h, W_y, b_y)
print("Hidden states:\n", h)
print("\nOutputs:\n", y)
