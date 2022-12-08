import streamlit as st
import base64
import numpy as np
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from google.oauth2 import service_account
from google.cloud import storage
import asyncio
import aiohttp
from datetime import datetime
import plotly.express as px
import os
import pandas as pd
import pytz
import json
import plotly.graph_objects as go

timezone = pytz.timezone("Europe/Madrid")
base_url = "https://wavewatcher-uy3hohwooq-ez.a.run.app/predict"

if "past_data" not in st.session_state:
    st.session_state["past_data"] = pd.DataFrame()

if "fig" not in st.session_state:
    st.session_state["fig"] = None

if "message" not in st.session_state:
    st.session_state["message"] = ""

if "show" not in st.session_state:
    st.session_state["show"] = False

def fetch_data(session , images):
    return session.get(base_url, params={"num_images": images})


#----------Function for adding a background image------------------------------
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://github.com/IamjustNick/wavewatcher/blob/master/wavewatcher/frontend_interface/backgroundimage.png?raw=true");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
add_bg_from_url()


#----------Credentials for using Google Cloud storage -------------------------
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"])
client = storage.Client(credentials=credentials)

#----------Async API Functions = Non Frozen UI -------------------------

def fetch_data(session, images : int , iterations : int):
    return session.get(base_url, params={"num_images": images})


async def get_requests(iterations : int = 2 , images : int = 8):
    async with aiohttp.ClientSession() as session:
        jobs = [fetch_data(session, images=images , iterations = iterations)]
        results = await asyncio.gather(*jobs)
        for r in results:
            prediction = await r.text()
        return prediction


async def plot_graph():
    ##store prediction
    data = pd.DataFrame(st.session_state["past_data"])
    #fig = px.line(df, x="time", y="prediction", title='Past Wave Conditions')
    linecolor = "rgba(255,255,0,1.0)"
    fig = go.Figure(data=go.Scatter(
        x=data["time"],
        y=data["prediction"],
        marker=dict(color=linecolor, symbol="circle-open"),
        line=dict(width=3, dash="dot", color=linecolor),
        hoverlabel=dict(
            font=dict(color=linecolor), bgcolor='black', bordercolor='black'),
        hovertemplate='<br>'.join(["<br>Total Reports: %{y}", "<extra></extra>"]),
        hoverinfo="none",
    ))
    fig.update_layout(title='Wavewatcher Reports',
                    hoverlabel=dict(bgcolor='black'),
                    hovermode="x unified",
                    paper_bgcolor="rgba(20,20,20,0.8)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    yaxis_title="Conditions",
                    title_x=0.5,
                    width=800,
                    height=500,
                    title_font=dict(size=30))
    fig.update_xaxes(showline=False,
                    linewidth=2,
                    showgrid=False,
                    linecolor='black',
                    gridcolor='black',
                    visible=True,
                    title_text="date",
                    showticklabels=True)
    fig.update_yaxes(showline=False,
                    showgrid=False,
                    linewidth=2,
                    linecolor='black',
                    showticklabels = False,
                    gridcolor='black',
                    zerolinecolor='rgba(0,0,0,0)')
    return fig


    # bucket_name = "waves_surfer_data"
    # file_path = "prediction/forecast.csv"

    # hour = csv.iloc[0,2]
    # hour2 = datetime.strptime(hour, '%H:%M:%S')
    # hour3 = str(hour2 + timedelta(hours=1)).split(" ")[1]

st.markdown("""# <span style='color:yellow; font-size:90px; font-family:Graphic'><center>WAVEWATCHER</center></span>
## <span style='color:white'>Choose your break:</span>""", unsafe_allow_html=True)


#----------Code for an API request done by Louis ------------------------------

def final_message(outcome : str) -> str:
    if outcome == "Good":
        return "<span style='color:white; font-size:40px; font-family:Monaco'>Cowabunga!! Today is a great day to rip some waves!</span>"
    elif outcome == "Chaotic":
        return "<span style='color:white; font-size:40px; font-family:Monaco'>Too gnarly conditions to surf now my dudes and dudettes. Better waves soon!</span>"
    elif outcome == "Flat":
        return "<span style='color:white; font-size:40px; font-family:Monaco'>No waves at the moment, however do not worry, there are a million waves in the world </span>"
    else:
        return "<span style='color:white; font-size:40px; font-family:Monaco'>Current conditions could not be checked atm.</span>"


