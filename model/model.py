import os
os.environ["KERAS_BACKEND"] = "torch"

import keras

from pathlib import Path
from PIL import Image
import numpy as np

p = Path('./data/raw/224')
gen = p.rglob('*.jpg')
result_list = sorted(gen)

def get_image_label(file_name):
    part = file_name.split('_')[1]
    number_string = part[1:]
    number = int(number_string)
    return number

def get_image_array(file):
    with Image.open(file) as image:
        rgb = image.convert("RGB")
        arr = np.array(rgb)
    return arr

def train_model(days, epochs, batch_size):
    images_per_day = 64

    for i in range(0, days * images_per_day, images_per_day):
        chunk_images = image_arrays[i:i + images_per_day]
        chunk_labels = image_labels[i:i + images_per_day]

        if len(chunk_images) < images_per_day:
            break

        train_images.extend(chunk_images[:48])
        train_labels.extend(chunk_labels[:48])

        val_images.extend(chunk_images[48:56])
        val_labels.extend(chunk_labels[48:56])

        test_images.extend(chunk_images[56:64])
        test_labels.extend(chunk_labels[56:64])

    x_train = np.stack(train_images)
    y_train = np.array(train_labels, dtype="float32")
    x_val = np.stack(val_images)
    y_val = np.array(val_labels, dtype="float32")
    x_test = np.stack(test_images)
    y_test = np.array(test_labels, dtype="float32")

    print("Training images:", len(train_images))
    print("Validation images:", len(val_images))
    print("Testing images:", len(test_images))
    print("Sample training label:", y_train[0])
    print("Sample training array shape:", x_train[0].shape)

    print(keras.backend.backend())

    model = keras.Sequential([
        keras.Input(shape=(224, 224, 3)),
        keras.layers.Rescaling(1./255),
        keras.layers.Conv2D(filters=32, kernel_size=3, padding="same", activation="relu"),
        keras.layers.MaxPooling2D(pool_size=2),
        keras.layers.Conv2D(filters=64, kernel_size=3, padding="same", activation="relu"),
        keras.layers.MaxPooling2D(pool_size=2),
        keras.layers.Conv2D(filters=128, kernel_size=3, padding="same", activation="relu"),
        keras.layers.MaxPooling2D(pool_size=2),
        keras.layers.Conv2D(filters=256, kernel_size=3, padding="same", activation="relu"),
        keras.layers.MaxPooling2D(pool_size=2),
        keras.layers.Conv2D(filters=256, kernel_size=3, padding="same", activation="relu"),
        keras.layers.MaxPooling2D(pool_size=2),
        keras.layers.Flatten(),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(32, activation="relu"),
        keras.layers.BatchNormalization(),
        keras.layers.Dense(32, activation="relu"),
        keras.layers.BatchNormalization(),
        keras.layers.Dense(1)
    ])

    model.compile(
        optimizer="adam",
        loss="mae"
    )

    model.summary()

    model.fit(x_train,
            y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(x_val, y_val),
            verbose=1)

    print(model.evaluate(x_test, y_test, verbose=1))

image_labels = [get_image_label(file.name) for file in result_list]
image_arrays = [get_image_array(file) for file in result_list]

train_images, train_labels = [], []
val_images, val_labels = [], []
test_images, test_labels = [], []

train_model(18, 5000, 32)