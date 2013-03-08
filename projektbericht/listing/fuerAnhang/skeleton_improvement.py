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