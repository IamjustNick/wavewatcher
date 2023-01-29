import numpy as np
import cv2
import requests
from PIL import Image
from io import BytesIO
import numpy as np

def get_images(number : int):
    #Calling the api several times
    imgs = []
    url = "https://oceans-uy3hohwooq-no.a.run.app/honey"
    for _ in range(number):
        try:
            response = requests.get(url = url)
            print(response.status_code)
            #will investigate
            #img = np.frombuffer(response.content , dtype = np.uint8)
            #success , img_encoded = cv22.imencode(".png" , img)

            img = Image.open(BytesIO(response.content))
            arr_img = np.array(img)
            arr_img = cv2.cvtColor( arr_img , cv2.COLOR_RGBA2GRAY)
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
    img = cv2.resize(cropped,(reshape_size,reshape_size),interpolation = cv2.INTER_AREA)
    img = cv2.medianBlur(img,5)
    _ ,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                cv2.THRESH_BINARY,11,2)
   # No normalization
    images =[th1,img,th2]
    images = np.array(images).T
    return images