def call():
    return requests.get(base_url)
def cron():
    scheduler = BackgroundScheduler()
    scheduler.add_job(call, 'interval', minutes=720)
    scheduler.start()

async def main():
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "wave_data.csv"))

    patos = Image.open(os.path.join(os.path.dirname(__file__), "patos.jpg"))
    new_patos = patos.resize((600, 400))

    zarautz =Image.open(os.path.join(os.path.dirname(__file__), "zarautz.jpg"))
    new_zarautz = zarautz.resize((600, 400))

    hawai = Image.open(os.path.join(os.path.dirname(__file__), "hawai.jpg"))
    new_hawai = hawai.resize((600, 400))

    col1 , col2 , col3 = st.columns(3)
    col1.image(new_patos)
    col2.image(new_zarautz)
    col3.image(new_hawai)

    with col1:
        patos_button = st.button("PREDICTION FOR PATOS")

    with col2:
        zarautz_button = st.button("PREDICTION FOR ZARAUZ")

    with col3:
        hawai_button = st.button("PREDICTION FOR HAWAI")

    if zarautz_button:
        with col2:
            st.markdown(
                f"""<span style='color:white; font-size:20px'><b> :rotating_light: :construction: :rotating_light::construction:  <span style='color:white'> Under Construction </span> :rotating_light: :construction: :rotating_light:</b></span>""",
                    unsafe_allow_html=True)

    if hawai_button:
        with col3:
            st.markdown(f"""<span style='color:white; font-size:20px'><b> :rotating_light: :construction: :rotating_light::construction:  <span style='color:white'> Under Construction </span> :rotating_light: :construction: :rotating_light:</b></span>""",
                                unsafe_allow_html=True)

    pred_maps = {"Chaotic": 3, "Good": 2, "Flat": 1}
    maps_pred = {3: "Chaotic", 2 : "Good" , 1 : "Flat"}

    if not patos_button:
        row = df.iloc[-1]
        prediction = maps_pred.get(row[0])
        date = row[1].split(" ")[0]
        time = row[1].split(" ")[1].split(".")[0]
        with col1:
            st.markdown(f"""<span style='color:white; font-size:20px'><b>The last prediction at: {date} {time}</b></span>
                     <p><span style='color:white; font-size:20px'><b>How were the waves: {prediction}</b></span></p>"""
                    , unsafe_allow_html=True)

    with col1:
        display = st.button("Display graph")
        hide = st.button("Hide graph")

    if hide:
        display = False

    if display:
        hide = False
        if st.session_state["fig"]:
            waves_timeline = st.plotly_chart(st.session_state["fig"])


    if patos_button:
        waiting_message = """<span style='color:yellow; font-size:40px'><b>Assessing conditions... (don't worry, it may take some time) </b></span>"""
        st.session_state["show"] = False

        prediction = json.loads(await get_requests()).get("prediction")
        data = {"prediction": pred_maps.get(prediction),
                    "time": datetime.now(timezone)   }

        st.session_state["message"] = final_message(prediction)

        new_data = pd.DataFrame(data, index=[0])

        if len(df) > 100:
            df.iloc[:98] = df.iloc[1:99]
            df.reset_index(drop=True , inplace=True)
            df.iloc[-1] = new_data
            df.to_csv(os.path.join(os.path.dirname(__file__) , "wave_data.csv"), index=False, mode="w+")
        else:
            pd.DataFrame(data , index=[0]).to_csv(os.path.join(os.path.dirname(__file__) , "wave_data.csv"),
                                                    index=False,
                                                    header=None,
                                                    mode="a+")
        st.session_state["past_data"] = df
        fig = await plot_graph()
        st.session_state["fig"] = fig
        st.success("It seems there are new data available!")
        st.markdown(st.session_state["message"] , unsafe_allow_html=True)
        cron()

#----------Cron Jobs ------------------------



if __name__ == "__main__":
    asyncio.run(main())
