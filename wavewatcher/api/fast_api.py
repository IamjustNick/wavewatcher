from datetime import datetime
import pandas as pd
from fastapi import FastAPI
from tensorflow.keras import models
import numpy as np
import requests
from http import HTTPStatus
from google.cloud import storage
from fastapi.middleware.cors import CORSMiddleware
import logging
#Internal imports
#To import images and preprocess them
from wavewatcher.api.utilities import get_images,preprocess_image_lite
# Model state
from tensorflow.python.lib.io import file_io
from keras.models import load_model

logging.basicConfig(level = logging.INFO ,
                    format = "%(message)s")
app = FastAPI(title = "Wavewatcher")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Start up
@app.on_event("startup")
async def startup_event():
    then = datetime.now()
    logging.info("Good morning amigo!")
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

#Predict function
@app.get("/predict")
async def predict(num_images : int = 15) -> dict:
    images = get_images(num_images)
    sequence = ["Chaotic","Good","Flat"]
    predictions = []

    index = 0
    indexes_to_remove = []
    #Removes "black" screenshots
    for img in images:
        _, pixel_counts = np.unique(img, return_counts=True)
        if pixel_counts[0] > 1000:
            indexes_to_remove.append(index)
        index += 1

    filtered_images = np.delete(images, indexes_to_remove, axis=0)
    del images

    for image in filtered_images:
        processed_img = preprocess_image_lite(image)
        processed_img = np.array([processed_img])
        prediction = app.state.model.predict(processed_img)
        # Decides the outcome based on the position of the highest value
        # Chaotic, Flat, Good
        prediction = sequence[ np.argmax(prediction)]
        predictions.append(prediction)
    #"Voting" Decides the day condition based on the most repeated outcome
    counts = [predictions.count(cat) for cat in sequence]
    max_index = counts.index(max(counts))

    forecast_df = pd.DataFrame({"prediction":[sequence[max_index]],
                        "time":[datetime.now().strftime("%H:%M:%S")],
                        "beach":["empty"]})

    forecast_df.to_csv("gs://waves_surfer_data/prediction/forecast.csv")
    return {"prediction" : sequence[max_index]}
