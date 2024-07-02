import cv2
import numpy as np

lower = (94, 6, 163)
higher = (179, 172, 255)

cam = cv2.VideoCapture(0)
cam.set(3, 320)
cam.set(4, 240)

size = (320, 240)
threshold = 5

while True:
    ret, frame = cam.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, higher)
    white = cv2.bitwise_and(frame, frame, mask=mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.line(frame, (size[0] // 2, 0), (size[0] // 2, size[1]), (0, 0, 255), 2)
    if len(contours) > 0:
        max_contour = max(contours, key=cv2.contourArea)
        polygon = cv2.approxPolyDP(
            max_contour, 0.01 * cv2.arcLength(max_contour, True), True
        )
        cv2.drawContours(frame, [polygon], -1, (0, 255, 0), 2)
        total_left = 0
        total_right = 0
        for point in polygon:
            if point[0][0] < size[0] // 2 - threshold:
                total_left += 1
            elif point[0][0] > size[0] // 2 + threshold:
                total_right += 1
        print(total_left, total_right)
        if abs(total_left - total_right) < 1:
            print("Forward")
        elif total_left > total_right:
            print("Left")
        elif total_right > total_left:
            print("Right")
    images = np.hstack((frame, white))
    cv2.imshow("Line Following", images)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
