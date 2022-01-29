import cv2
import numpy as np
import time
import math


cap = cv2.VideoCapture(-1)

window = 'Threshold'
EMPTY_THRESHOLD = 10000000
THRESHOLDS = [0,8000,8005,EMPTY_THRESHOLDS,math.inf]
CLASSES = ['MALE','UNSEGREGATED','FEMALE','EMPTY']
#THRESHOLD_MALE = 20000//2


def empty(pos):
	pass

#TH_list= [0 , 90(78) ,90(78) ,19(25),]
def create_color_threshold_window():
	cv2.namedWindow(window)
	cv2.createTrackbar('Rl','Threshold',0,255,empty)
	cv2.createTrackbar('Gl','Threshold',78,255,empty)
	cv2.createTrackbar('Bl','Threshold',78,255,empty)
	cv2.createTrackbar('Rh','Threshold',25,255,empty)
	cv2.createTrackbar('Gh','Threshold',255,255,empty)
	cv2.createTrackbar('Bh','Threshold',255,255,empty)
values = []
tot = 0
frameNo = 0

y1,y2,x1,x2 = 160,360,100,460
#y1,y2,x1,x2 = 235,260,240,273
GREEN = (0,255,0)
thickness = 1
sm = 0
empty_sm = 0
PIN_MALE,PIN_UNSPECIFIED,PIN_FEMALE,PIN_EMPTY = [23,24,25,19]
RELAY_PINS=[PIN_MALE,PIN_UNSPECIFIED,PIN_FEMALE,PIN_EMPTY]
DURATION  = 1
