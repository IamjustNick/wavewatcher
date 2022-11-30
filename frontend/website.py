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
add_bg_from_local('/home/mateuszcezary/code/iamjustnick/wavewatcher/frontend/5423150-beach-water-sea-wave-ocean-sand-sandy-wafe-looking-down-from-above-tide-ripple-seashore-shoreline-shore-split-symmetrical-yellow-sand-crashing-wafe-clear-water-free-pictures.jpg')


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
    images_for_prediction.clear()
    while len(images_for_prediction) < 10:
        response = requests.get(url = url, stream = True)
        #img = Image.open(BytesIO(response.content))
        images_for_prediction.append(response.content)
        my_bar.progress(len(images_for_prediction)*10)
        sleep(0.1)



st.button("Get prediction!", on_click= get_10_images())
#get_10_images()
st.image(Image.open(BytesIO(images_for_prediction[2])))
st.image(Image.open(BytesIO(images_for_prediction[9])))
