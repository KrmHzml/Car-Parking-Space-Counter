import cv2
import numpy as np
import cvzone
import pickle

width, height = 108, 48  

cap = cv2.VideoCapture("carPark.mp4")

with open("carParkPos", "rb") as f:
    posList = pickle.load(f)

def check_parking_space( imgPro):
    spaceCounter = 0

    for pos in posList:
        
        x, y = pos
        cv2.rectangle(imgPro, pos, (pos[0]+width,pos[1]+height), (255,0,255), 2)

        cv2.imshow("frame", frame)
        #cv2.imshow("frameGray", frameGray)
        #cv2.imshow("frameThreshold", frameThreshold)
        #cv2.imshow("frameMedian", frameMedian)
        #cv2.imshow("frameDilate", frameDilate)

        imgCrop = imgPro[y:y+height, x:x+width]
        #cv2.imshow(str(x*y), imgCrop)

        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(frame, str(count), (x, y+height-10), scale=1, thickness=1, offset=0, colorR=(0,0,255))

        if count < 1000:
            color = (0,255,0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0,0,255)
            thickness = 1
        cv2.rectangle(frame, pos, (pos[0]+width,pos[1]+height), color, thickness)
        cvzone.putTextRect(frame,f"FREE {str(spaceCounter)}/{len(posList)}", (450,50), scale=2, thickness=5, offset=10, colorR=(0,255,0))

while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    ret, frame = cap.read()

    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frameBlur = cv2.GaussianBlur(frameGray, (3,3), 1)
    frameThreshold = cv2.adaptiveThreshold(frameBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    frameMedian = cv2.medianBlur(frameThreshold,5)
    kernel = np.zeros((3,3), np.uint8)
    frameDilate = cv2.dilate(frameMedian, kernel, iterations=1)

    check_parking_space(frameDilate)

    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()