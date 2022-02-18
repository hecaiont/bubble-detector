# https://stackoverflow.com/questions/64410486/draw-contours-around-images-of-the-same-color-with-opencv-python
# https://pythonprogramming.net/color-filter-python-opencv-tutorial/

import cv2
import numpy as np

img = cv2.imread('./image/WoWScrnShot_060521_002413.jpg', 1)



hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imshow('hsv', hsv)


lower_bound = np.array([90, 120, 0])
upper_bound = np.array([110, 130, 255])

mask = cv2.inRange(hsv, lower_bound, upper_bound)

kernel = np.ones((5,5), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)


contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


for contour in contours:
    x,y,w,h = cv2.boundingRect(contour)
    img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

# print(mask)

cv2.imshow('mask', mask)
# # cv2.imshow('img', img)

cv2.waitKey(0)

cv2.destroyAllWindows()