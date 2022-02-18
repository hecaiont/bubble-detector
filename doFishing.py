import numpy as np
import cv2
from PIL import ImageGrab

import time
import datetime

import pyautogui as pg

class CaptureEngine():

    def __init__(self):
        '''
        ## defalut location for 1280x768
        self.WindowZeroPointX = 1200
        self.WindowZeroPointY = 700
        self.WindowCaptureW = 2400
        self.WindowCaptureH = 1400
        '''

        self.WindowZeroPointX = 1550
        self.WindowZeroPointY = 900
        self.WindowCaptureW = 2150
        self.WindowCaptureH = 1300

        self.isCapturable = True
        self.isFishing = False
        self.isBite = False
        self.Fullbag = False


        self.imageLen = 2
        self.gdifference = 0
        self.gdifferenceLen = 10
        self.meanDifferenceValue = 0.0

        self.imageList = []
        self.gdifferenceList = []
        self.gdifferenceMaxList = []
        self.differenceListStdList = []

        # gdifferenceSTD
        self.GDSList = []
        self.GDSListLen = 100
        

        # for Wailing Caverns
        self.CatchValue = 150 # over
        self.BaitValue = 50 # over
        self.WaterValue = 20 # under


    def defaultArea(self):
        # 600, 400
        self.WindowZeroPointX = 1550
        self.WindowZeroPointY = 900
        self.WindowCaptureW = 2150
        self.WindowCaptureH = 1300


    def baitArea(self, ptx1, ptx2, pty1, pty2):
        self.WindowZeroPointX = ptx1-100
        self.WindowZeroPointY = pty1-100
        self.WindowCaptureW = ptx2+100
        self.WindowCaptureH = pty2+100
        return self.WindowZeroPointX, self.WindowZeroPointY, self.WindowCaptureW, self.WindowCaptureH


    def grabImg(self):
        self.raw = ImageGrab.grab(bbox=(self.WindowZeroPointX, self.WindowZeroPointY, self.WindowCaptureW, self.WindowCaptureH)) #x, y, w, h    
        self.img = cv2.cvtColor(np.array(self.raw), cv2.COLOR_BGR2RGB)
        
        self.imageList.append(self.raw)
        self.imageList = self.imageList[-self.imageLen:]

        if len(self.imageList) > 1 and self.isCapturable:
            mat1 = np.array(self.imageList[-1])
            mat2 = np.array(self.imageList[-2])

            # to gray image
            gmat1 = cv2.cvtColor(mat1, cv2.COLOR_BGR2GRAY)
            gmat2 = cv2.cvtColor(mat2, cv2.COLOR_BGR2GRAY)

            self.gdifference = cv2.subtract(gmat1, gmat2)

            self.gdifferenceList.append(self.gdifference)
            self.gdifferenceList = self.gdifferenceList[-self.gdifferenceLen:]

            self.gdifferenceMaxList.append(self.gdifference.max())
            self.gdifferenceMaxList = self.gdifferenceMaxList[-self.gdifferenceLen:]



    def showLastImg(self, imgType='DEFAULT'):
        if imgType=='DIFFERENCE':
            if len(self.imageList) > 1:
                cv2.imshow('showLast2Diff', self.gdifference)
            else:
                print('no self.gdifference')
        elif imgType=='DEFAULT':
                cv2.imshow('showLastImg', self.img)
        else:
            raise ValueError('imgType')



    # def calDifferenceMean(self):
    #     return np.mean(self.gdifferenceList)
    
    def calDifferenceMaxMean(self):
        return np.mean(self.gdifferenceMaxList)
    
    # 1 sec delayed gdifference mean; (5 item)
    def calDelayedDifferenceMaxMean(self):
        return np.mean(self.gdifferenceMaxList[:5])

    def lastMaxDifference(self):
        return self.gdifference.max()


    def calDifferenceSTD(self):
        if len(self.gdifferenceList) == self.gdifferenceLen:
            self.differenceListStd = np.std(self.gdifferenceList)

            # self.differenceListStdList.append(self.differenceListStd)
            # self.differenceListStdList = self.differenceListStdList[-self.gdifferenceLen:]

            self.GDSList.append(self.differenceListStd)
            self.GDSListLen = 100

            return self.differenceListStd



    def casting(self):
        self.isFishing = True
        return

    def reelUp(self):
        self.isFishing = False        
        return


    def trackBait(self):
        if 1 < round(np.mean(self.differenceListStdList), 1):
            self.isCapturable = False
            
            self.imageList = []
            self.gdifferenceList = []
            # self.gdifferenceMaxList = []
            # self.differenceListStdList = []


            WindowZeroPointX, WindowZeroPointY, WindowCaptureW, WindowCaptureH = self.baitArea(self.ptx1, self.ptx2, self.pty1, self.pty2)
            print(WindowZeroPointX, end=', ')
            print(WindowZeroPointY, end=', ')
            print(WindowCaptureW, end=', ')
            print(WindowCaptureH)
            

    def trackDifference(self):

        if len(self.gdifferenceList) > 2:
            if len(np.where(self.gdifference == self.gdifference.max())[0]) > 1:
                

                self.ptx1 = np.where(self.gdifference == self.gdifference.max())[1].min()
                self.ptx2 = np.where(self.gdifference == self.gdifference.max())[1].max()
                self.pty1 = np.where(self.gdifference == self.gdifference.max())[0].min()
                self.pty2 = np.where(self.gdifference == self.gdifference.max())[0].max()


                # self.lastPoint(self.gdifference.max(), ((ptx1+ptx2)//2, (pty1+pty2)//2))


                cv2.rectangle(self.img, (self.ptx1, self.pty1), (self.ptx2, self.pty2), (0, 0, 255), 3)
                # pg.moveTo((ptx1+ptx2)//2+300, (pty1+pty2)//2+300)
                # time.sleep(1)
                # pg.click(button='right')
                # time.sleep(1)
                # pg.press('0')


                # if self.calDifferenceMean < self.WaterValue:
                #     pg.press('0')
                #     return
                
                # return
            
            # elif len(np.where(self.gdifference == self.gdifference.max())[0]) == 1:
                
            #     ptx = np.where(self.gdifference == self.gdifference.max())[1][0]
            #     pty = np.where(self.gdifference == self.gdifference.max())[0][0]
                
            #     # self.lastPoint(self.gdifference.max(), (ptx, pty))

            #     if self.gdifference.max() > self.CatchValue:
            #         cv2.rectangle(self.img, (ptx-2, pty-2), (ptx+2, pty+2), (0, 0, 255), 3)
            #         # pg.moveTo(ptx+300, pty+300)
            #         # time.sleep(1)
            #         # pg.click(button='right')
            #         # time.sleep(1)
            #         # pg.press('0')
            #         return

            #     return

            # else:    
            #     return 
        


if __name__=='__main__':

    ce = CaptureEngine()

    while True:

        
        ce.grabImg()

        ce.trackDifference()

        ce.showLastImg()
        
        differenceStdValue = ce.calDifferenceSTD()


        if differenceStdValue == None:
            print('Need more img item')
        else:
            print(datetime.datetime.now(), end=' | ')
            print('dMx: ', round(ce.lastMaxDifference(), 3), end=' | ')
            # print('dMxM: ', round(ce.calDifferenceMaxMean(), 3), end=' | ')
            # print('d1sDMxM: ', round(ce.calDelayedDifferenceMaxMean(), 3), end=' | ')
            # print('d10M: ', round(ce.calDifferenceMean(), 3), end=' | ')
            # print('dMxL: ', ce.gdifferenceMaxList[5], end=' | ')
            print('dSTD: ', round(differenceStdValue, 3), end=' | ')
            print('dSTD: ', round(differenceStdValue, 3))

            # print(np.mean(ce.differenceListStdList))


        if cv2.waitKey(1) & 0Xff == ord('q'):
            break
        
    cv2.destroyAllWindows()