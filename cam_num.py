import cv2

for i in range(10):
    cam = cv2.VideoCapture(i)
    if cam.isOpened():
        print(f"Camera number {i} is available")
        cam.release()