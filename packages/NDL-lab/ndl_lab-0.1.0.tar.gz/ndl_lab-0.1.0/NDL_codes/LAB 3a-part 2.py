# Perceptron Logic Gate Simulator (linearly separable only)
gates = {
    'AND':  ([(0,0), (0,1), (1,0), (1,1)], [0,0,0,1]),
    'OR':   ([(0,0), (0,1), (1,0), (1,1)], [0,1,1,1]),
    'NAND': ([(0,0), (0,1), (1,0), (1,1)], [1,1,1,0]),
    'NOR':  ([(0,0), (0,1), (1,0), (1,1)], [1,0,0,0]),
    'NOT':  ([(0,), (1,)], [1,0]),
}

for name, (X, y) in gates.items():
    w = [0.5] * len(X[0])
    b = -0.5
    for _ in range(100):  # training loop
        for x, t in zip(X, y):
            z = sum(xi * wi for xi, wi in zip(x, w)) + b
            o = 1 if z >= 0 else 0
            e = t - o
            w = [wi + 0.1 * e * xi for xi, wi in zip(x, w)]
            b += 0.1 * e
    print(f"{name} Gate:")
    for x in X:
        z = sum(xi * wi for xi, wi in zip(x, w)) + b
        o = 1 if z >= 0 else 0
        print(f"Input: {x} -> Output: {o}")
    print()
