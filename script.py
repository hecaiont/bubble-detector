# import cv2 as cv
# import numpy as np
# import pyautogui


# cv.namedWindow("result");
# cv.moveWindow("result", 0, 500);

# img_piece = cv.imread('dino.png', cv.IMREAD_COLOR)
# h,w = img_piece.shape[:2]

# while 1:
#     pic = pyautogui.screenshot(region=(0, 0, 700, 500))
#     img_frame = np.array(pic)
#     img_frame  = cv.cvtColor(img_frame, cv.COLOR_RGB2BGR)
#     meth = 'cv.TM_CCOEFF'
#     method = eval(meth)


#     res = cv.matchTemplate(img_piece, img_frame, method)
#     min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
#     top_left = max_loc
#     bottom_right = (top_left[0] + w, top_left[1] + h)

#     cv.rectangle(img_frame, top_left, bottom_right, (0, 255, 0), 2)
#     print(max_val, top_left)

#     cv.imshow('result', img_frame)
    
#     key = cv.waitKey(1)
#     if key == 27:
#         break



import cv2
import numpy as np

from scipy.spatial import distance as dist


 
while True:

    frame = cv2.imread('./image/WoWScrnShot_060521_002358.jpg', cv2.IMREAD_COLOR)
 
    # Converting the image to grayscale.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('Frame', gray)

    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

 
# Closes all the frames
cv2.destroyAllWindows()