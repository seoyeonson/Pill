import os
import cv2
import pytesseract
import matplotlib.pyplot as plt
from PIL import Image

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 5000)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 5080)

if not cap.isOpened():
    print('Camera open failed!')
    exit()

frame = None

while True:
    _, frame = cap.read()
    if frame is None:
        break
    cv2.imshow('frame', frame)
    text2 = pytesseract.image_to_string(frame, lang='kor')
    if "처방" in text2.replace(' ', ''):
        break

    if cv2.waitKey(1) == 27:
        break
        
cap.release()
cv2.destroyAllWindows()

