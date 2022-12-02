import numpy as np
import cv2 as cv
import requests
from PIL import Image
from io import BytesIO
import numpy as np


def get_images(number : int):
    #Calling the api several times
    imgs = []
    url = "https://oceanbees-xbzgoqiv5a-ew.a.run.app/honey"
    for _ in range(number):
        try:
            response = requests.get(url = url)
            print(response.status_code)
            #will investigate
            #img = np.frombuffer(response.content , dtype = np.uint8)
            #success , img_encoded = cv2.imencode(".png" , img)

            img = Image.open(BytesIO(response.content))
            arr_img = np.array(img)
            arr_img = cv.cvtColor( arr_img , cv.COLOR_RGBA2GRAY)
            imgs.append(arr_img)
            print("all good here")
        except Exception:
            print("WOOPS! Are you sure you are doing everything ok?")
            continue
    return np.array(imgs)

def preprocess_image_lite(image, reshape_size=300):
    if image.shape == (570, 1015):
        cropped = image[250:-100,100:]
    elif image.shape == (582, 1034):
        cropped = image[60:500,:]
    elif image.shape == (624, 1200):
        cropped = image[150:,:]
    elif image.shape == (624, 1110):
        cropped = image[350:-100,:]
    else:
        cropped = image[150:,:]
    img = cv.resize(cropped,(reshape_size,reshape_size),interpolation = cv.INTER_AREA)
    img = cv.medianBlur(img,5)
    ret,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
    th2 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,\
                cv.THRESH_BINARY,11,2)
   #This change is unique to inputs from an online camera
    images =[th1,img,(th2/255)]

    return images



def majority_voting(predictions):
    labels = {0:"Chaotic" , 1:"Good",2:"Flat"}
    _ , counts = np.unique(predictions , return_counts=True)
    return labels.get(np.argmax(counts))

def return_outcome(chaotic,good,flat):
    if flat >chaotic and flat > good:
        return 2
    elif chaotic > flat and chaotic > good:
        return 0
    elif good > flat and good > chaotic:
        return 1
    else:
        return "invalid"

def predictions_time(model, results):
    processed_images = []
    outcomes = []
    for result in results:
        proc = preprocess_image_lite(result, 300)
        processed_images.append(np.array([(proc)]).reshape(1,300,300,3))
    for image in processed_images:
        prediction = model.predict(image)
        outcomes.append(prediction)
        return outcomes
