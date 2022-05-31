#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 31 15:24:21 2022

@author: jonathan.bouyer
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np

I = cv2.imread('./Images/im1.png')
ny,nx,nc = I.shape
I = cv2.cvtColor(I,cv2.COLOR_RGB2GRAY)
I = 255 - 255 * (I>70).astype(np.uint8)

d = int(I.shape[0]/230)
SE = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (d,d))

I_e = cv2.erode(I,SE)
I_th = I_e - cv2.morphologyEx(I_e, cv2.MORPH_OPEN, SE)
plt.imshow(I_th,'gray')

#Repérage des notes
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
        
res_notes = cv2.imread('./Images/im1.png')

for b in notes_traitees:
    res_notes[b[0]-5:b[0]+5,b[1]-5:b[1]+5,0] = 255
    
plt.imshow(res_notes)

#Positionnement des portées
res = cv2.imread('./Images/im1.png')
lines = cv2.HoughLines(I,1,np.pi/1000,1200) 
s = np.sqrt(nx**2 + ny**2)
droites = [[],[]]
R = []
dr = d
nb = 0
for l in lines:
    R.sort()
    for rho,theta in l:
        treated = False
        if len(R) > 0:
            i = 0
            while (i < len(R) and R[i] < rho + d):
                if abs(rho - R[i]) < d:
                    treated = True
                i += 1
        if not(treated):
            R.append(rho)
            droites[0].append(rho)
            droites[1].append(theta)
            nb += 1
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + s*(-b))
            y1 = int(y0 + s*(a))
            x2 = int(x0 - s*(-b))
            y2 = int(y0 - s*(a))
            cv2.line(res,(x1,y1),(x2,y2),(255,0,0),1)
            
plt.imshow(res)

#Evaluation des notes
tone = []

for n in notes_traitees:
    