import cv2
import numpy as np
import serial
import time
import math

class Constants:
    DISTANCE = 5.5
    BOARD_W = 1.75
    BOARD_H = 2.5
    SCREEN_W = 512
    SCREEN_H = 768 
    SCREEN_HW = SCREEN_W / 2
    SCREEN_HH = SCREEN_H / 2
    BAUD = 38400
    FADE_TIME = 2

class Utility:
    DISTANCE = 5.5

    @staticmethod
    def c2a(coord):
        return -math.degrees(math.atan2(coord, Utility.DISTANCE)) + 60;

class Movement:
    def __init__(self):
        self.drawing = False
        self.az = 60
        self.al = 60
        self.circle_centers = []
        self.last_time = 1e25

    def periodic(self, img):
        if time.time() - self.last_time > Constants.FADE_TIME:
            cx, cy, ct = self.circle_centers.pop(0)
            cv2.circle(img, (cx, cy), 3, (0, 0, 0), -1)

            if self.circle_centers:
                self.last_time = self.circle_centers[0][2]
            else:
                self.last_time = 1e25

    def record_movement(self, event, x, y, flags, img):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.az = Utility.c2a(Constants.BOARD_W / Constants.SCREEN_HW * (x - Constants.SCREEN_HW))
            self.al = Utility.c2a(Constants.BOARD_H / Constants.SCREEN_HW * (y - Constants.SCREEN_HW))

            self.circle_centers.append((x, y, time.time()))
            if self.last_time == 1e25:
                self.last_time = time.time()
            cv2.circle(img, (x, y), 6, (255, 0, 0), -1)
        elif self.drawing and event == cv2.EVENT_MOUSEMOVE:
            self.az = Utility.c2a(Constants.BOARD_W / Constants.SCREEN_HW * (x - Constants.SCREEN_HW))
            self.al = Utility.c2a(Constants.BOARD_H / Constants.SCREEN_HH * (y - Constants.SCREEN_HW))

            self.circle_centers.append((x, y, time.time()))
            if self.last_time == 1e25:
                self.last_time = time.time()
            cv2.circle(img, (x, y), 6, (255, 0, 0), -1)
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False

    def getAz(self):
        return self.az

    def getAl(self):
        return self.al

class Main:
    @staticmethod
    def main():
        ser = serial.Serial('COM8', Constants.BAUD)
        movement = Movement()
        img = np.zeros((Constants.SCREEN_H, Constants.SCREEN_W, 3), np.uint8)
        cv2.namedWindow('LaserDraw')
        cv2.setMouseCallback('LaserDraw', movement.record_movement, param=img)

        ser.read()

        while(1):
            cv2.imshow('LaserDraw', img)

            ser.write(bytes('{:+.7f}'.format(movement.getAz())[:7].encode('utf-8')))
            ser.write(bytes('{:+.7f}'.format(movement.getAl())[:7].encode('utf-8')))
            ser.read()

            movement.periodic(img)

            if cv2.waitKey(10) & 0xFF == 27:
                break

if __name__ == '__main__':
    Main.main()
