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
#from colorama import Fore,Style
from streamlit_autorefresh import st_autorefresh

import streamlit as st
from google.oauth2 import service_account
from google.cloud import storage

#----------Function for adding a background image------------------------------
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
add_bg_from_local('backgroundphoto.jpg')

#----------Credentials for using Google Cloud storage -------------------------
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"])
client = storage.Client(credentials=credentials)


#---------- Retriving contents from csv file in Google Cloud Storage ----------

#Uses st.experimental_memo to only rerun when the query changes or after 1 hour
@st.experimental_memo(ttl=3600)
def read_file(bucket_name, file_path):
    bucket = client.bucket(bucket_name)
    #Content is retrived as a string
    content = bucket.blob(file_path).download_as_string().decode("utf-8")
    return content

bucket_name = "waves_surfer_data"
file_path = "yourmom.csv"

content = read_file(bucket_name, file_path)

#Getting a dictionary from a CSV file that is inside our Google bucket
# dict1 = {}
# for line in content.strip().split("\n"):
#     playa, time, prediction = line.split(";")
#     dict1[playa] = prediction



#The code below is for buttons customisation
m = st.markdown("""
<style>
div.stButton > button:first-child color: #4F8BF9;
border-radius: 40%;
backgroud-color: #00ff00;
height: 60em;
width: 120em;}
</style>""", unsafe_allow_html=True)


#----------Code for an API request done by Louis ------------------------------
response = requests.get(api, params=params)
prediction = response.json()["prediction"]
if st.button('Get the prediction'):
    if prediction == "Good":
        st.write('Cowabunga!! Today is a great day to rip some waves!')
    if prediction == "Chaotic":
        st.write('Too gnarly conditions to surf today my dudes and dudettes. Do not worry, better waves in the future!')
    if prediction == "Flat":
        st.write('No waves today, however do not worry, there are a million waves in the world, one will be right for you')


#----------Division of the page into 3 columns by Louis ------------------------
columns = st.columns(3)
columns[0].button("PREDICTION FOR PATOS")
columns[0].write(dict1["Patos"])
#columns[0].image(..)
columns[1].button("PREDICTION FOR ZARAUTZ")
columns[1].write(dict1["Zarautz"])
#columns[1].image(..)
columns[2].button("PREDICTION FOR HAWAI")
columns[2].write(dict1["Hawai"])
#columns[2].image(..)
st.markdown("## Give our model a try:")
#st.set_option('deprecation.showfileUploaderEncoding', False)
#uploaded_file = st.file_uploader("## Give our model a try")
#if uploaded_file is not None:
    #data = pd.read_csv(uploaded_file)
    #st.write(data)


#This code just calls API and shows the picture
st.markdown("""# Welcome to WaveWatcher!
## Done by Nico, Mateo, Miguel and Louis""")

#-----An old functioni that was taking images from Nicole's API----------------
#my_bar = st.progress(0)
#images_for_prediction = []


# def get_10_images():
#     #Calling the api several times
#     images_for_prediction.clear()
#     while len(images_for_prediction) < 20:
#         response = requests.get(url = url, stream = True)
#         #img = Image.open(BytesIO(response.content))
#         images_for_prediction.append(response.content)
#         my_bar.progress(len(images_for_prediction)*5)
#         sleep(2)
#     return images_for_prediction

# X_pred = get_images_preprocessed(images_for_prediction)
# X,y = fetch_train_images()
# preds = predict_10(X,y,X_pred)

#st.button("Get prediction!", on_click= get_10_images())
#st.markdown(f"""#Today is a {preds} wave day""")
#get_10_images()
#st.image(Image.open(BytesIO(images_for_prediction[2])))
