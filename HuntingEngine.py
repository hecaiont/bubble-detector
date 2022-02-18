import numpy as np
import cv2
from PIL import ImageGrab

import time
import datetime

import pyautogui as pg








class HuntingEngine():

    def __init__(self, runType):
        self.runType = runType
        self.startTime = time.time()

        self.WindowOriginX = 1920
        self.WindowOriginY = 1080

        self.isReady = True


    
    
    def toOrigin(self):
        pg.moveTo(self.WindowOriginX, self.WindowOriginY)
        return 



    def main(self):
        
        # while self.isReady:

        self.toOrigin()
        pg.click(button='left')

        pg.press('tab')
        time.sleep(1)
        pg.press('1')
        time.sleep(1)
        pg.press('2')
        time.sleep(1)
        pg.press('3')








if __name__=='__main__':
    he = HuntingEngine('run')

    he.main()