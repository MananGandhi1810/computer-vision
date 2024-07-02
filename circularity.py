import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while 1:
    ret, frame = cap.read()
    # frame = cv2.GaussianBlur(frame, cv2.)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    contours, hierarchy = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    marked_frame = cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0:
            continue
        area = cv2.contourArea(contour)
        
        circularity = 4 * np.pi * (area / (perimeter ** 2))
        print(circularity)


    cv2.imshow("Edges", edges)
    cv2.imshow("Contoured Frame", marked_frame)
    # cv2.imshow("Approx Frame", approx_contours)
    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
