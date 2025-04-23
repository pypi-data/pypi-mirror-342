w1, w2, b = 0.5, 0.5, -1

def activate(x):
    return 1 if x >= 0 else 0

def train(X, y, lr, epochs):
    global w1, w2, b
    for _ in range(epochs):
        err = 0
        for (A, B), t in zip(X, y):
            o = activate(w1*A + w2*B + b)
            e = t - o
            w1 += lr * e * A
            w2 += lr * e * B
            b  += lr * e
            err += abs(e)
        if err == 0: break

X = [(0,0), (0,1), (1,0), (1,1)]
y = [0, 0, 0, 1]
train(X, y, 0.1, 100)

for A, B in X:
    print(f"Input: ({A}, {B}) Output: {activate(w1*A + w2*B + b)}")
