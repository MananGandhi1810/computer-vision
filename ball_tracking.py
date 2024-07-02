import cv2
import numpy as np
import time

# import serial

time.sleep(2)

previous_command = b""
command = b""


def detect_and_encircle_ball(frame, area_threshold=1000, stop_threshold=15):
    global previous_command, command
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([0, 74, 38])
    upper_bound = np.array([179, 251, 174])
    #     lower_bound = np.array([0, 0, 0])
    #     upper_bound = np.array([0, 0, 0])
    #     lower_bound = np.array([0, 0, 0])
    #     upper_bound = np.array([0, 0, 0])
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    cv2.imshow("mask", mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    frame_width = frame.shape[1]
    center_line_1 = frame_width // 2 - 75
    center_line_2 = frame_width // 2 + 75
    line_height = frame.shape[0] - 25

    center_line_1 = int(center_line_1)
    center_line_2 = int(center_line_2)
    line_height = int(line_height)

    cv2.line(frame, (center_line_1, 0), (center_line_1, frame.shape[0]), (0, 0, 255), 2)
    cv2.line(frame, (center_line_2, 0), (center_line_2, frame.shape[0]), (0, 0, 255), 2)
    cv2.line(frame, (0, line_height), (frame_width, line_height), (0, 0, 255), 2)

    if not contours:
        cv2.putText(
            frame, "Rotate", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2
        )
        command = b"r"
    else:

        ball_contours = []
        for contour in sorted(contours, key=cv2.contourArea)[:10]:
            perimeter = cv2.arcLength(contour, True)
            if not perimeter:
                continue
            area = cv2.contourArea(contour)
            if area < 50:
                continue
            circularity = 4 * np.pi * (area / (perimeter**2))
            if circularity > 0.7:
                print(circularity)
                ball_contours.append(contour)
        cv2.drawContours(frame, ball_contours, -1, (0, 255, 0), 2)

        if len(ball_contours) == 0:
            return None

        largest_contour = max(ball_contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)

        if area > area_threshold:
            ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(frame, center, radius, (0, 255, 0), 2)

            if center_line_1 < center[0] < center_line_2:
                if y < line_height - stop_threshold:
                    cv2.putText(
                        frame,
                        "Move Forward",
                        (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2,
                    )
                    command = b"F"
                else:
                    cv2.putText(
                        frame,
                        "Stop",
                        (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2,
                    )
                    command = b"I"

                    time.sleep(6)
                cv2.putText(
                    frame,
                    "Center",
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )
            elif center[0] < center_line_1:
                cv2.putText(
                    frame, "Left", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
                )
                command = b"R"
            else:
                cv2.putText(
                    frame,
                    "Right",
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )
                command = b"L"

        if previous_command != command:
            pass
        previous_command = command

    return frame


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 20)

while True:
    ret, frame = cap.read()
    cv2.resize(frame, (50, 50), interpolation=cv2.INTER_LINEAR)
    result_frame = detect_and_encircle_ball(frame)
    if result_frame is None:
        continue
    cv2.imshow("Ball Detection", result_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        # ser.write(b"s")
        break

cap.release()
cv2.destroyAllWindows()
