# -*- coding: utf-8 -*-
"""
Verbesserung der Skelettqualitaet des Distanzskeletts mittels
Breitensuche.

Created on Wed Jan 16 12:27:19 2013

@author: Sandra Schroeder
"""
import cv

"""Bestimmen der Features auf dem Bild image."""
def calcGoodFeatures(image):
    #Zum Speichern der Eigenwerte
    eigenvalueImage = cv.CreateImage(cv.GetSize(image),cv.IPL_DEPTH_32F,1)
    tempImage = cv.CreateImage(cv.GetSize(image),cv.IPL_DEPTH_32F,1)

    corners = []
    #Spezifikationen:
    #   Wieviele Ecken sollen gefunden werden?
    #   Welche Qualitaet?
    #   Was ist die minimale Distanz zwischen den Ecken?
    cornerCount = 10
    qualityLevel = 0.1
    minDistance = 5
    
    #Funktion zur Berechnung der Features (OpenCV Funktion)
    corners = cv.GoodFeaturesToTrack(image,eigenvalueImage,tempImage,
                                     cornerCount,qualityLevel,minDistance)
    
    return corners

"""Zeichnen der Features features in Bild image. Features werden mit
einem Kreis mit dem Radius 5 Pixel markiert."""   
def drawFeatures(features,image):
    
    for point in features:
        center = int(point[0]), int(point[1])
        cv.Circle(image,(center),5,(255,0,0))
  
"""Startfunktion der Breitensuche. Auswahl eines Startpunktes, bei dem
die Breitensuche beginnen soll und dann Aufruf einer weiteren Funktion,
die die eigentliche Breitensuche ausfuehrt."""      
def startConnect(features,searchDistance,img):
    features = [(183.0, 225.0), (174.0, 177.0), (206.0, 245.0), (205.0, 185.0), (220.0, 176.0), (25.0, 224.0), (187.0, 191.0), (191.0, 170.0), (196.0, 235.0), (176.0, 160.0), (155.0, 168.0), (266.0, 128.0), (143.0, 25.0), (83.0, 49.0), (203.0, 71.0), (156.0, 93.0), (145.0, 44.0), (150.0, 68.0), (160.0, 109.0), (168.0, 132.0), (203.0, 133.0), (185.0, 213.0), (43.0, 227.0), (99.0, 250.0), (105.0, 97.0), (91.0, 69.0), (53.0, 231.0), (146.0, 250.0), (86.0, 245.0), (164.0, 122.0), (63.0, 235.0), (153.0, 81.0), (160.0, 243.0), (172.0, 149.0), (196.0, 154.0), (200.0, 144.0), (148.0, 58.0), (203.0, 116.0), (203.0, 94.0), (117.0, 252.0), (186.0, 201.0), (203.0, 106.0), (100.0, 87.0), (232.0, 170.0), (248.0, 154.0), (257.0, 142.0), (123.0, 132.0), (134.0, 150.0), (169.0, 235.0), (140.0, 158.0)]
    startpoint = features.pop()
    #Breitensuche
    neighbours = connectFeatures(startpoint,features,searchDistance,img)
    return neighbours
 
"""Breitensuche. Beginnt mit dem Punkt startpoint und sucht nach naechsten
Nachbarn in der Liste features in einer Distanz searchDistance."""       
def connectFeatures(startpoint,features,searchDistance,img):    
    #Nachbarn des Punktes startpoint
    neighbours = []
    #Knoten, die bereits besucht wurden. Werden dann nicht mehr besucht.
    visited = []
    neighbours.append(startpoint)
    while len(neighbours) != 0:
        current = neighbours.pop()
        visited.append(current)
        #Koordinaten des aktuellen Punktes
        x = current[0]
        y = current[1]
        #Fuer jeden Punkt in der Liste der Features pruefen, ob er in der
        #Naehe des aktuellen (fest gewaehlten) Punktes current liegt.
        for f in features:
            if f not in visited:
                #Koordinaten des Features f 
                x1 = f[0]
                y1 = f[1]
                #Befuellen der temporaeren Liste. 
                #Haelt die Punkte, die am naechsten dran vom 
                #aktuellen Punkt sind.
                #Es zunaechst in x-Richtung, dann in y-Richtung geprueft.
                #Es wird ein Suchkoordinatenkreuz mit dem aktuellen 
                #Punkt im Ursprung.
                if x1>=x-searchDistance and x1<=x or x1<=x+searchDistance and x1>=x:
                    if y1>=y-searchDistance and y1<=y or y1<=y+searchDistance and y1>=y:     
                        neighbours.append((x1,y1))
                        #Verbinden des aktuellen Punktes mit dem Nachbarn, 
                        #der im Intervall liegt.
                        cv.Line(img, (int(current[0]),int(current[1])), (int(f[0]),int(f[1])), (255,255,255), thickness=2, lineType=8, shift=0)
                        #Nachbar wurde besucht und als besucht markiert.
                        #Er wird dann nicht noch einmal besucht. 
                        visited.append(f)

    return visited