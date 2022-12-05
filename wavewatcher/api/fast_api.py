from datetime import datetime
import pandas as pd
from fastapi import FastAPI
from tensorflow.keras import models
import numpy as np
import requests
from http import HTTPStatus
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime

#IMPORTS
from wavewatcher.api.utilities import get_images
from wavewatcher.api.utilities import majority_voting
from wavewatcher.api.utilities import preprocess_image_lite, majority_voting, get_images, predictions_time

# model state
from tensorflow.python.lib.io import file_io
from keras.models import load_model

# Question, will it run from a docker image? : Yes!

logging.basicConfig(level = logging.INFO ,
                    format = "%(message)s")
app = FastAPI(title = "Wavewatcher")

# I don't know exactly what is the middleware but it seems neccesary

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.on_event("startup")
async def startup_event():
    then = datetime.now()
    logging.info("Buenos Dias!")
    model_file = file_io.FileIO('gs://waves_surfer_data/modelb7.h5', mode='rb')
    temp_model_location = './temp_model.h5'
    temp_model_file = open(temp_model_location, 'wb')
    temp_model_file.write(model_file.read())
    temp_model_file.close()
    model_file.close()
    app.state.model = load_model(temp_model_location)
    now = datetime.now()
    total_startup_seconds = round((now - then).total_seconds(),2)
    logging.info(f"Model has succesfully started within {total_startup_seconds} second(s)!")

@app.on_event("shutdown")
async def shutdown_event():
    logging.info("Goodbye!")


@app.get("/")
def root():
    """Health Check"""
    return {"greetings": "Hello",
            "status" : HTTPStatus.OK,
            "data": {}}


@app.get("/predict")
async def predict(num_images : int = 1) -> dict:
    images = get_images(num_images)
    sequence = ["Chaotic","Good","Flat"]
    predictions = []

    index = 0
    indexes_to_remove = []
    for img in images:
        _, pixel_counts = np.unique(img, return_counts=True)
        if pixel_counts[0] > 1000:
            indexes_to_remove.append(index)
        index += 1

    filtered_images = np.delete(images, indexes_to_remove, axis=0)
    del images
    processed_imgs = []

    for image in filtered_images:
        processed_img = np.array(preprocess_image_lite(image))
        processed_img = processed_img.reshape(1,*processed_img.shape[::-1])
        processed_imgs.append(processed_img)

        prediction = app.state.model.predict(processed_img)
        prediction = sequence[ np.argmax(prediction) ]
        predictions.append(prediction)


    counts = [predictions.count(cat) for cat in sequence]
    max_index = counts.index(max(counts))
    return {"prediction" : sequence[max_index]}
