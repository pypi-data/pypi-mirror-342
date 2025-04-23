code='''import matplotlib.pyplot as plt
from tensorflow.keras import Sequential, layers, datasets

(x_train, y_train), (x_test, y_test) = datasets.mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

model = Sequential([
    layers.Flatten(input_shape=(28, 28)),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')
])
model.compile(optimizer='adam', loss="sparse_categorical_crossentropy", metrics=['accuracy'])

h = model.fit(x_train, y_train, epochs=10, validation_data=(x_test, y_test))
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"Accuracy is: {test_acc * 100:.2f}%")

plt.plot(h.history['accuracy'], label="Training Accuracy")
plt.plot(h.history['val_accuracy'], label="Validation Accuracy")
plt.xlabel("Epochs"), plt.ylabel("Accuracy")
plt.legend()
plt.show()
'''