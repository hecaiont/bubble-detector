import time 

import cv2

import os

import numpy as np


class BubbleCounter():

    def __init__(self):
        self.startTime = time.time()
        
        # self.images = []
        # folder = 'C:/Users/dlsxo/Desktop/bubble counter/sample00/'
        # for filename in os.listdir(folder):
        #     img = cv2.imread(os.path.join(folder, filename))
        #     if img is not None:
        #         self.images.append(img)


        self.vidcap = cv2.VideoCapture('./KakaoTalk_20220131_002306209.mp4')
        self.success, self.image = self.vidcap.read()
        





    def main(self):
        count = 0
        while self.success:
            cv2.imwrite("./sample00/%06d.jpg" % count, self.image)     # save frame as JPEG file
            self.success, self.image = self.vidcap.read()
            print('Read a new frame: ', self.success)
            count += 1



    def printInfo(self):

        print(type(self.image))
        print(self.image.shape)




    def cropCircle(self):
        mask = np.zeros((1080, 1920), np.uint8)
        circle_img = cv2.circle(mask, (950, 500), radius=500, color=(255, 255, 255), thickness=-1)        
        masked_data = cv2.bitwise_and(self.image, self.image, mask=circle_img)
        
        while True:
            cv2.imshow('showImg', masked_data)

            if cv2.waitKey(1) & 0Xff == ord('q'):
                break
        
    
    def cropCircle(self, img):
        mask = np.zeros((1080, 1920), np.uint8)
        circle_img = cv2.circle(mask, (950, 500), radius=500, color=(255, 255, 255), thickness=-1)        
        masked_data = cv2.bitwise_and(img, img, mask=circle_img)
        return masked_data
        
    
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




    def imgLoad(self):
        img1 = cv2.imread('C:/Users/dlsxo/Desktop/bubble counter/sample00/000000.jpg')
        img1 = self.cropCircle(img1)
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        

        img2 = cv2.imread('C:/Users/dlsxo/Desktop/bubble counter/sample00/000001.jpg')
        img2 = self.cropCircle(img2)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        BD = cv2.subtract(img1, img2)

        while True:
            BDS = cv2.resize(BD, (960, 540)) #Resize image

            cv2.imshow('showImg', BDS)

            if cv2.waitKey(1) & 0Xff == ord('q'):
                break



    def imgLoad(self):
        img1 = cv2.imread('C:/Users/dlsxo/Desktop/bubble counter/sample00/000022.jpg')
        img1 = self.cropCircle(img1)
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        

        img2 = cv2.imread('C:/Users/dlsxo/Desktop/bubble counter/sample00/000023.jpg')
        img2 = self.cropCircle(img2)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        BD = cv2.subtract(img1, img2)



        ret, img_binary = cv2.threshold(BD, 10, 255, 0)
        contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    
        for cnt in contours:
            cv2.drawContours(img2, [cnt], 0, (255, 0, 0), 2)  # blue


        while True:
            img2 = cv2.resize(img2, (960, 540)) #Resize image

            cv2.imshow('showImg', img2)

            if cv2.waitKey(1) & 0Xff == ord('q'):
                break



    def vPlay(self):        
        vidcap = cv2.VideoCapture('./KakaoTalk_20220131_002306209.mp4')
        success, image = vidcap.read()
        

        # video info
        print('Frame width:', int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)))
        print('Frame height:', int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        print('Frame count:', int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)))
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        print('FPS:', fps)


        count = 0
        while success:


            img1 = self.cropCircle(image)
            # img1 = image
            # img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)


            success, image = vidcap.read()
            # print('Read a new frame: ', success)
            print(count)

            img2 = self.cropCircle(image)
            # img2 = image
            # img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)


            BD = cv2.subtract(img1, img2)

            BD = cv2.resize(BD, (960, 540)) #Resize image

            cv2.imshow('showImg', BD)

            if cv2.waitKey(1) & 0Xff == ord('q'):
                break


            # time.sleep(0.5)
            count += 1




    def vPlay(self):
        vidcap = cv2.VideoCapture('./KakaoTalk_20220131_002306209.mp4')
        success, image = vidcap.read()
        

        # video info
        print('Frame width:', int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)))
        print('Frame height:', int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        print('Frame count:', int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)))
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        print('FPS:', fps)


        count = 0
        while success:


            img1 = self.cropCircle(image)
            # img1 = image
            # img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)


            success, image = vidcap.read()
            # print('Read a new frame: ', success)
            print(count)

            img2 = self.cropCircle(image)
            # img2 = image
            # img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

            BD = cv2.subtract(img1, img2)

            ret, img_binary = cv2.threshold(BD, 50, 255, 0)
            contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                cv2.drawContours(img2, [cnt], 0, (255, 0, 0), 2)  # blue



            img2 = cv2.resize(img2, (960, 540)) #Resize image

            cv2.imshow('showImg', img2)

            if cv2.waitKey(1) & 0Xff == ord('q'):
                break


            # time.sleep(0.5)
            count += 1





if __name__=='__main__':
    bc = BubbleCounter()
    
    # bc.main()

    # bc.printInfo()
    # bc.cropCircle()

    # bc.imgLoad()

    bc.vPlay()

 