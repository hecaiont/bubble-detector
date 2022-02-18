import cv2
import numpy as np

img = cv2.imread('./image/WoWScrnShot_060621_225852.jpg', 1)



hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# water color mask range
lower_bound = np.array([90, 120, 0])
upper_bound = np.array([110, 130, 255])

mask = cv2.inRange(hsv, lower_bound, upper_bound)

kernel = np.ones((5,5), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)


# contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


print(mask)
print(type(mask))

print(mask.shape)


x1 = (min(np.nonzero(mask)[1]))
x2 = (max(np.nonzero(mask)[1]))

y1 = (min(np.nonzero(mask)[0]))
y2 = (max(np.nonzero(mask)[0]))




cv2.rectangle(hsv, (x1, y1), (x2, y2), (0,255,0), 2)

cv2.imshow('mask', mask)
cv2.imshow('img', hsv)

cv2.waitKey(0)

cv2.destroyAllWindows()