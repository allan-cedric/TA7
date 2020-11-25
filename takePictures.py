#!/usr/bin/env python3
import cv2

capture = cv2.VideoCapture(0)
cv2.namedWindow('Window', cv2.WINDOW_NORMAL)

success = True
count = 1
while success:
    success, image = capture.read()
    if success:

        cv2.imshow("Window", image)
        key=cv2.waitKey(5) & 0xFF

        if chr(key) == 's':
            cv2.imwrite("pictures/chessboard{}.png".format(count), image)
            count += 1