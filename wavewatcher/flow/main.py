import numpy as np
import pandas as pd
from time import sleep
from statistics import mode

from wavewatcher.ml_logic.preprocess import preprocess_image_lite, preprocess_image_main
from wavewatcher.ml_logic.model import initialize_model, compile_model, train_model, evaluate_model
from wavewatcher.frontend_interface.website import get_10_images

def get_images_preprocessed():
    lista = get_10_images()
    preprocessed = []
    i = 0
    for i in lista:
        if i < 3:
            image = preprocess_image_lite(i)
            preprocessed.append(image)
    i += 1
    return preprocessed

def predict_10(X):

    model = load_model()
    results = []
    for x in X:
        flat, chaotic, good = model.predict(np.array([x]))[0]
        results.append(return_outcome(flat,chaotic, good))
    return mode(results)

def return_outcome(flat,chaotic,good):
    if flat >chaotic and flat > good:
        return "flat"
    elif chaotic > flat and chaotic > good:
        return "chaotic"
    elif good > flat and good > chaotic:
        return "good"
    else:
        return "undetermined"

if __name__ == '__main__':
    get_images_preprocessed()
    predict_10()
