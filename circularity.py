import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while 1:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    contours, hierarchy = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    ball_contours = []

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0:
            continue
        area = cv2.contourArea(contour)

        if area < 100:
            continue

        circularity = 4 * np.pi * (area / (perimeter**2))
        if circularity > 0.7:
            ball_contours.append(contour)

    marked_frame = cv2.drawContours(frame, ball_contours, -1, (0, 255, 0), 3)

    cv2.imshow("Edges", edges)
    cv2.imshow("Contoured Frame", marked_frame)
    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
