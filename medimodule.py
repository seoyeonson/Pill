from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import pickle
import cv2
import os
from matplotlib import pyplot as plt
import io
from google.cloud import vision
from PIL import Image
import json
import pandas as pd

def medisearch():
    path ='C:/DevRoot/tablet_image_search-master/Code/final_image/circle_blue/140.png'

    # 이미지를 로드합니다
    img = cv2.imread(path)

    # 분류를 위한 이미지 전처리를 수행합니다
    image = cv2.resize(img, (280, 160))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    # 학습된 네트워크와 `MultiLabelBinarizer`를 로드합니다
    model = load_model("./medi_data/model.h5")
    mlb = pickle.loads(open("./medi_data/labelbin", "rb").read())

    # 이미지에 대한 분류를 수행한 후, 
    # 확률이 가장 높은 두 개의 클래스 라벨을 찾습니다
    # print("[INFO] classifying image...")
    proba = model.predict(image)[0]
    idxs = np.argsort(proba)[::-1][:4]


    for (i, j) in enumerate(idxs):
        label = "{}: {:.2f}%".format(mlb.classes_[j], proba[j] * 100)


    first_acc=mlb.classes_[idxs[0]]
    second_acc=mlb.classes_[idxs[1]]
    third_acc=mlb.classes_[idxs[2]]
    fourth_acc=mlb.classes_[idxs[3]]

    tablet_shape=[]
    tablet_color=[]

    tablet_shape_labels=['a hemicyclea semicircle','circle','diamond','ellipse','hexagon','octagon','pentagon',
    'rectangle','tetragon','triangle']
    tablet_color_labels=['black','blue','blue, light','blue, transparency','bluish green','bluish green, transparency','brown',
    ' brown, transparency','dark blue','dark blue','transparency','gray','green','green, transparency',
    'orange','orange, transparency','pink','pink, deep','pink, light','pink, transparency','purple',
    'purple, transparency','red','red, transparency','transparency','white','white, blue','white, brown',
    'white, green','white, red','white, transparency','white, yellow','wine','wine, transparency','yellow',
    'yellow, transparency','yellowish green','yellowish green, transparency']


    for idx in range(4) :
        if mlb.classes_[idxs[idx]] in tablet_shape_labels :
            tablet_shape.append(mlb.classes_[idxs[idx]])

        elif mlb.classes_[idxs[idx]] in tablet_color_labels :
            tablet_color.append(mlb.classes_[idxs[idx]])


    #google API 환경설정 및 실행

    with io.open(path, 'rb') as image_file:    
        content = image_file.read()

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] ='C:/DevRoot/project-ocr-355006-8c11c19495f5.json'

    client = vision.ImageAnnotatorClient()


    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    search_word=texts[1].description

    df1=pd.read_csv('./medi_data/공공데이터개방_낱알식별목록_re.csv',encoding = 'cp949')

    check1 = df1[(df1['의약품제형']==tablet_shape[0]) & (df1['색상앞']==tablet_color[0])]  
    check2 = check1[(check1['표시앞']==search_word) | (check1['표시뒤']==search_word) | (check1['표시앞']==search_word.replace(' ','')) | (check1['표시뒤']==search_word.replace(' ','')) | (check1['표시앞']==search_word.replace('\n',' ')) | (check1['표시뒤']==search_word.replace('\n',' '))]

    check2.to_json('medi.json', orient='table')

    with open('medi.json') as json_file:
        json_data = json.load(json_file)

    tablet_name = json_data["data"][0]["품목명"]
    tablet_function = json_data["data"][0]["분류명"]

return tablet_name