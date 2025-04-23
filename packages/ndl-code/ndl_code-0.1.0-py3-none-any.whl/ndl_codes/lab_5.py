code='''import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
class Neuron:
    def __init__(self, features, lr):
        self.lr = lr
        self.weights = np.random.rand(features)
    def activate(self, inputs):
        return np.dot(inputs, self.weights)
    def hebbian_learn(self, inputs, epochs=100):
        for _ in range(epochs):
            for p in inputs:
                self.weights += self.lr * self.activate(p) * p
            norm = np.linalg.norm(self.weights)
            if norm:
                self.weights /= norm
x = np.random.randint(0, 100, 1000)
y = 3 * x + 2 + np.random.normal(2, 50, x.shape)
inputs = np.column_stack((x, y))
centered = inputs - np.mean(inputs, axis=0)
neuron = Neuron(2, 1e-5)
neuron.hebbian_learn(centered)
w = neuron.weights * 500
pca = PCA(n_components=1).fit(centered)
plt.scatter(centered[:, 0], centered[:, 1], alpha=0.3, label="Data points")
plt.quiver(0, 0, *w, color="r", scale=3, scale_units='xy', angles='xy', label="Hebbian")
plt.quiver(0, 0, *(pca.components_[0] * 500), color="g", scale=3, scale_units='xy', angles='xy', label="PC")
plt.legend()
plt.title("Hebbian Learning vs PCA")
plt.axis('equal')
plt.show()
'''