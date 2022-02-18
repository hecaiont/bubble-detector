import time
import datetime

import cv2 as cv
import numpy as np

from PIL import ImageGrab

import pyautogui as pg
import pyperclip

import winsound as sd





class CaptureEngine():

    def __init__(self):
        self.startTime = time.time()
        self.isCapturable = False

        # center point of display
        self.WindowOriginX = 1920
        self.WindowOriginY = 1080
        
        self.template = None
        
    def setTemplate(self, url):
        self.template = cv.imread(url, 0) # 
        self.temW, self.temH = self.template.shape[::-1]


    def setCaptureRegion(self, xBegin, yBegin, xEnd, yEnd):
        self.xBegin = xBegin
        self.yBegin = yBegin
        self.xEnd = xEnd
        self.yEnd = yEnd

        self.captureWidth = self.xEnd - self.xBegin
        self.captureHeight = self.yEnd - self.yBegin


    def checkElapsedTime(self, cycle):
        elapsed = time.time() - self.checkTime
        if round(elapsed//cycle, 1) > 1.0: 
            print('self.checkTime renewal : ', self.checkTime)
            self.checkTime = time.time()
            return True
        else:
            return False

    def showCapture(self, img):
        cv.imshow('showCapture', img)

    
    def showRawCapture(self):
        cv.imshow('showRawCapture', self.raw)

    def moveCursor(self, xloc, yloc):
        if self.runType != 'test':
            pg.moveTo(xloc, yloc)
        
        return xloc, yloc
        
    def toOrigin(self):
        if self.runType != 'test':
            pg.moveTo(self.WindowOriginX, self.WindowOriginY)
         

    def mouseLeftClick(self):
        if self.runType != 'test':
            pg.click(button='left')
        

    def mouseRightClick(self):
        if self.runType != 'test':
            pg.click(button='right')
        

    def interactionMouseOver(self):
        if self.runType != 'test':
            pg.press('F12')
        

    def activateWindow(self):
        self.toOrigin()
        self.mouseLeftClick()
        



    def doCapture(self):
        self.isCapturable = True
        

    def stopCapture(self):
        self.isCapturable = False 
        


    def beepsound(self):
        fr = 2000    # range : 37 ~ 32767
        du = 1500     # 1000 ms ==1second
        sd.Beep(fr, du) # winsound.Beep(frequency, duration)


    def grabImg(self):
        raw = np.array(ImageGrab.grab(bbox=(self.xBegin, self.yBegin, self.xEnd, self.yEnd))) #x, y, w, h)
        return raw


    def getObj(self, raw, threshold):
        img_gray = cv.cvtColor(raw, cv.COLOR_BGR2GRAY)
        res = cv.matchTemplate(img_gray, self.template, cv.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        return loc





class CaptureCombat(CaptureEngine):
    # to check if combat
    
    def __init__(self, runType):
        super().__init__()
        self.runType = runType
        self.checkTime = time.time()

        # map
        self.setCaptureRegion(1072, 720, 1102, 750)
        # self.setTemplate('image/obj02.png') # minimap object image(red dot)


    def cropCircle(self, img, r):
        mask = np.zeros((self.captureWidth, self.captureHeight), np.uint8)
        circle_img = cv.circle(mask, (r, r), radius=r, color=(255, 255, 255), thickness=-1)        
        masked_data = cv.bitwise_and(img, img, mask=circle_img)
        return masked_data


    def main(self):
        while True:
            raw = self.grabImg()
            raw = self.cropCircle(raw, r=15)
            img = cv.cvtColor(raw, cv.COLOR_BGR2RGB)

            # self.showCapture(img)

            print(np.mean(img))


            if cv.waitKey(1) & 0Xff == ord('q'):
                break

            time.sleep(1)
            
        cv.destroyAllWindows()
    




class CaptureMap(CaptureEngine):
    # (85, 85) is center of minimap
    # resolution: window mode, 1600x900
    
    # start location 9.4, 62.6
    
    def __init__(self, runType):
        super().__init__()
        self.runType = runType
        self.checkTime = time.time()

        self.noObjCount = 0
        self.zoomInCount = 0

        # tagetable list

        # self.targetList = '올빼미'
        # self.targetList = '전쟁망치일족'

        # self.targetList = ['굶주린 수렁군주', '굶주린 곰팡이 거인']
        # self.targetList = ['바람올빼미', '야생 엘레크']
        
        # self.targetList = ['가시먹이 탈부크', '수컷 갈래발굽', '휘몰아치는 폭풍']
        # self.targetList = ['갈래발굽']
        # self.exceptList = ['줄무늬 탈부크', '바람올빼미', '야생 엘레크']
        self.targetList = ['굶주린 바람올빼미', '야생 엘레크', '휘몰아치는 폭풍']
        self.exceptList =[]


        # map
        self.setCaptureRegion(2450, 685, 2620, 855)
        self.setTemplate('image/obj02.png') # minimap object image(red dot)


        self.isCapturable = False

        self.Collectable = False # True if deadbody is collectable, (약초채집, 채광)
        self.isHunting = False


    
    # 170x170, r=85, 
    def cropCircle(self, img, r=85):
        mask = np.zeros((self.captureWidth, self.captureHeight), np.uint8)
        circle_img = cv.circle(mask, (r, r), radius=r, color=(255, 255, 255), thickness=-1)        
        masked_data = cv.bitwise_and(img, img, mask=circle_img)
        return masked_data



    def cart2pol(self, x, y):
        rho = np.sqrt(x**2 + y**2)
        theta = np.arctan2(y, x)
        return rho, theta


    def zoomIn(self, ):

        return 

    def sleepCount(self, count):
        for i in range(count)[::-1]:
            time.sleep(1)
            print(i)
        return

    def cleanObj(self):
        # targeting
        print('cleanObj')

        target = self.exportTxt(tabTarget=True, printTarget=True) # targetting
        target = self.delPlayerName(target)
        print('target is :', target)

        if target in self.targetList:
            print('run')
    
            # attack
            pg.press('F12')

            # dot deal
            pg.press('3')
            time.sleep(2)
            
            # pet attack
            # pg.press('6')
            pg.press('F12')
            # time.sleep(2)
            
            pg.press('2')
            
            pg.keyDown('s')
            time.sleep(1)
            pg.press('space')
            time.sleep(1)
            pg.keyUp('s')
            
            pg.press('5')

            time.sleep(2)
            pg.press('=')
            time.sleep(2)

            pg.press('F12')
            pg.press('4')
            time.sleep(2)
            pg.press('1')
            time.sleep(2)

            pg.press('F1')
            time.sleep(0.3)

            pg.press('F12')
            pg.keyDown('s')
            time.sleep(0.5)
            pg.press('space')
            time.sleep(0.5)
            pg.press('space')
            time.sleep(0.5)
            pg.keyUp('s')


            # normal attack
            pg.press('F12')

            pg.press('1')
            time.sleep(2)
            pg.press('5')
            time.sleep(2)
            time.sleep(3)


            print('done')

            target = self.exportTxt(tabTarget=False, printTarget=True) # current target
            target = self.delPlayerName(target)
            print('target is :', target)
            self.rooting(target)

            # if target in self.targetList:
            #     print('continue run')
                
            #     pg.press('F3')
            #     pg.press('F2')
            #     time.sleep(2)
            #     pg.press('3')
            #     time.sleep(2)
            #     pg.press('5')
                
            #     print('done')

            #     target = self.exportTxt(False, True)
            #     target = self.delPlayerName(target)
            #     print('target is :', target)
            #     self.rooting(target)

            # else:
            #     print('donex2')
            #     self.beepsound()
            #     print('error objs...')
            #     self.sleepCount(10)
            #     print('........')


        elif target == '<대상 없음>':
            print('no attackable objs...continue')
        
        elif target in self.exceptList:
            pg.press('esc')
            print('no attackable objs...continue')
            
        else:
            pg.press('esc')

            # error beep
            self.beepsound()
            print('no attackable objs...')
            self.sleepCount(10)
            print('search Objs...')

            


    def rooting(self, target):
        if target == '<대상 없음>':
            print('root')

            pg.press('F11')
            pg.press('F12')
            
            if self.Collectable:
                time.sleep(6)
                # center of worldFrame
                self.moveCursor(1846, 1054)

                time.sleep(1)
                pg.press('`')

            time.sleep(3)
            pg.press('=')
            time.sleep(5)

        else:
            print(target)
        


    def exportTxt(self, tabTarget, printTarget):
        if tabTarget:
            pg.press('tab')
            print('press tab')
            time.sleep(1)

        # print current target
        if printTarget:
            pg.press('0')
            print('press 0')
            time.sleep(1)

        pg.press('9') # print target to chat

        time.sleep(0.1)
        pg.moveTo(1994, 992)
        pg.click(button='left')

        time.sleep(0.1)
        pg.keyDown('shift')
        pg.press('home')
        pg.keyUp('shift')
        time.sleep(0.1)
        pg.hotkey('ctrl', 'c')
        time.sleep(0.1)
        pg.press('esc')
        pg.press('9')
        
        txt = pyperclip.paste()
        
        return txt

    def delPlayerName(self, txt):
        txt = txt[(txt.find('방송광고개혁안')+10):]
        return txt


    def turnLeft(self, count):
        pg.keyDown('a')
        time.sleep(0.05 * count)
        pg.keyUp('a')
        return count

    def turnRight(self, count):
        pg.keyDown('d')
        time.sleep(0.05 * count)
        pg.keyUp('d')        
        return count


    def calTurnCount(self, degrees):
        return round(round(np.abs(degrees))//10)



    def faceTarget(self, degrees):
        if degrees < 90 and degrees >= 0:
            count = self.calTurnCount(degrees)
            self.turnRight(count)
        elif degrees <= 180 and degrees >= 90:
            count = self.calTurnCount(degrees-90)            
            self.turnLeft(count)
        elif degrees >= -90 and degrees < 0:
            count = self.calTurnCount(degrees) + self.calTurnCount(90)
            self.turnRight(count)
        elif degrees >= -180 and degrees < -90:
            count = self.calTurnCount(degrees+90) + self.calTurnCount(90)
            self.turnLeft(count)
        else:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            count = 0
        return count



    def searchObjs(self, loc, img):
        if len(loc[0]) > 0:
            self.noObjCount = 0
            print('map obj count :', len(loc[0]))            
            
            for pt in zip(*loc[::-1]):
                
                x = pt[0] + self.temW//2
                y = pt[1] + self.temH//2

                break

            self.isHunting = True
            return x, y

        
        else:
            self.noObjCount += 1
            self.isHunting = False
            return 85, 85







    def taskObj(self, x, y):
        # (85, 85) as (0, 0)
        x = x - 85
        y = 85 - y
        
        r, theta = self.cart2pol(x, y)
        degs = np.degrees(theta)

        print('x: ', x, 'y: ', y, end=' ')
        print('r:', round(r, 1),  end=' ')
        print('degrees:', round(degs, 1))

        count = self.faceTarget(degs)
        print('count :', count)

        return r 

    def dashObj(self, r):

        cal_r = r + self.zoomInCount*10
        if cal_r > 50:

            print('too far, move forward!')
            pg.keyDown('w')
            time.sleep(1+self.zoomInCount)
            pg.keyUp('w')

        print('cal_r :', round(cal_r, 1))




                
    def initialize(self,):
        try:
            self.activateWindow()

            for i in range(5):
                pg.press('num9')

            self.doCapture()

            print(self.captureWidth, self.captureHeight)

            self.captureNo = 0
    
            return True
        
        except:
            return False



    def main(self, initializeResult):
        if initializeResult:
                
            while self.isCapturable:

                raw = self.cropCircle(self.grabImg())
                img = cv.cvtColor(raw, cv.COLOR_BGR2RGB)

                # cv.circle(img, (85, 85), radius=1, color=(0, 0, 255), thickness=1)


                loc = self.getObj(raw, 0.8)
                x, y = self.searchObjs(loc, img)
                
                cv.circle(img, (x, y), radius=10, color=(0, 0, 255), thickness=2)


                self.showCapture(img)


                if self.isHunting:
                    while self.zoomInCount > 0:
                        pg.press('num9')
                        self.zoomInCount -= 1
                        print('zoom in!')

                    r = self.taskObj(x, y)
                    
                    self.dashObj(r)

                    self.cleanObj()

                    self.isHunting = False


                if self.noObjCount > 5:
                    print('no Objs, Zoom in')
                    pg.press('num8')
                    self.zoomInCount += 1

                    self.noObjCount = 0

                    if self.zoomInCount > 5:
                        
                        while self.zoomInCount > 0:
                            pg.press('num9')
                            self.zoomInCount -= 1
                            print('zoom in!')
                        
                        print('no Objs, rest...')
                        self.sleepCount(10)
                        print('search Objs...')



                print('captureNo :', self.captureNo)
                self.captureNo+=1
                

                if cv.waitKey(1) & 0Xff == ord('q'):
                    break
                
            cv.destroyAllWindows()
        
        else:
            print('fail to initialize')




    def movePlayer(self):
        initX = 9.1
        initY = 62.8

        self.activateWindow()

        pg.press('7')
        
        results = self.exportTxt()
        results = results[1:]
        xloc, yloc = results.split(',')

        print(xloc, yloc)

        xloc, yloc = float(xloc), float(yloc)

        dx = initX - xloc
        dy = initY - yloc

        dx = round(dx)*10
        dy = round(dy)*10

        if dx < 0:
            for i in range(-dx):
                pg.keyDown('q')
                time.sleep(0.4)
                pg.keyUp('q')
        elif dx > 0:
            for i in range(dx):
                pg.keyDown('e')
                time.sleep(0.4)
                pg.keyUp('e')
        else:
            print('dx is zero')
        
        if dy < 0:
            for i in range(-dy):
                pg.keyDown('w')
                time.sleep(0.5)
                pg.keyUp('w')
        elif dy > 0:
            for i in range(dy):
                pg.keyDown('s')
                time.sleep(0.5)
                pg.keyUp('s')
        else:
            print('dy is zero')


        pg.press('7')
        
        results = self.exportTxt()
        results = results[1:]
        xloc, yloc = results.split(',')

        print(xloc, yloc)
        print(float(xloc)/initX, float(yloc)/initY)


    def movePlayer(self):
        initX = 9.1
        initY = 62.8

        self.activateWindow()

        pg.press('7')
        
        results = self.exportTxt()
        results = results[1:]
        xloc, yloc = results.split(',')

        print(xloc, yloc)

        xloc, yloc = float(xloc), float(yloc)

        dx = initX - xloc
        dy = initY - yloc

        rho, theta = cart2pol(dx, dy)





class AutoHunter(CaptureCombat, CaptureMap):
    
    def __init__(self, ):
        super().__init__()
        











if __name__=='__main__':
    # ce = CaptureMap('run')
    
    # result = ce.initialize()
    # ce.main(result)

    # ce.movePlayer()




    # cb = CaptureCombat('test')

    # cb.main()
    
    


