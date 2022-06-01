#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 16:39:02 2022

@author: axel.nael
"""

"""
L'indication de mesure et la clé sont repérées comme notes
Hough n'est pas forcément le mieux pour les dièses et les bémols, les barres de mesures sont aussi détectées avec ca
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('./Images/im4.jpg')
img = img[int(0.02*img.shape[0]):int(0.98*img.shape[0]) , int(0.02*img.shape[1]):int(0.98*img.shape[1])]

if (len(img.shape) == 3):
    ny,nx,nc = img.shape
    I = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

I = cv2.adaptiveThreshold(I, 255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 31, 15)
I = 255 - I

d = int(0.9*I.shape[0]/140)
d2 = int(0.25*I.shape[0]/140)
SE = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (d,d))
SE2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (d2,d2))

d = int(I.shape[0]/140)

I_f = cv2.morphologyEx(I, cv2.MORPH_CLOSE, SE2, iterations = 1)

I_e = cv2.erode(I_f,SE)

notes = np.argwhere(I_e == 255) #Listes des coordonnées des "notes"
notes_traitees = [] #Liste des positions des notes

for n in notes:
    treated = False
    #On vérifie si la note a déjà été traitée
    for k in notes_traitees:
        if abs(k[0] - n[0]) < d and abs(k[1] - n[1]) < d:
            treated = True
            break
        
    V = [] #Voisinage de la note
    for k in notes:
        if abs(k[0] - n[0]) < d and abs(k[1] - n[1]) < d:
            V.append(k)
    #Calcul du barycentre du voisinage et ajout de ce dernier à la liste des notes traitées    
    if not(treated):
        B = [int(sum([V[k][0] for k in range(len(V))])/len(V)) , int(sum([V[k][1] for k in range(len(V))])/len(V))]
        notes_traitees.append(B)
res = cv2.cvtColor(I,cv2.COLOR_GRAY2RGB)
for n in notes_traitees:
    temp = I[n[0] - 2*d : n[0] + 2*d , n[1] - 2*d : n[1] - int(3*d/4)]
    temp = cv2.morphologyEx(temp,cv2.MORPH_TOPHAT,np.ones((1,d)))
    temp = cv2.morphologyEx(temp,cv2.MORPH_CLOSE,np.ones((3,3)))
    lines = cv2.HoughLines(temp,1,np.pi,15)
    
    s = 8*d
    if type(lines) != type(None):
        for l in lines[:8]:
            for rho,theta in l:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho + n[1] - 2*d
                y0 = b*rho + n[0] - 2*d
                x1 = int(x0 + s*(-b))
                y1 = int(y0 + s*(a))
                x2 = int(x0 - s*(-b))
                y2 = int(y0 - s*(a))
                print(n,x1,y1,x2,y2)
                cv2.line(res,(x1,y1),(x2,y2),(255,0,0),1)
                
plt.imshow(res,'gray')