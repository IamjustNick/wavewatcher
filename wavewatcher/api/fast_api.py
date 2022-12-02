from datetime import datetime
import pandas as pd
from fastapi import FastAPI
from tensorflow.keras import models
import numpy as np
import requests
from fastapi.middleware.cors import CORSMiddleware


#IMPORTS
from wavewatcher.utilities(move_later_fix_imports) import get_images
from wavewatcher.utilities(move_later_fix_imports) import majority_voting
from wavewatcher.utilities(move_later_fix_imports) import preprocess_image_lite, majority_voting, get_images, predictions_time

# model state
from tensorflow.python.lib.io import file_io
from keras.models import load_model

# Question, will it run from a docker image?


app = FastAPI()

model_file = file_io.FileIO('gs://waves_surfer_data/modelb7.h5', mode='rb')
temp_model_location = './temp_model.h5'
temp_model_file = open(temp_model_location, 'wb')
temp_model_file.write(model_file.read())
temp_model_file.close()
model_file.close()
app.state.model = load_model(temp_model_location)

# I don't know exactly what is the middleware but it seems neccesary

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

#1 get images

images = get_images(30)
images = images[10:]

outcomes = predictions_time(images)


results =app.state.model.predict(outcomes)

def printed_result(results):
    {}
    outcome = majority_voting(results)


if __name__ == "__main__":
    tik = time.perf_counter()
    images = get_images(number = 5)
    tak = time.perf_counter()
    print(f"Process completed within {tak-tik:.2f} second(s)!")
# http://127.0.0.1:8000/predict?pickup_datetime=2012-10-06 12:10:20&pickup_longitude=40.7614327&pickup_latitude=-73.9798156&dropoff_longitude=40.6513111&dropoff_latitude=-73.8803331&passenger_count=2
@app.get("/predict")
def predict():
    images = get_images()




@app.get("/")
def root():
    return {'greeting': 'Hello'}
