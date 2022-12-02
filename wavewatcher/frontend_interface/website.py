import streamlit as st
import base64
import numpy as np
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
from time import sleep
from colorama import Fore,Style

from wavewatcher.flow.main import get_images_preprocessed, predict_10, fetch_train_images
from wavewatcher.ml_logic.preprocess import preprocess_image_lite, preprocess_image_main
from wavewatcher.ml_logic.model import initialize_model, compile_model, train_model, evaluate_model

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('/Users/nicolasmartinez-geijovila/code/IamjustNick/wavewatcher/wavewatcher/frontend_interface/5423150-beach-water-sea-wave-ocean-sand-sandy-wafe-looking-down-from-above-tide-ripple-seashore-shoreline-shore-split-symmetrical-yellow-sand-crashing-wafe-clear-water-free-pictures.jpg')


#This code just calls API and shows the picture
st.markdown("""# Welcome to WaveWatcher!
## Done by Nico, Mateo, Miguel and Louis""")

url = "https://oceanbees-xbzgoqiv5a-ew.a.run.app/honey"
#response = requests.get(url = url, stream = True)
#img = Image.open(BytesIO(response.content))

#
my_bar = st.progress(0)
images_for_prediction = []

def get_10_images():
    #Calling the api several times
    images_for_prediction.clear()
    while len(images_for_prediction) < 20:
        response = requests.get(url = url, stream = True)
        #img = Image.open(BytesIO(response.content))
        images_for_prediction.append(response.content)
        my_bar.progress(len(images_for_prediction)*5)
        sleep(2)
    return images_for_prediction

X_pred = get_images_preprocessed(images_for_prediction)
X,y = fetch_train_images()
preds = predict_10(X,y,X_pred)

st.button("Get prediction!", on_click= get_10_images())
st.markdown(f"""#Today is a {preds} wave day""")
#get_10_images()
st.image(Image.open(BytesIO(images_for_prediction[2])))
st.image(Image.open(BytesIO(images_for_prediction[9])))
