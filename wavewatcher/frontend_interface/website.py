import json
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

import streamlit as st
from streamlit_lottie import st_lottie
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
add_bg_from_local('backgroundimage.png')



#---------- Animations from LottieFiles ------------------------------------
# def load_lottieurl(url: str):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()

# lottie_construction_url = "https://assets2.lottiefiles.com/packages/lf20_RkWAMt.json"
# lottie_json = load_lottieurl(lottie_construction_url)


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


csv = pd.read_csv('gs://waves_surfer_data/prediction/forecast.csv')
bucket_name = "waves_surfer_data"
file_path = "prediction/forecast.csv"

content = read_file(bucket_name, file_path)

#Getting a dictionary from a CSV file that is inside our Google bucket
# dict1 = {}
# list1 = []
# for line in content.strip().split("\n"):
#     list1.append(line)
    # prediction, time, time = line.split(",")
    # dict1[playa] = prediction

st.markdown("""# <span style='color:yellow; font-size:90px; font-family:Graphic'><center>WAVEWATCHER</center></span>
## <span style='color:white'>Choose your break:</span>""", unsafe_allow_html=True)

#----------Code for an API request done by Louis ------------------------------
api = "https://wavewatcher-uy3hohwooq-ez.a.run.app/predict?num_images=15"


def final_message(outcome):
    if outcome == "Good":
        st.markdown(f"<span style='color:white; font-size:20px'>Cowabunga!! Today is a great day to rip some waves!</span>", unsafe_allow_html=True)
    if outcome == "Chaotic":
        st.markdown(f"<span style='color:white; font-size:20px'>Too gnarly conditions to surf today my dudes and dudettes. Do not worry, better waves in the future!</span>", unsafe_allow_html=True)
    if outcome == "Flat":
        st.markdown(f"<span style='color:white; font-size:20px'>No waves today, however do not worry, there are a million waves in the world, one will be right for you", unsafe_allow_html=True)


patos = Image.open("patos.jpg")
new_patos = patos.resize((600, 400))

zarautz =Image.open("zarautz.jpg")
new_zarautz = zarautz.resize((600, 400))

hawai = Image.open("hawai.jpg")
new_hawai = hawai.resize((600, 400))
#----------Division of the page into 3 columns by Louis ------------------------


columns = st.columns(3)
# with columns[0]:
#     if st.button("PREDICTION FOR PATOS"):
#         st.write('test')
columns[0].image(new_patos)
if columns[0].button("PREDICTION FOR PATOS"):
    response = requests.get(api)
    prediction = response.json()
    final_message(prediction['prediction'])
columns[0].markdown(f"<span style='color:white; font-size:20px'><b>The latest prediction at: {csv.iloc[0,2]}</b></span>", unsafe_allow_html=True)
columns[0].markdown(f"<span style='color:white; font-size:20px'><b>How were the waves: {csv.iloc[0,1]}</b></span>", unsafe_allow_html=True)

columns[1].image(new_zarautz)
with columns[1]:
    if columns[1].button("PREDICTION FOR ZARAUTZ"):
        st.markdown(f"""## :rotating_light: :construction: :rotating_light::construction:  <span style='color:white'> Under Construction </span> :rotating_light: :construction: :rotating_light::construction:
        """, unsafe_allow_html=True)

columns[2].image(new_hawai)
with columns[2]:
    if columns[2].button("PREDICTION FOR HAWAI"):
        st.markdown(f"""## :rotating_light: :construction: :rotating_light::construction:  <span style='color:white'> Under Construction </span> :rotating_light: :construction: :rotating_light::construction:
        """, unsafe_allow_html=True)
# with columns[1]:
#     if st.button("PREDICTION FOR ZARAUTZ"):
#         st.write('test2')
# #
# #columns[1].image(..)
# with columns[2]:
#     if st.button("PREDICTION FOR HAWAI"):
#         st.write('test3')
# #columns[2].write(dict1["Hawai"])
# #columns[2].image(..)


#st.set_option('deprecation.showfileUploaderEncoding', False)
#uploaded_file = st.file_uploader("## Give our model a try")
#if uploaded_file is not None:
    #data = pd.read_csv(uploaded_file)
    #st.write(data)

#-----An old function that was taking images from Nicole's API----------------
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
