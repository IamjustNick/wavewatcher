FROM tensorflow/tensorflow:latest

#WORKDIR /src

RUN apt-get update
#RUN apt-get install ninja-build libglib2.0-0 libsm6 libxrender-dev libxext6 libgl1-mesa-dev ffmpeg libsm6 libgl1 libgl1-mesa-glx libxext6 python3-opencv -y
#RUN apt-get install ninja-build libglib2.0-0 libsm6 libxrender-dev libxext6 libgl1-mesa-dev -y

FROM python:3.8.12-buster

WORKDIR /app

# libraries required by OpenCV
RUN apt-get update
RUN apt-get install \
  'ffmpeg'\
  'libsm6'\
  'libxext6'  -y


RUN echo "Hello World!"

COPY test.py test.py
RUN pip install opencv-python
RUN python test.py

COPY requirements.txt requirements.txt
COPY setup.py setup.py
COPY wavewatcher/api wavewatcher/api
COPY wavewatcher/__init__.py wavewatcher/__init__.py

RUN pip install --upgrade pip
RUN pip install .

CMD uvicorn wavewatcher.api.fast_api:app --host 0.0.0.0 --port $PORT
