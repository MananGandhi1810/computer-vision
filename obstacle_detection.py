import cv2
import math

cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = (0, 29, 10)
    upper = (68, 148, 164)
    mask = cv2.inRange(hsv, lower, upper)
    white = cv2.bitwise_and(frame, frame, mask=mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        area = cv2.contourArea(max(contours, key=cv2.contourArea))
        if area > 1000:
            cv2.putText(frame, "Obstacle Detected", (10, 75), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 2)
            max_contour = max(contours, key=cv2.contourArea)
            polygon = cv2.approxPolyDP(
                max_contour, 0.01 * cv2.arcLength(max_contour, True), True
            )
            cv2.drawContours(frame, [polygon], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(polygon)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            center = (x + w // 2, y + h // 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            cv2.line(frame, center, (frame.shape[1] // 2, frame.shape[0]), (0, 0, 255), 2)
    cv2.imshow("Obstacle Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break