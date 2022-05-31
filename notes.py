# -*- coding: utf-8 -*-
"""
Created on Thu May 26 17:37:24 2022

@author: jonat
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    img = cv2.imread('./Images/Simple/im1.png')
    I = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    I = 255-I
    #I = cv2.resize(I,(int(I.shape[1]/2),int(I.shape[0]/2)))
    
    nx = I.shape[1]
    ny = I.shape[0]
    
    #BH = cv2.morphologyEx(I,cv2.MORPH_BLACKHAT,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7)))
    test = cv2.erode(I,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7)))
    TH = cv2.morphologyEx(test,cv2.MORPH_TOPHAT,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7)))
    
    plt.imshow(TH,'gray')