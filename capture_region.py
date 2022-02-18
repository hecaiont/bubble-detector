import numpy as np
import cv2
from PIL import ImageGrab

import time
import datetime

import pyautogui as pg

# from pywinauto import Application

class ScreenImage():

    def __init__(self):
        self.now = datetime.datetime.now()
        self.imageList = []
        self.WindowZeroPointX = 300
        self.WindowZeroPointY = 300
        self.WindowCaptureW = 1100
        self.WindowCaptureH = 600
        self.imageLen = 10
        self.gdifferenceLen = 10
        self.gdifferenceList = [0.0, 0.0]
        self.meanDifferenceValue = 0.0

        self.CastingBarRegionX = 540
        self.CastingBarRegionY = 640
        self.CastingBarRegionW = 730 - self.CastingBarRegionX
        self.CastingBarRegionH = 660 - self.CastingBarRegionY

        # for Wailing Caverns
        self.CatchValue = 150 # over
        self.BaitValue = 50 # over
        self.WaterValue = 20 # under        

    # def ngrabImg(self):
    #     self.app = Application().connect(title_re=".*World of Warcraft")
    #     hwin = self.app.top_window()
    #     hwin.set_focus()
    #     self.img = hwin.capture_as_image()
    #     self.imageList.append(self.img)

    #     if len(self.imageList) == self.imageLen:
    #         self.imageList.pop(0)
    #         # print('delete img 0')
        
    #     return self.imageList


    def grabImg(self):
        # self.img = ImageGrab.grab(bbox=(0, 0, 1300, 800)) #x, y, w, h    
        # self.img = ImageGrab.grab(bbox=(0, 0, 1300, 600)) #x, y, w, h    
        self.img = ImageGrab.grab(bbox=(self.WindowZeroPointX, self.WindowZeroPointY, self.WindowCaptureW, self.WindowCaptureH)) #x, y, w, h    
        self.imageList.append(self.img)
        # print('append img')
        # print(len(self.imageList))

        if len(self.imageList) == self.imageLen:
            self.imageList.pop(0)
            # print('delete img 0')
        
        return self.imageList


    def lastPoint(self, maxValue, location):
        self.lastMaxValue = maxValue
        self.lastLocation = location

        print(self.lastMaxValue)
        print(self.lastLocation)
        

    def trackDifference(self, gdifference):
        self.gdifferenceList.append(gdifference)

        if len(self.gdifferenceList) == self.gdifferenceLen:
            self.gdifferenceList.pop(0)

        self.meanDifferenceValue = self.meanDifference()



    def meanDifference(self):
        return np.mean(self.gdifferenceList)
    

currentImg = ScreenImage()


while True:
    imgList = currentImg.grabImg()
    # imgList = currentImg.ngrabImg()
        
    # print('!start>>>')
    # print(currentImg.meanDifferenceValue)
    # print('--')
    # print(currentImg.WaterValue)
    # print('<<<end!')
        
    if len(imgList) > 1:
        mat1 = np.array(imgList[-1])
        mat2 = np.array(imgList[-2])

        gmat1 = cv2.cvtColor(mat1, cv2.COLOR_BGR2GRAY)
        gmat2 = cv2.cvtColor(mat2, cv2.COLOR_BGR2GRAY)

        gdifference = cv2.subtract(gmat1, gmat2)
        
        currentImg.trackDifference(gdifference.max())


        print('-------')
        # # print(gdifference.shape)
        # print(gdifference.max())
        # # print(np.where(gdifference == gdifference.max()))
        
        # # print(gdifference.min())
        # # print(np.where(gdifference == gdifference.min()))
        # print('-------')

        # print(np.where(gdifference == gdifference.max())[0], np.where(gdifference == gdifference.max())[1])


        if len(np.where(gdifference == gdifference.max())[0]) > 1:
            

            ptx1 = np.where(gdifference == gdifference.max())[1].min()
            ptx2 = np.where(gdifference == gdifference.max())[1].max()
            pty1 = np.where(gdifference == gdifference.max())[0].min()
            pty2 = np.where(gdifference == gdifference.max())[0].max()


            currentImg.lastPoint(gdifference.max(), ((ptx1+ptx2)//2, (pty1+pty2)//2))


            # print(ptx1, pty1)
            # print(ptx2, pty2)

            if gdifference.max() > currentImg.CatchValue:
                cv2.rectangle(gmat1, (ptx1, pty1), (ptx2, pty2), (0, 0, 255), 3)
                pg.moveTo((ptx1+ptx2)//2+300, (pty1+pty2)//2+300)
                time.sleep(1)
                pg.click(button='right')
                time.sleep(1)
                pg.press('0')


            if currentImg.meanDifferenceValue < currentImg.WaterValue:
                # pg.press('1')
                # time.sleep(0.1)
                # pg.press('2')
                # time.sleep(0.1)
                # pg.press('3')
                # time.sleep(0.1)
                # pg.press('4')
                # time.sleep(0.1)
                # pg.press('5')
                # time.sleep(0.1)
                # pg.press('6')
                # time.sleep(0.1)
                # pg.press('7')
                # time.sleep(0.1)

                pg.press('0')
        
        elif len(np.where(gdifference == gdifference.max())[0]) == 1:
            
            ptx = np.where(gdifference == gdifference.max())[1][0]
            pty = np.where(gdifference == gdifference.max())[0][0]
            
            currentImg.lastPoint(gdifference.max(), (ptx, pty))

            if gdifference.max() > 150:
                cv2.rectangle(gmat1, (ptx-2, pty-2), (ptx+2, pty+2), (0, 0, 255), 3)
                pg.moveTo(ptx+300, pty+300)
                time.sleep(1)
                pg.click(button='right')
                time.sleep(1)
                pg.press('0')

        else:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')



        # cv2.imshow('gdifference', gdifference)
        cv2.imshow('mark', gmat1)


    if cv2.waitKey(1) & 0Xff == ord('q'):
        break

    time.sleep(0.3)
    
cv2.destroyAllWindows()