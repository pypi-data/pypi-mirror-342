code='''import numpy as np

def train_hopfield(patterns):
    W = sum(np.outer(p, p) for p in patterns)
    np.fill_diagonal(W, 0)
    return W

def recall_pattern(W, pattern, max_iter=10):
    for _ in range(max_iter):
        pattern = np.sign(W @ pattern)
    return pattern

# Example usage
original = [-1, 1, -1, -1, -1, -1, -1, 1, -1, 1]
noisy = [-1, -1, -1, 1, -1, -1, -1, 1, -1, -1]

W = train_hopfield([original])
recovered = recall_pattern(W, np.array(noisy))
print("Original:", original)
print("Noisy:", noisy)
print("Recovered:", recovered)
'''