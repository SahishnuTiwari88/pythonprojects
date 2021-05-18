#Project 1 : VIRTUAL PAINT
import cv2
import numpy as np
frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture(0)  # video from webcam
cap.set(3,frameWidth)  # width=640 at id number 3   and this is
# used to resize or setting video size on laptop screen
cap.set(4,frameHeight)  # heigth=480 at id number 4
cap.set(10,150) # for change brightness id = 10 and value 100

myColors = [[5,107,0,19,255,255],
            [133,56,0,159,156,255],
            [57,76,0,100,255,255],
            [90,48,0,118,255,255]] # list of all colors to find matching one

myColorValues = [[51,153,255],
                 [255,0,255],
                 [0,255,0],
                 [255,0,0]] # list of colors to define corresponding value of myColors
                     # colors are in BGR format

myPoints =  []  #[x ,y ,colorId] ,we loop through myPoints & every time we can check value of x,y & we can draw circle of the color given by colorId at this point



def findColor(img,myColors,myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints=[]
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x,y = getContours(mask)
        cv2.circle(imgResult,(x,y),10,myColorValues[count],cv2.FILLED) #center of bounding box not contour
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count +=1
        #cv2.imshow(str(color[0]),mask)
    return newPoints

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        Area = cv2.contourArea(cnt)
       # print(Area)

        # now check for minimum area
        if Area>500:
            #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3) # to check area of each image
            # Now calculate curve length it helps us to approx. corners of our images shape
            peri = cv2.arcLength(cnt,True)

            approx = cv2.approxPolyDP(cnt,0.02*peri,True)   # to approx corner points i.e. how many corner points we have,we use True to show condition that all images are closed
            #print(approx) # it gives us corner point of each shapes

            x,y,w,h = cv2.boundingRect(approx) # it gives x,y,width,height each of objects shape
    return x+w//2,y
def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)


while True:
    success,img = cap.read()
    imgResult = img.copy() # image with all final information on it
    newPoints = findColor(img,myColors,myColorValues)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)

    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValues)

    cv2.imshow("Result",imgResult)
    if cv2.waitKey(1) & 0xFF == ord('d'):
        break
