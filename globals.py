import cv2
import numpy as np
import time
import math


cap = cv2.VideoCapture(-1)

window = 'Threshold'
THRESHOLDS = [0,30000,31000,math.inf]
CLASSES = ['MALE','UNSEGREGATED','FEMALE']
#THRESHOLD_MALE = 20000//2


def empty(pos):
	pass


cv2.namedWindow(window)
cv2.createTrackbar('Rl','Threshold',0,255,empty)
cv2.createTrackbar('Gl','Threshold',35,255,empty)
cv2.createTrackbar('Bl','Threshold',70,255,empty)
cv2.createTrackbar('Rh','Threshold',40,255,empty)
cv2.createTrackbar('Gh','Threshold',255,255,empty)
cv2.createTrackbar('Bh','Threshold',255,255,empty)
values = []
tot = 0
frameNo = 0

y1,y2,x1,x2 = 205,260,210,320
#y1,y2,x1,x2 = 235,260,240,273
GREEN = (0,255,0)
thickness = 1
sm = 0
PIN_MALE,PIN_UNSPECIFIED,PIN_FEMALE = [23,24,25]
RELAY_PINS=[PIN_MALE,PIN_UNSPECIFIED,PIN_FEMALE]
DURATION  = 1
