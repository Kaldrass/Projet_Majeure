import cv2
import numpy as np
import matplotlib.pyplot as plt

I = cv2.imread('ProjetMajeure\Images\im4.jpg')
I = cv2.cvtColor(I,cv2.COLOR_RGB2GRAY)

sol = cv2.imread('ProjetMajeure\Images\clefdesol.png')
sol = cv2.cvtColor(sol,cv2.COLOR_RGB2GRAY)


def threshold(I,seuil):
    return cv2.threshold(I,seuil,255,cv2.THRESH_BINARY)[1]
def hotsu(I,size,C): #size doit être impair et au moins 3
    return cv2.adaptiveThreshold(I,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,size,C)
def dilate(I,x,y):
    return cv2.dilate(I,np.ones((y,x)))

def erode(I,x,y):
    return cv2.erode(I,np.ones((x,y)))
def bottomhat(I):
    return cv2.morphologyEx(I,cv2.MORPH_BLACKHAT,np.ones((11,11)))
def gradient(I,x,y):
    return cv2.morphologyEx(I,cv2.MORPH_GRADIENT,np.ones((y,x)))

def skeletonization(I):
    skel = np.zeros(I.shape,np.uint8)
    cross = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    while True:
        eroded = cv2.erode(I,cross)
        temp = cv2.dilate(eroded,cross)
        temp = cv2.subtract(I,temp)
        skel = cv2.bitwise_or(skel,temp)
        I = eroded.copy()
        if cv2.countNonZero(I) == 0:
            break
    return skel 

    

## Détection de la clef et de l'armure

J = hotsu(I,31,15) # 90x40 pour la clef de sol
sol = threshold(sol, 96)
sol = sol/255 # on binarise sol
sol = sol.astype(np.uint8)

sol = cv2.resize(sol,(3*sol.shape[1]//40,3*sol.shape[0]//40))
sol = skeletonization(1-sol)
sol = 1-sol

plt.imshow(sol, 'gray')
plt.show()
plt.imshow(J, 'gray')
plt.show()
