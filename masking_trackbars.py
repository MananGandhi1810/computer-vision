import cv2

cam = cv2.VideoCapture(0)

lowerh = 0
lowers = 0
lowerv = 0
upperh = 179
uppers = 255
upperv = 255

def updateLowerH(value):
    global lowerh
    lowerh = value
    print(lowerh)

def updateLowerS(value):
    global lowers
    lowers = value
    print(lowers)

def updateLowerV(value):
    global lowerv
    lowerv = value
    print(lowerv)

def updateUpperH(value):
    global upperh
    upperh = value
    print(upperh)

def updateUpperS(value):
    global uppers
    uppers = value
    print(uppers)

def updateUpperV(value):
    global upperv
    upperv = value
    print(upperv)

cv2.namedWindow("frame")
cv2.createTrackbar("LowerH", "frame", 0, 179, updateLowerH)
cv2.createTrackbar("LowerS", "frame", 0, 255, updateLowerS)
cv2.createTrackbar("LowerV", "frame", 0, 255, updateLowerV)
cv2.createTrackbar("UpperH", "frame", 0, 179, updateUpperH)
cv2.createTrackbar("UpperS", "frame", 0, 255, updateUpperS)
cv2.createTrackbar("UpperV", "frame", 0, 255, updateUpperV)

while True:
    print((lowerh, lowers, lowerv), (upperh, uppers, upperv))
    ret, frame = cam.read()
    cv2.imshow("frame", frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = (lowerh, lowers, lowerv)
    upper = (upperh, uppers, upperv)
    mask = cv2.inRange(hsv, lower, upper)
    white = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow("White", white)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break