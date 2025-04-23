from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.reshape(-1,28,28,1) / 255.0
x_test = x_test.reshape(-1,28,28,1) / 255.0
y_train = to_categorical(y_train,10)
y_test = to_categorical(y_test,10)

def lenet():
    return models.Sequential([
        layers.Conv2D(6, (5,5), activation='relu'), layers.AveragePooling2D((2,2)),
        layers.Conv2D(16, (5,5), activation='relu'), layers.AveragePooling2D((2,2)), layers.Flatten(),
        layers.Dense(120, activation='relu'), layers.Dense(84, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
def alexnet():
    return models.Sequential([
        layers.Conv2D(64, (3,3), activation='relu'), layers.MaxPooling2D((2,2)),
        layers.Conv2D(128, (3,3), activation='relu'), layers.MaxPooling2D((2,2)),
        layers.Conv2D(256, (3,3), activation='relu'), layers.Flatten(),
        layers.Dense(512, activation='relu'), layers.Dropout(0.5),
        layers.Dense(10, activation='softmax')
    ])
def vgg():
    return models.Sequential([
        layers.Conv2D(64, (3,3), activation='relu', padding='same'),
        layers.Conv2D(64, (3,3), activation='relu', padding='same'), layers.MaxPooling2D((2,2)),
        layers.Conv2D(128, (3,3), activation='relu', padding='same'),
        layers.Conv2D(128, (3,3), activation='relu', padding='same'), layers.MaxPooling2D((2,2)),
        layers.Flatten(), layers.Dense(256, activation='relu'), layers.Dropout(0.5),
        layers.Dense(10, activation='softmax')
    ])
def placesnet():
    return models.Sequential([
        layers.Conv2D(32, (5,5), activation='relu'), layers.MaxPooling2D((2,2)),
        layers.Conv2D(64, (5,5), activation='relu'), layers.MaxPooling2D((2,2)),
        layers.Flatten(), layers.Dense(128, activation='relu'),
        layers.Dropout(0.5), layers.Dense(10, activation='softmax')
    ])

models_dict = {"LeNet": lenet(), "AlexNet": alexnet(), "VGG": vgg(), "PlacesNet": placesnet()}
accs = {}
for name, model in models_dict.items():
    print(f"\nTraining {name}\n")
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    h = model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=10, batch_size=32, verbose=0)
    accs[name] = h

for name, h in accs.items():
    plt.figure(figsize=(6,4))
    plt.plot(h.history['accuracy'], label='Train Acc')
    plt.plot(h.history['val_accuracy'], label='Val Acc', linestyle='dashed')
    plt.xlabel('Epochs'), plt.ylabel('Accuracy')
    plt.title(name)
    plt.legend(), plt.show()
