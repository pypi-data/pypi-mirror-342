import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.reshape(-1, 28, 28, 1).astype('float32') / 255.0
x_test = x_test.reshape(-1, 28, 28, 1).astype('float32') / 255.0
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)


def create_model():
    return models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])


optimizers = {
    "Adam": tf.keras.optimizers.Adam(),
    "RMSProp": tf.keras.optimizers.RMSprop(),
    "Adagrad": tf.keras.optimizers.Adagrad()
}

for name, opt in optimizers.items():
    model = create_model()
    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=10, validation_split=0.2, verbose=0)
    _, acc = model.evaluate(x_test, y_test)
    print(f"{name} Accuracy: {acc*100:.2f}%")
