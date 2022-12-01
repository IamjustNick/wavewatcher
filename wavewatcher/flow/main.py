import numpy as np
import pandas as pd
from time import sleep
from statistics import mode
from wavewatcher.ml_logic.preprocess import preprocess_image_lite, preprocess_image_main
from wavewatcher.ml_logic.model import initialize_model, compile_model, train_model, evaluate_model
import os
import cv2 as cv

def fetch_train_images():
    X = []
    y = []
    idx = 0
    failed =[]

    for root , dirs , files in os.walk("raw_data"):
        if dirs:
            parent = root
            folders = dirs
            print(folders)

        if files:
            print(f"Preprocessing folder {folders[idx]}...")
            failed = []
            for file in np.random.choice(np.array(files),len(files), replace = False):
                try:
                    original_image = cv.imread(os.path.join(parent , folders[idx], file), 0)


                    processed_image = preprocess_image_lite(original_image)

                    if len(processed_image) < 2:
                        print(f"problemita in {os.path.join(parent , folders[idx], file)}")
                    else:
                        X.append(np.array(processed_image).T)
                        y.append(idx)
                    #The print below was just to check the value for each situation
                    #print(idx)

                except Exception as e:
                    print("Detected bad image!")
                    failed.append(os.path.join(parent , folders[idx], file))
                    continue

            idx += 1

    X = np.array(X)
    y = np.array(y)
    return X,y
def get_images_preprocessed(lista):
    preprocessed = []
    i = 0
    for i in lista:
        if i < 3:
            image = preprocess_image_lite(i)
            preprocessed.append(image)
    i += 1
    return preprocessed

def predict_10(X,y, X_pred):

    model = initialize_model()
    model = compile_model(model)
    model = train_model(model,X,y)

    results = []

    for x in X_pred:
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
