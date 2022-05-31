import cv2
import numpy as np

vid = cv2.VideoCapture(0)
ret, frame = vid.read()

ny,nx,nc = frame.shape

#A4 paper sheet dimensions
l = ny - 20
L = l/1.414
  
while(ret):
    ret, frame = vid.read()
    I = frame[int((ny - l)/2):int((ny + l)/2) , int((nx - L)/2):int((nx + L)/2)]
    I = cv2.cvtColor(I,cv2.COLOR_RGB2GRAY)
    I = cv2.filter2D(I,-1,1/81*np.ones((9,9)))
  
    #Affichage
    cv2.line(frame,(int((nx - L)/2),int((ny - l)/2)),(int((nx + L)/2),int((ny - l)/2)),(0,0,255),2)
    cv2.line(frame,(int((nx - L)/2),int((ny + l)/2)),(int((nx + L)/2),int((ny + l)/2)),(0,0,255),2)
    cv2.line(frame,(int((nx - L)/2),int((ny - l)/2)),(int((nx - L)/2),int((ny + l)/2)),(0,0,255),2)
    cv2.line(frame,(int((nx + L)/2),int((ny - l)/2)),(int((nx + L)/2),int((ny + l)/2)),(0,0,255),2)
    
    #Traitement
    #Calcul du gradient
    seuil = 10
    gy,gx = np.gradient(I)
    G = np.sqrt(gx**2 + gy**2)
    G_thr = 255*(G>seuil).astype(np.uint8)
    
    lines = cv2.HoughLines(G_thr,1,np.pi/360,100) #= None si trouve et rien et ca plante
    
    I2 = cv2.cvtColor(G_thr,cv2.COLOR_GRAY2RGB)
    
    dt = np.pi/18
    dr = 50
    i = 0
    h1 = False
    h2 = False
    v1 = False
    v2 = False
    T = []
    R = []
    s = np.sqrt(nx**2 + ny**2)
    
    while not(h1 and h2 and v1 and v2) and type(lines) != type(None) and i < len(lines):
        line = lines[i]
        i += 1
        for rho,theta in line:
            affichage = False
        
            if (theta < dt or theta > np.pi - dt) and rho < dr and not(v1):
                v1 = True
                affichage = True
                T.append(theta)
                R.append(rho)
                
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho + int((nx - L)/2)
                y0 = b*rho + int((ny - l)/2)
                x1 = int(x0 + s*(-b))
                y1 = int(y0 + s*(a))
                x2 = int(x0 - s*(-b))
                y2 = int(y0 - s*(a))
                cv2.line(frame,(x1,y1),(x2,y2),(255,0,0),2)
                
            elif (theta < dt or theta > np.pi - dt) and rho > L - dr and not(v2):
                v2 = True
                affichage = True
                T.append(theta)
                R.append(rho)
                
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho + int((nx - L)/2)
                y0 = b*rho + int((ny - l)/2)
                x1 = int(x0 + s*(-b))
                y1 = int(y0 + s*(a))
                x2 = int(x0 - s*(-b))
                y2 = int(y0 - s*(a))
                cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),2)
                
            elif np.pi/2 - dt < theta < np.pi/2 + dt and rho < dr and not(h1):
                h1 = True
                affichage = True
                T.append(theta)
                R.append(rho)
                
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho + int((nx - L)/2)
                y0 = b*rho + int((ny - l)/2)
                x1 = int(x0 + s*(-b))
                y1 = int(y0 + s*(a))
                x2 = int(x0 - s*(-b))
                y2 = int(y0 - s*(a))
                cv2.line(frame,(x1,y1),(x2,y2),(255,255,255),2)
                
            elif np.pi/2 - dt < theta < np.pi/2 + dt and rho > l - dr and not(h2):
                h2 = True
                affichage = True
                T.append(theta)
                R.append(rho)
                
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho + int((nx - L)/2)
                y0 = b*rho + int((ny - l)/2)
                x1 = int(x0 + s*(-b))
                y1 = int(y0 + s*(a))
                x2 = int(x0 - s*(-b))
                y2 = int(y0 - s*(a))
                cv2.line(frame,(x1,y1),(x2,y2),(255,255,0),2)
                
            if affichage:
                continue
            
    Is = cv2.hconcat([frame,cv2.resize(I2,(339,480))])        
    cv2.imshow('frame', Is)
      
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    if h1 and h2 and v1 and v2:
        print(T,R)
        break
    
    k = cv2.waitKey(100)
  
vid.release()
#cv2.destroyAllWindows()

#cv2.imshow('frame',frame)