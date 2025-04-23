code='''import tensorflow as tf
import numpy as np
class RNNModel(tf.keras.Model):
    def __init__(self, hidden_dim, output_dim):
        super().__init__()
        self.rnn = tf.keras.layers.SimpleRNN(hidden_dim, return_sequences=True)
        self.dense = tf.keras.layers.Dense(output_dim)
    def call(self, x):
        x = self.rnn(x)
        return self.dense(x)
if __name__ == "__main__":
    time_steps, input_dim, hidden_dim, output_dim = 5, 3, 4, 2
    num_samples = 100
    X = np.random.randn(num_samples, time_steps, input_dim).astype(np.float32) * 0.1
    Y = np.random.randn(num_samples, time_steps, output_dim).astype(np.float32) * 0.1
    model = RNNModel(hidden_dim, output_dim)
    model.compile(optimizer=tf.keras.optimizers.Adam(1e-3), loss='mse')
    model.fit(X, Y, epochs=50, verbose=2)
'''