import random
from threading import Timer
from tkinter import *

from PIL.ImageTk import PhotoImage as PI, Image as IMG

from Car import Car
from DE import BaseDE
from ga_settings import yellow_time as yT, lb1, ub1, verbose, epoch, pop_size, max_car, rand_list

listInterSec = []


def scaleImage(file, size):
    image_file = IMG.open(file)
    image_file.thumbnail(size)
    return PI(image_file)


def scaleImageCar(dir, size):
    list = []
    for i in range(0, 10):
        car_file = dir + 'car' + str(i) + '.png'
        image_file = IMG.open(car_file)
        image_file.thumbnail(size)
        list.append(PI(image_file))
    return list


class InterSec(Canvas):
    """class Panel1 creates a panel with an image on it, inherits wx.Panel"""

    def loadImgCar(self, file):
        imageFile = IMG.open(file)
        imageFile.thumbnail(self.sizeCar)
        return PI(imageFile)

    def __init__(self, root, position=(0, 0), size=(598, 246), horiz=True, yellow=True, redTime=30, greenTime=20,
                 index=None):

        # create the canvas with the index ( index is the identify )

        super().__init__(root, width=size[0], height=size[0])
        self.place(x=position[0], y=position[1])
        self.index = index

        # postion of light and labels of time posLight
        self.posLight = [(220, 175), (348, 50), (220, 50), (348, 175)]
        self.posLabels = [(200, 175), (385, 50), (200, 50), (385, 175)]
        self.posLabelsNbCars = [(170, 175), (410, 50), (200, 30), (385, 190)]

        # setting bg, add a image road (route) with size 600x400
        self.sizeBg = (600, 400)
        self.road_image = scaleImage('bg/background.png', self.sizeBg)
        # setting lights, add the light g, r, y ,off light
        self.sizeLight = (30, 50)
        self.greenLight = scaleImage('bg/light_green.png', self.sizeLight)
        self.redLight = scaleImage('bg/light_red.png', self.sizeLight)
        self.yellowLight = scaleImage('bg/light_yellow.png', self.sizeLight)
        self.lightOff = scaleImage('bg/light_off.png', self.sizeLight)
        # setting car with size
        self.sizeCar = (30, 25)

        self.listCars = {
            'l': scaleImageCar('bg/cars_left/', self.sizeCar),
            'r': scaleImageCar('bg/cars_right/', self.sizeCar),
            'u': scaleImageCar('bg/cars_up/', self.sizeCar),
            'd': scaleImageCar('bg/cars_down/', self.sizeCar)
        }

        self.whereWait = {
            'l': [],
            'r': [],
            'u': [],
            'd': []
        }

        self.where = {
            'l': [],
            'r': [],
            'u': [],
            'd': []
        }

        self.list_light = []
        self.list_lbls = []
        self.index_left = 0
        self.index_right = 0
        self.index_up = 0
        self.index_down = 0
        self.horiz = horiz
        self.yellow = yellow
        self.redTime = redTime
        self.greenTime = greenTime
        self.yTime = yT
        self.model = BaseDE(self.obj_func, lb1, ub1, verbose, epoch, pop_size)

        self.threads = []
        self.threadLeft = []
        self.threadRight = []
        self.threadUp = []
        self.threadDown = []
        self.ThreadingHorizontal = []
        self.ThreadingVertical = []
        try:
            self.create_image(0, 0, image=self.road_image, anchor=NW)

            self.list_light = [Label(self, image=self.lightOff) for _ in range(4)]
            for i in range(len(self.list_light)):
                self.list_light[i].place(x=self.posLight[i][0], y=self.posLight[i][1])

            self.list_lbls = [Label(self, text='0', fg='black', bg='white') for _ in range(4)]
            for i in range(len(self.list_lbls)):
                self.list_lbls[i].place(x=self.posLabels[i][0], y=self.posLabels[i][1])

            self.list_lblsNbCars = [Label(self, text='0', fg='black', bg='white') for _ in range(4)]
            for i in range(len(self.list_lblsNbCars)):
                self.list_lblsNbCars[i].place(x=self.posLabelsNbCars[i][0], y=self.posLabelsNbCars[i][1])

            self.CarLeft()
            self.CarRight()
            self.CarUp()
            self.CarDown()
            self.switch()
            self.checkCarsWaitHorizontal()
            self.checkCarsWaitVertical()
        except IOError:
            raise SystemExit

    def changeLight(self):
        if self.horiz:
            for i in range(2):
                self.list_light[i].config(image=self.greenLight)
                self.list_light[i + 2].config(image=self.redLight)
        else:
            for i in range(2):
                self.list_light[i + 2].config(image=self.greenLight)
                self.list_light[i].config(image=self.redLight)

    def changeYellow(self):
        if self.horiz:
            for i in range(2, 4):
                self.list_light[i].config(image=self.yellowLight)
        else:
            for i in range(2):
                self.list_light[i].config(image=self.yellowLight)

    def startYellow(self):
        for i in range(4):
            self.list_light[i].config(image=self.yellowLight)

    def moveCars(self, axes):
        # TODO
        try:
            if axes == ['l', 'r']:
                for car in self.where['l']:
                    if car.winfo_x() <= 220:
                        car.place(x=car.winfo_x() + 10)
                    else:
                        self.whereWait['l'].append(car)
                        self.where['l'].remove(car)

                for car in self.where['r']:
                    if car.winfo_x() >= 348:
                        car.place(x=car.winfo_x() - 10)
                    else:
                        self.whereWait['r'].append(car)
                        self.where['r'].remove(car)
            elif axes == ['u', 'd']:
                for car in self.where['u']:
                    if car.winfo_y() <= 50:
                        car.place(y=car.winfo_y() + 10)
                    else:
                        self.whereWait['u'].append(car)
                        self.where['u'].remove(car)
                for car in self.where['d']:
                    if car.winfo_y() >= 170:
                        car.place(y=car.winfo_y() - 10)
                    else:
                        self.whereWait['d'].append(car)
                        self.where['d'].remove(car)
            else:
                print('Errors axes entered')
                return False
            return True
        finally:
            return False

    def RemoveCar(self, car, axe):
        # TODO
        self.whereWait[axe].remove(car)
        car.destroy()

    def addCar(self, position, axe, index):
        # TODO
        car = Car(self, index, self.listCars[axe][index])
        car.place(x=position[0], y=position[1])
        self.where[axe].append(car)
        # self.fct[axe]()

    def CarLeft(self):
        # TODO
        th = Timer(random.randint(10, 20), self.CarLeft)
        length = len(self.where['l'])
        if length >= max_car:
            th.start()
            self.threadLeft.clear()
            self.threadLeft.append(th)
            return

        beginIndex = 220
        if 0 < length:
            beginIndex = self.where['l'][length - 1].winfo_x() - 35
        r = 0
        nb_car = random.randint(0, int(max_car * rand_list['left']))
        for i in range(nb_car):
            r += random.randint(0, 10)
            positionXY = (beginIndex - (i * 35) - r, 135)
            indexCar = random.randint(0, 9)
            self.addCar(positionXY, 'l', indexCar)
        th.start()
        self.threadLeft.clear()
        self.threadLeft.append(th)

    def CarRight(self):
        th = Timer(random.randint(10, 20), self.CarRight)
        length = len(self.where['r'])
        if length >= 10:
            th.start()
            self.threadRight.clear()
            self.threadRight.append(th)
            return

        beginIndex = 348
        if 0 < length:
            beginIndex = self.where['r'][length - 1].winfo_x() + 35
        r = 0
        nb_car = random.randint(0, int(max_car * rand_list['right']))
        for i in range(nb_car):
            r += random.randint(0, 10)
            positionXY = (beginIndex + (i * 35) + r, 92)
            indexCar = random.randint(0, 9)
            self.addCar(positionXY, 'r', indexCar)
        th.start()
        self.threadRight.clear()
        self.threadRight.append(th)

    def CarUp(self):
        th = Timer(random.randint(10, 20), self.CarUp)
        length = len(self.where['u'])
        if length >= 10:
            th.start()
            self.threadUp.clear()
            self.threadUp.append(th)
            return

        beginIndex = 50
        if 0 < length:
            beginIndex = self.where['u'][length - 1].winfo_y() - 35
        r = 0
        nb_car = random.randint(0, int(max_car * rand_list['up']))
        for i in range(nb_car):
            r += random.randint(0, 10)
            positionXY = (265, beginIndex - (i * 35) - r)
            indexCar = random.randint(0, 9)
            self.addCar(positionXY, 'u', indexCar)
        th.start()
        self.threadUp.clear()
        self.threadUp.append(th)

    def CarDown(self):
        th = Timer(random.randint(10, 20), self.CarDown)
        length = len(self.where['d'])
        if length >= 10:
            th.start()
            self.threadDown.clear()
            self.threadDown.append(th)
            return

        beginIndex = 170
        if 0 < length:
            beginIndex = self.where['d'][length - 1].winfo_y() + 35
        r = 0
        nb_car = random.randint(0, int(max_car * rand_list['down']))
        for i in range(nb_car):
            r += random.randint(0, 10)
            positionXY = (310, beginIndex + (i * 35) + r)
            indexCar = random.randint(0, 9)
            self.addCar(positionXY, 'd', indexCar)
        th.start()
        self.threadDown.clear()
        self.threadDown.append(th)

    def clearThreadLeft(self):
        for th in self.threadLeft:
            th.cancel()
        self.threadLeft.clear()

    def clearThreads(self):
        for th in self.threads:
            th.cancel()

    def clearThreadRight(self):
        for th in self.threadRight:
            th.cancel()
        self.threadRight.clear()

    def clearThreadUp(self):
        for th in self.threadUp:
            th.cancel()
        self.threadUp.clear()

    def clearThreadDown(self):
        for th in self.threadDown:
            th.cancel()
        self.threadDown.clear()

    def clearAllThread(self):
        self.clearThreadLeft()
        self.clearThreadRight()
        self.clearThreadUp()
        self.clearThreadDown()
        self.clearThreads()
        self.clearThreadingVert()
        self.clearThreadingHoriz()

    def switch(self):
        if self.yellow:
            #self.checkCarsBeforeVertical()
            #self.checkCarsBeforeHorizontal()
            self.changeYellow()
            self.yellow_time()
        else:
            if self.horiz:
                #self.checkCarsBeforeVertical()
                self.startHorizontal()
            else:
                #self.checkCarsBeforeHorizontal()
                self.startVerical()

    def resetYellowTime(self):
        self.yTime = yT

    def setLbls(self):
        index = 0
        for axe in self.where:
            self.list_lblsNbCars[index].config(text=str(len(self.where[axe])))
            index += 1
        if self.horiz:
            for i in range(2):
                if self.yellow:
                    self.list_lbls[i + 2].config(text=str(self.yTime))
                    self.list_lbls[i].config(text=str(self.yTime))
                else:
                    self.list_lbls[i].config(text=str(self.greenTime))
                    self.list_lbls[i + 2].config(text=str(self.greenTime + self.yTime))
        else:
            for i in range(2):
                if self.yellow:
                    self.list_lbls[i + 2].config(text=str(self.greenTime))
                    self.list_lbls[i].config(text=str(self.yTime))
                else:
                    self.list_lbls[i + 2].config(text=str(self.greenTime))
                    self.list_lbls[i].config(text=str(self.greenTime + self.yTime))

    def yellow_time(self):
        # start = timer()
        timeGA, _, _ = self.model.train()
        self.greenTime = int(timeGA[0])
        self.redTime = int(timeGA[1])
        # end = timer()
        # self.yTime -= (end - start)
        self.updateYellow()

    def startHorizontal(self):
        self.setLbls()
        if self.moveCars(['l', 'r']):
            pass
        self.greenTime -= 1
        if self.greenTime == 0:
            self.horiz = False
            self.yellow = True
            for th in self.threads:
                th.cancel()
            self.threads.clear()
        th = Timer(1, self.switch)
        th.start()
        self.threads.append(th)

    def startVerical(self):
        self.setLbls()
        if self.moveCars(['u', 'd']):
            pass
        self.greenTime -= 1
        if self.greenTime == 0:
            self.horiz = True
            self.yellow = True
            for th in self.threads:
                th.cancel()
            self.threads.clear()
        th = Timer(1, self.switch)
        th.start()
        self.threads.append(th)

    def updateYellow(self):
        self.setLbls()
        self.yTime -= 1
        # self.checkCarsLeft()
        if self.yTime == 0:
            self.yellow = False
            self.clearThreads()
            self.resetYellowTime()
            th2 = Timer(1, self.changeLight)
            th2.start()
            th = Timer(1, self.switch)
            th.start()
            self.threads = [th, th2]
        else:
            th = Timer(1, self.updateYellow)
            th.start()
            self.threads.append(th)

    def checkCarsWaitHorizontal(self):
        for car in self.whereWait['l']:
            if car.winfo_x() < 580:
                car.place(x=car.winfo_x() + 12)
            else:
                if (self.index % 2) == 0 and (self.index + 1 < len(listInterSec)):
                    try:
                        length = len(listInterSec[self.index + 1].where['l'])
                        positionXY = [0, car.winfo_y()]
                        if length > 0:
                            positionXY[0] = listInterSec[self.index + 1].where['l'][length - 1].winfo_x() - 32
                    except:
                        positionXY = [-32, car.winfo_y()]
                    listInterSec[self.index + 1].addCar(positionXY, 'l', car.index)
                self.RemoveCar(car, 'l')

        for car in self.whereWait['r']:
            if car.winfo_x() > 10:
                car.place(x=car.winfo_x() - 12)
            else:
                if (self.index % 2) == 1 and (self.index - 1 >= 0):
                    try:
                        length = len(listInterSec[self.index - 1].where['r'])
                        positionXY = [630, car.winfo_y()]
                        if length > 0:
                            positionXY[0] = listInterSec[self.index - 1].where['r'][length - 1].winfo_x() + 32
                    except:
                        positionXY = [630, car.winfo_y()]
                    listInterSec[self.index - 1].addCar(positionXY, 'r', car.index)
                self.RemoveCar(car, 'r')
        th = Timer(0.3, self.checkCarsWaitHorizontal)
        th.start()
        self.clearThreadingHoriz()
        self.ThreadingHorizontal.append(th)

    def checkCarsWaitVertical(self):
        for car in self.whereWait['u']:
            if car.winfo_y() < 246:
                car.place(y=car.winfo_y() + 12)
            else:
                if (self.index + 2) < len(listInterSec):
                    try:
                        length = len(listInterSec[self.index + 2].where['u'])
                        positionXY = [car.winfo_x(), 0]
                        if length > 0:
                            positionXY[1] = listInterSec[self.index + 2].where['u'][length - 1].winfo_y() - 32
                    except:
                        positionXY = [car.winfo_x(), -32]
                    listInterSec[self.index + 2].addCar(positionXY, 'u', car.index)
                self.RemoveCar(car, 'u')

        for car in self.whereWait['d']:
            if car.winfo_y() > 10:
                car.place(y=car.winfo_y() - 12)
            else:
                if (self.index - 2) >= 0:
                    try:
                        length = len(listInterSec[self.index - 2].where['d'])
                        positionXY = [car.winfo_x(), 400]
                        if length > 0:
                            positionXY[1] = listInterSec[self.index - 2].where['d'][length - 1].winfo_y() + 32
                    except:
                        positionXY = [car.winfo_x(), 432]
                    listInterSec[self.index - 2].addCar(positionXY, 'd', car.index)
                self.RemoveCar(car, 'd')
        th = Timer(0.3, self.checkCarsWaitVertical)
        th.start()
        self.clearThreadingVert()
        self.ThreadingVertical.append(th)

    def checkCarsBeforeHorizontal(self):
        for car in self.where['l']:
            i = 0
            if car.winfo_x() < 220:
                if i == 0:
                    position = 220 - car.winfo_x()
                else:
                    previous_car = self.where['l'][i - 1]
                    position = - car.winfo_x() + previous_car.winfo_x() + 35

                if position - 10 > 0:
                    car.place(x=car.winfo_x() + 10)
            i += 1
        for car in self.where['r']:
            i = 0
            if car.winfo_x() > 348:
                if i == 0:
                    position = car.winfo_x() - 348
                else:
                    previous_car = self.where['r'][i - 1]
                    position = - previous_car.winfo_x() + car.winfo_x() - 35
                if position - 10 > 0:
                    car.place(x=car.winfo_x() - 10)
            i += 1

    def checkCarsBeforeVertical(self):
        for car in self.where['u']:
            i = 0
            if car.winfo_y() < 50:
                if i == 0:
                    position = 50 - car.winfo_y()
                else:
                    previous_car = self.where['u'][i - 1]
                    position = - car.winfo_y() + previous_car.winfo_y() + 35

                if position - 10 > 0:
                    car.place(y=car.winfo_y() + 10)
            i += 1
        for car in self.where['d']:
            i = 0
            if car.winfo_y() > 170:
                if i == 0:
                    position = car.winfo_y() - 170
                else:
                    previous_car = self.where['d'][i - 1]
                    position = - previous_car.winfo_y() + car.winfo_y() - 35
                if position - 10 > 0:
                    car.place(y=car.winfo_y() - 10)
            i += 1


    def clearThreadingHoriz(self):
        for anyTh in self.ThreadingHorizontal:
            anyTh.cancel()
        self.ThreadingHorizontal.clear()

    def clearThreadingVert(self):
        for anyTh in self.ThreadingVertical:
            anyTh.cancel()
        self.ThreadingVertical.clear()
