#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 31 15:24:21 2022
@author: jonathan.bouyer
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np

def line_evaluator(rho,theta,x):
    return rho/np.sin(theta) - x/np.tan(theta)

I = cv2.imread('./Images/im1.png')
ny,nx,nc = I.shape
I = cv2.cvtColor(I,cv2.COLOR_RGB2GRAY)
ret, thresh1 = cv2.threshold(I, 120, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
I = 255 - 255 * (I>70).astype(np.uint8)

d = int(I.shape[0]/230)
SE = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (d,d))

I_e = cv2.erode(I,SE)
I_th = I_e - cv2.morphologyEx(I_e, cv2.MORPH_OPEN, SE)
plt.imshow(I_th,'gray')

#Positionnement des portées
res = cv2.imread('./Images/im1.png')
lines = cv2.HoughLines(I,1,np.pi/1000,1200) 
s = np.sqrt(nx**2 + ny**2)
T = []
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
            T.append(theta)
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

#TEST
D = 0
for k in range(1,len(R)):
    if not(k%5 == 0):
        D += R[k] - R[k-1]
d = D/((len(R)//5)*4)
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

#Evaluation des notes
TH = {(529, 1802): -0.5,
 (548, 2110): 0,
 (551, 1491): 0.5,
 (562, 2418): 0.5,
 (562, 653): 1,
 (564, 1193): 1,
 (573, 385): 1.5,
 (609, 923): 3,
 (1009, 897): 6,
 (1010, 335): 6,
 (1011, 1180): 6,
 (1021, 616): 6.5,
 (1030, 2108): 6.5,
 (1049, 1801): 7.5,
 (1057, 2414): 7.5,
 (1060, 1490): 8,
 (1445, 334): 10.5,
 (1446, 616): 10.5,
 (1461, 899): 11,
 (1463, 1181): 11,
 (1478, 2105): 11.5,
 (1501, 1794): 12.5,
 (1501, 2413): 12.5,
 (1512, 1487): 13,
 (1905, 333): 16,
 (1905, 619): 16,
 (1916, 903): 16.5,
 (1930, 1183): 17,
 (1942, 1487): 17.5}

tones = {}
droites = sorted(zip(R,T))
for n in notes_traitees:
    x = n[1]
    y = n[0]
    
    h = 0
    minimum = max(R) + 1
    
    i = 0
    while i < len(droites) and droites[i][0] < y + 2*d:
        y_portee = line_evaluator(droites[i][0],droites[i][1],x)
        
        if abs(y_portee - y) < abs(minimum):
            minimum = y_portee - y
            h = i
            
        i += 1
    if minimum >= d/2:
        h -= 0.5
    elif minimum <= -d/2:
        h += 0.5
        
    tones[(y,x)] = h
    
err = 0
for t in tones.keys():
    if tones[t] != TH[t]:
        err += 1
print(err)