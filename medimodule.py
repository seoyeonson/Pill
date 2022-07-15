import numpy as np
import argparse
import imutils
import pickle
import cv2
import base64

from matplotlib import pyplot as plt
import io
from google.cloud import vision
from PIL import Image
import json
import pandas as pd

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from keras.preprocessing.image import img_to_array
from keras.models import load_model

from VisionAPI.key_path import CREDENTIAL_PATH

def medisearch(img):
    kernel_sharpen_1 = np.array(
            [[-1, -1, -1, -1, -1], [-1, 2, 2, 2, -1],[-1, 2, 8, 2, -1],[-1, 2, 2, 2, -1],[-1, -1, -1, -1, -1]]) / 8.0
    # 이미지를 로드합니다
    # img = cv2.imread(path)
    img_temp = base64.b64decode(img)
    img_array = np.fromstring(img_temp, np.uint8)
    image_arr = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    # image_arr = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)


    # gray scale
    img_gray = cv2.cvtColor(image_arr,cv2.COLOR_BGR2GRAY)

    # 흐리게
    img_blur = cv2.GaussianBlur(img_gray,(5,5),0)
    # 외곽선
    img_can = cv2.Canny(img_blur,25,200,L2gradient=True)

    # 선명하게
    img_canny = cv2.filter2D(img_can,-1,kernel_sharpen_1)


    contours,_ = cv2.findContours(
        img_canny, # image
        cv2.RETR_EXTERNAL, # mode
        cv2.CHAIN_APPROX_NONE, # method
    )
    # 외곽선 그리기
    # img_fill = cv2.drawContours(image,contours,-1,(0,255,0),3)

    contours_xy = np.array(contours)
    # contours_xy.shape

    # x의 min과 max 찾기
    x_min, x_max = 0,0
    value = list()
    for i in range(len(contours_xy)):
        for j in range(len(contours_xy[i])):
            value.append(contours_xy[i][j][0][0]) #네번째 괄호가 0일때 x의 값
            x_min = min(value)
            x_max = max(value)


    # y의 min과 max 찾기
    y_min, y_max = 0,0
    value = list()
    for i in range(len(contours_xy)):
        for j in range(len(contours_xy[i])):
            value.append(contours_xy[i][j][0][1]) #네번째 괄호가 0일때 x의 값
            y_min = min(value)
            y_max = max(value)


    x = x_min
    y = y_min
    w = x_max-x_min
    h = y_max-y_min
    img_trim = image_arr[y:y+h, x:x+w] # 잘려진 알약 이미지 
    print(x)


    # cv2.imshow('dst', img_trim)

    # cv2.waitKey()
    # cv2.destroyAllWindows()
    # 분류를 위한 이미지 전처리를 수행합니다
    image = cv2.resize(img_trim, (280, 160))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image_array = np.expand_dims(image, axis=0)

    # 학습된 네트워크와 `MultiLabelBinarizer`를 로드합니다
    model = load_model("./medi_data/model.h5 ")
    mlb = pickle.loads(open("./medi_data/labelbin", "rb").read())


    # 이미지에 대한 분류를 수행한 후, 
    # 확률이 가장 높은 두 개의 클래스 라벨을 찾습니다
    # print("[INFO] classifying image...")
    proba = model.predict(image_array)[0]
    idxs = np.argsort(proba)[::-1][:4]

    # for (i, j) in enumerate(idxs):
    #     label = "{}: {:.2f}%".format(mlb.classes_[j], proba[j] * 100)

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

    print('shape: ', tablet_shape)
    print('color: ', tablet_color)


    #google API 환경설정 및 실행

    content = img

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIAL_PATH

    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    search_word=texts[0].description
    print('약에 적힌 문자: ', search_word)

    df1=pd.read_csv('./medi_data/공공데이터개방_낱알식별목록_re.csv',encoding = 'cp949')
    print(tablet_shape[0],tablet_color[0])
    tablet_name = None
    try:
        check1 = df1[(df1['의약품제형']==tablet_shape[0]) & (df1['색상앞']==tablet_color[0])]  #### 수정
        print('check1: ', check1)
        check2 = check1[(check1['표시앞']==search_word) | (check1['표시뒤']==search_word) | (check1['표시앞']==search_word.replace(' ','')) | (check1['표시뒤']==search_word.replace(' ','')) | (check1['표시앞']==search_word.replace('\n',' ')) | (check1['표시뒤']==search_word.replace('\n',' '))  | (check1['표시앞']==search_word.replace('\n','')) | (check1['표시뒤']==search_word.replace('\n',''))]
        print('check2: ', check2)

        tablet_name = check2['품목명'].iloc[0]
    except Exception as ex:
        print(ex)
        return None
        
    if tablet_name == None:
        return None

    # with open('medi.json') as json_file:
    #     json_data = json.load(json_file)

    # print(json_data)
    # tablet_name = json_data["data"][0]["품목명"]
    # tablet_function = json_data["data"][0]["분류명"]
    print(tablet_name)

    return tablet_name, image_arr