def drawROI(img, c):
    cpy = img.copy()

    color = (0, 255, 255)

    for pt in c:
        cv2.circle(cpy, tuple(pt.astype(int)), 25, color, -1, cv2.LINE_AA)

    cv2.line(cpy, tuple(c[0].astype(int)), tuple(c[1].astype(int)), color, 2, cv2.LINE_AA)
    cv2.line(cpy, tuple(c[1].astype(int)), tuple(c[2].astype(int)), color, 2, cv2.LINE_AA)
    cv2.line(cpy, tuple(c[2].astype(int)), tuple(c[3].astype(int)), color, 2, cv2.LINE_AA)
    cv2.line(cpy, tuple(c[3].astype(int)), tuple(c[0].astype(int)), color, 2, cv2.LINE_AA)

    result = cv2.addWeighted(img, 0.3, cpy, 0.7, 0)

    return result

def onMouse(event, x, y, flags, param):
    global srcQuad, dragSrc, ptOld, src

    if event == cv2.EVENT_LBUTTONDOWN:
        for i in range(4):
            if cv2.norm(srcQuad[i] - (x, y)) < 25:
                dragSrc[i] = True
                ptOld = (x, y)
                break

    if event == cv2.EVENT_LBUTTONUP:
        for i in range(4):
            dragSrc[i] = False

    if event == cv2.EVENT_MOUSEMOVE:
        for i in range(4):
            if dragSrc[i]:
                dx = x - ptOld[0]
                dy = y - ptOld[1]

                srcQuad[i] += (dx, dy)

                cpy = drawROI(src, srcQuad)
                cv2.imshow('img', cpy)
                ptOld = (x, y)
                break

import sys
import numpy as np
import cv2

src = cv2.imread('testt4.jpg')
if src is None:
    print('Image open failed!')
    sys.exit()

h, w = src.shape[:2]
dw = 800
dh = round(dw * 297 / 210)  # A4 용지 크기: 210x297cm

cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.resizeWindow(winname='img', width=1080, height=1440)

srcQuad = np.array([[50, 50], [50, h-50], [w-50, h-50], [w-50, 50]], np.float32)
dstQuad = np.array([[0, 0], [0, dh-1], [dw-1, dh-1], [dw-1, 0]], np.float32)
dragSrc = [False, False, False, False]

disp = drawROI(src, srcQuad)

cv2.imshow('img', disp)
cv2.setMouseCallback('img', onMouse)

while True:
    key = cv2.waitKey()
    if key == 13:  # ENTER 키
        break
    elif key == 27:  # ESC 키
        cv2.destroyWindow('img')
        sys.exit()

pers = cv2.getPerspectiveTransform(srcQuad, dstQuad)
dst = cv2.warpPerspective(src, pers, (dw, dh), flags=cv2.INTER_CUBIC)

cv2.imshow('dst', dst)
cv2.waitKey() # 아무 키나 눌러도 모든 윈도우가 닫힘.
cv2.destroyAllWindows()

