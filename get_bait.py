import cv2
import numpy as np
import pyautogui
import time

'''
# screenshot bait
time.sleep(1)

im1 = pyautogui.screenshot('image/bait01.png', region=(600, 300, 2600, 1200))
im1 = cv2.cvtColor(np.array(im1), cv2.COLOR_RGB2BGR)
print(type(im1))
cv2.imshow('im1', im1)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''




img = cv2.imread('./image/bait01.png', 1)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

print(hsv.shape)

# print(hsv[230:350, 1400:1600, :].shape)

# hsv = hsv[230:350, 1400:1600, :]
# print(hsv.shape)


# hsv = cv2.circle(hsv, (73, 70), radius=1, color=(0, 0, 255), thickness=-1)
# print(hsv[73, 70, :])

# cv2.imshow('img', hsv)
# cv2.waitKey(0)

# cv2.destroyAllWindows()


# [ 25 121  61]

# water color mask range
lower_bound = np.array([0, 170, 170])
upper_bound = np.array([50, 250, 250])

lower_bound = np.array([161, 155, 84])
upper_bound = np.array([179, 255, 255])

mask = cv2.inRange(hsv, lower_bound, upper_bound)
# mask = cv2.inRange(rgb, lower_bound, upper_bound)

# kernel = np.ones((5,5), np.uint8)
# mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
# mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)


red = cv2.bitwise_and(frame, frame, mask=mask)

# contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


print(mask)
print(type(mask))

print(mask.shape)


x1 = (min(np.nonzero(mask)[1]))
x2 = (max(np.nonzero(mask)[1]))

y1 = (min(np.nonzero(mask)[0]))
y2 = (max(np.nonzero(mask)[0]))




cv2.rectangle(hsv, (x1, y1), (x2, y2), (0,255,0), 2)
# cv2.rectangle(rgb, (x1, y1), (x2, y2), (0,255,0), 2)

cv2.imshow('mask', mask)
cv2.imshow('img', hsv)
# cv2.imshow('img', rgb)

cv2.waitKey(0)

cv2.destroyAllWindows()

