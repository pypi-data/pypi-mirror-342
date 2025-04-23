import cv2, numpy as np, matplotlib.pyplot as plt
from numpy.random import rand, uniform
from tensorflow.keras import Sequential, layers, datasets
(x_train, y_train), (x_test, y_test) = datasets.mnist.load_data()
x_train, x_test = x_train/255, x_test/255
def augment(img):
    r,c=img.shape
    M=cv2.getRotationMatrix2D((c/2,r/2), uniform(-30,30), uniform(.8,1.2))
    img=cv2.warpAffine(img, M, (c,r))
    if rand()>.5: img=cv2.flip(img,1)
    if rand()>.5: img=cv2.flip(img,0)
    return img
fig,ax=plt.subplots(2,10,figsize=(15,4))
for i in range(10):
    ax[0,i].imshow(x_train[i],'gray'); ax[0,i].axis('off')
    ax[1,i].imshow(augment(x_train[i]),'gray'); ax[1,i].axis('off')
plt.suptitle("Image Transformations"); plt.show()
aug = np.array([augment(img) for img in x_train])
x_train = np.vstack((x_train, aug))
y_train = np.hstack((y_train, y_train))
model = Sequential([
    layers.Flatten(input_shape=(28,28)),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
h = model.fit(x_train, y_train, epochs=10, validation_data=(x_test, y_test), verbose=2)
_, acc = model.evaluate(x_test, y_test, verbose=0)
print(f"Accuracy: {acc*100:.2f}%")
plt.plot(h.history['accuracy'], marker='o', label='Train')
plt.plot(h.history['val_accuracy'], marker='o', label='Val')
plt.xlabel('Epochs'); plt.ylabel('Accuracy'); plt.legend(); plt.ylim(.6,1); plt.show()
