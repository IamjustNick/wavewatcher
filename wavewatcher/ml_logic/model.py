import time
import numpy as np
import pandas as pd
from tensorflow.keras import layers, Sequential, models
from keras.utils import to_categorical
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from keras.applications import efficientnet
from typing import Tuple
import cv2 as cv
import matplotlib.pyplot as plt
import skimage
import glob
import os
import random
from PIL import ImageFile
from sklearn.model_selection import train_test_split
from colorama import Fore, Style

ImageFile.LOAD_TRUNCATED_IMAGES = True

print(Fore.BLUE + "\nLoading tensorflow..." + Style.RESET_ALL)
start = time.perf_counter()



end = time.perf_counter()
print(f"\n✅ tensorflow loaded ({round(end - start, 2)} secs)")



def initialize_model():
    """
    Initialize the Neural Network with random weights
    """
    print(Fore.BLUE + "\nInitialize model..." + Style.RESET_ALL)

    n_classes = 3
    model = models.Sequential()
    model.add(
        efficientnet.EfficientNetB7(weights = 'imagenet',
                                     include_top = False,
                                     classes = n_classes,
                                     input_shape = (300, 300, 3))
    )
    model.add(layers.GlobalAveragePooling2D())
    model.add(layers.Flatten())
    model.add(layers.BatchNormalization())
    model.add(layers.Dense(256, activation = "relu"))
    model.add(layers.Dropout(0.2))

    model.add(layers.BatchNormalization())
    model.add(layers.Dense(256, activation = "relu"))
    model.add(layers.Dropout(0.2))
    model.add(layers.BatchNormalization())

    model.add(layers.Dense(n_classes, activation = "softmax"))
    model.layers[0].trainable = False

    print("\n✅ model initialized")

    return model

def compile_model(model, learning_rate=1e-4):
    """
    Compile the Neural Network
    """
    model.compile(loss = "categorical_crossentropy",
                            optimizer = Adam(learning_rate=learning_rate),
                            metrics = ["accuracy"])

    print("\n✅ model compiled")
    return model

def train_model(model,
                X: np.ndarray,
                y: np.ndarray,
                batch_size=16,
                patience=15,
                validation_split=0.2,
                validation_data=None):
    """
    Fit model and return a the tuple (fitted_model, history)
    """

    print(Fore.BLUE + "\nTrain model..." + Style.RESET_ALL)

    es = EarlyStopping(monitor="val_loss",
                       mode = "min",
                       patience= patience,
                       restore_best_weights=True,
                       verbose=0)

    history = model.fit(X,
                        y,
                        validation_split=validation_split,
                        validation_data=validation_data,
                        epochs=60,
                        batch_size=batch_size,
                        callbacks=[es],
                        verbose=0)

    print(f"\n✅ model trained ({len(X)} rows)")

    return model, history

def evaluate_model(model,
                   X: np.ndarray,
                   y: np.ndarray,
                   batch_size=16):
    """
    Evaluate trained model performance on dataset
    """

    print(Fore.BLUE + f"\nEvaluate model on {len(X)} rows..." + Style.RESET_ALL)

    if model is None:
        print(f"\n❌ no model to evaluate")
        return None

    metrics = model.evaluate(
        x=X,
        y=y,
        batch_size=batch_size,
        verbose=1,
        # callbacks=None,
        return_dict=True)

    loss = metrics["loss"]
    accuracy = metrics["accuracy"]

    print(f"\n✅ model evaluated: loss {round(loss, 2)} accuracy {round(accuracy, 2)}")

    return metrics
