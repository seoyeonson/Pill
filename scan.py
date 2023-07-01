from io import BytesIO
import numpy as np
import cv2
import imutils
from PIL import Image
import base64

def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped


def order_points(pts):
	rect = np.zeros((4, 2), dtype = "float32")
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
	return rect


def scan_main(image):
    # ratio = image.shape[0] / 500.0
    # orig = image.copy()
    origin_image = image
    image = base64.b64decode(image)
    image = np.fromstring(image, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    print(image.shape)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            screenCnt = approx
            break
        else:
            return origin_image

    screenCnt.resize(4,2)
    dw = 800
    dh = round(dw * 297 / 210)  # A4 용지 크기: 210x297cm
    dstQuad = np.array([[0, 0], [0, dh-1], [dw-1, dh-1], [dw-1, 0]], np.float32)
    sum_ = screenCnt.sum(axis=1)
    diff = np.diff(screenCnt, axis=1)
    tl = screenCnt[np.argmin(sum_)]
    br = screenCnt[np.argmax(sum_)]
    tr = screenCnt[np.argmin(diff)]
    bl = screenCnt[np.argmax(diff)]

    pers = cv2.getPerspectiveTransform(np.array([tl, bl, br, tr], dtype=np.float32), dstQuad)
    dst = cv2.warpPerspective(image, pers, (dw, dh), flags=cv2.INTER_CUBIC)
    
    dst = Image.fromarray(dst)
    buff = BytesIO()
    dst.save(buff, format="PNG")
    result_img = base64.b64encode(buff.getvalue()).decode('utf-8')
    print(result_img[:100])
    print(type(result_img))

    return result_img

    # cv2.imshow('original', imutils.resize(image, height = 1080))
    # cv2.imshow('dst', imutils.resize(dst, height = 1080))
    # cv2.waitKey()
    # cv2.destroyAllWindows()
