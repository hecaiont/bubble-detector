import numpy as np
import cv2
from PIL import ImageGrab

import time
import datetime

import pyautogui as pg



class CaptureEngine():

    def __init__(self, runType):
        self.runType = runType

        self.startTime = time.time()
        self.checkTime = time.time()

        self.FailCount = 0

        self.LastCaptureNoList = []
        self.LastCaptureNoListLen = 5

        self.WindowOriginX = 1550
        self.WindowOriginY = 900
        self.WindowWidth = 2150
        self.WindowHeight = 1300

        self.WindowWidthSize = self.WindowWidth - self.WindowOriginX
        self.WindowHeightSize = self.WindowHeight - self.WindowOriginY

        self.isCapturable = False
        self.isFishing = False
        self.isBite = False

        self.imageList = []
        self.imageLen = 2
        
        # Brightness Difference
        self.BDList = []
        self.BDLen = 10

        self.BDMaxList = []

        # Std of Brightness Difference
        self.BDSList = []
        self.BDSListLen = 100





        # for Wailing Caverns, default
        self.CatchValue = 150 # over
        self.CatchValue = 140 # over
        
        self.CatchValue = 165 # over
        self.CatchValue = 180 # over

        # self.CatchValue = 160 # over
        # self.CatchValue = 210 # over
        self.BaitValue = 50 # over
        self.WaterValue = 20 # under
        # self.WaterValue = 50 # rainy wheather
        # self.WaterValue = 30

        self.term = 1.25



        self.activateWindow()
        self.usePaste()
        self.doCapture()




    def castingFailureCheck(self):
        if np.mean(self.LastCaptureNoList) < 5.0 and len(self.LastCaptureNoList) == self.LastCaptureNoListLen:
            self.FailCount += 1
        return self.FailCount

    def checkElapsedTime(self, cycle):
        elapsed = time.time() - self.checkTime
        if round(elapsed//cycle, 1) > 1.0: 
            print('self.checkTime renewal : ', self.checkTime)
            self.checkTime = time.time()
            return True
        else:
            return False


    def grabImg(self):
        self.raw = ImageGrab.grab(bbox=(self.WindowOriginX, self.WindowOriginY, self.WindowWidth, self.WindowHeight)) #x, y, w, h    
        self.img = cv2.cvtColor(np.array(self.raw), cv2.COLOR_BGR2RGB)
        
        self.imageList.append(self.raw)
        self.imageList = self.imageList[-self.imageLen:]


    def getSubtract(self):
        mat1 = np.array(self.imageList[-1])
        mat2 = np.array(self.imageList[-2])

        # to gray image
        gmat1 = cv2.cvtColor(mat1, cv2.COLOR_BGR2GRAY)
        gmat2 = cv2.cvtColor(mat2, cv2.COLOR_BGR2GRAY)

        BD = cv2.subtract(gmat1, gmat2)

        self.BDList.append(BD)
        self.BDList = self.BDList[-self.BDLen:]

        self.BDMaxList.append(BD.max())
        self.BDMaxList = self.BDMaxList[-self.BDLen:]

        self.BDSList.append(np.std(BD))
        self.BDSList = self.BDSList[-self.BDSListLen:]




    def showCapture(self):
        cv2.imshow('showCapture', self.img)
        return

    def showDifference(self):
        cv2.imshow('showDifference', self.BDList[-1])
        return

    def calDifferenceStdRatio(self):
        return np.std(self.BDList[-1])/np.std(self.BDList[-2])



    def doCapture(self):
        self.isCapturable = True
        return

    def stopCapture(self):
        self.isCapturable = False 
        return

    def stateCheck(self):
        if self.BDMaxList[-1] < self.WaterValue:
            return True
        else:
            return False
            

    def trackDifference(self):
        if len(np.where(self.BDList[-1] == self.BDList[-1].max())[0]) > 1:
            self.trackType = '2'
            self.ptx1 = np.where(self.BDList[-1] == self.BDList[-1].max())[1].min()
            self.ptx2 = np.where(self.BDList[-1] == self.BDList[-1].max())[1].max()
            self.pty1 = np.where(self.BDList[-1] == self.BDList[-1].max())[0].min()
            self.pty2 = np.where(self.BDList[-1] == self.BDList[-1].max())[0].max()

            cv2.rectangle(self.img, (self.ptx1, self.pty1), (self.ptx2, self.pty2), (0, 0, 255), 3)
        elif len(np.where(self.BDList[-1] == self.BDList[-1].max())[0]) == 1:
            self.trackType = '1'
            self.ptx = np.where(self.BDList[-1] == self.BDList[-1].max())[1][0]
            self.pty = np.where(self.BDList[-1] == self.BDList[-1].max())[0][0]

            cv2.rectangle(self.img, (self.ptx-2, self.pty-2), (self.ptx+2, self.pty+2), (0, 255, 0), 3)
        else:
            print('no max !!!')

        return


    def Bite(self, Criteria='mx'):
        if Criteria=='mx':
            if self.isCapturable:
                if self.BDMaxList[-1] > self.CatchValue:
                    return True
                else:
                    return False
            else:
                return False
        
        # not working...
        elif Criteria=='std':
            if self.isCapturable:
                if self.BDSList[-1] > 4 and self.BDMaxList[-1] > self.CatchValue:
                    return True
                else:
                    return False
            else:
                return False

        else:
            raise ValueError('Criteria')


    def onBait(self, trackType):
        if trackType == '2':
            xloc, yloc = (self.ptx1+self.ptx2)//2+self.WindowOriginX, (self.pty1+self.pty2)//2+self.WindowOriginY
        elif trackType == '1':
            xloc, yloc = self.ptx+self.WindowOriginX, self.pty+self.WindowOriginY
        else:
            xloc, yloc = self.WindowOriginX, self.WindowOriginY
            ValueError('trackType')

        pg.moveTo(xloc, yloc)
        
        return xloc, yloc

    def toOrigin(self):
        pg.moveTo(self.WindowOriginX, self.WindowOriginY)
        return 

    def interactionMouseOver(self):
        if self.runType != 'test':
            pg.press('`')
        return

    def Hooking(self):
        time.sleep(self.term)
        if self.runType != 'test':
            # pg.click(button='right')
            self.interactionMouseOver()
            self.stopCapture()
        return 


    def usePaste(self):
        pg.press('2')
        return

    def openClam(self):
        pg.press('3')
        return

    def reCast(self):
        time.sleep(1)
        if self.runType != 'test':
            pg.press('1')
            self.doCapture()

            # if self.checkElapsedTime(600):
            #     # self.stopCapture()
            #     self.usePaste()
            #     print('use Paste')

            self.LastCaptureNoList.append(self.captureNo)
            self.LastCaptureNoList = self.LastCaptureNoList[-self.LastCaptureNoListLen:]

        return 

    def activateWindow(self):
        self.toOrigin()
        if self.runType != 'test':
            pg.click(button='left')
        return


    def main(self):

        self.captureNo = 0
        while self.isCapturable:

            self.grabImg()
            
            if len(self.imageList) == 2:
                self.getSubtract()

                print('{0:03d}'.format(self.captureNo), end=' ')
                print(datetime.datetime.now().time(), end=' ')
                print(round(self.BDSList[-1], 1), end =' ')
                print(self.BDMaxList[-1])

                self.trackDifference()
                             
                if self.Bite():# mx, std
                    print('BITE: ', end=' ')
                    print(self.onBait(self.trackType))
                    self.Hooking()
                    print('HOOK')


                    print('CASTING')
                    self.stopCapture()

                    self.openClam()

                    self.reCast()
                    print('Current FailCount: ', self.castingFailureCheck())
                    self.captureNo = 0
                    self.toOrigin()
                    
                if self.stateCheck():
                    print('NO BITE')
                    self.stopCapture()

                    self.openClam()
                    
                    self.reCast()
                    print('Current FailCount: ', self.castingFailureCheck())
                    self.captureNo = 0
                    self.toOrigin()

                self.showCapture()
                self.showDifference()


            if self.FailCount > 5:
            
                self.stopCapture()
                self.usePaste()
                time.sleep(2)
                
                print('RESTORE')

                self.doCapture()

                self.FailCount = 0
                self.LastCaptureNoList = []

            self.captureNo+=1


            if cv2.waitKey(1) & 0Xff == ord('q'):
                break
        
        else:
            print('STOP')
            print('3')
            time.sleep(1)
            print('2')
            time.sleep(1)
            print('1')
            time.sleep(1)

            self.grabImg()
            self.doCapture()
            
            
        cv2.destroyAllWindows()





if __name__=='__main__':
    ce = CaptureEngine('run')
    
    ce.main()

