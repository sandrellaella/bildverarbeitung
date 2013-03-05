# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 12:27:19 2013

@author: 8schroed
"""
import cv
import numpy

filename = "hand.jpg"
image = cv.LoadImage(filename,cv.CV_LOAD_IMAGE_GRAYSCALE)

def calcGoodFeatures(image):
    #grayImage = cv.LoadImage(image,2)
    eigenvalueImage = cv.CreateImage(cv.GetSize(image),cv.IPL_DEPTH_32F,1)
    tempImage = cv.CreateImage(cv.GetSize(image),cv.IPL_DEPTH_32F,1)
    
    
    corners = []
    cornerCount = 50
    qualityLevel = 0.1
    minDistance = 10
    
    corners = cv.GoodFeaturesToTrack(image,eigenvalueImage,tempImage,
                                     cornerCount,qualityLevel,minDistance)
    
    return corners
    
def drawFeatures(features,image):
    
    for point in features:
        center = int(point[0]), int(point[1])
        cv.Circle(image,(center),5,(255,0,0))
        
def startConnect(features,minDistance,epsilon,img):
    print features
    searchDistance = minDistance + epsilon
    startpoint = features.pop()
    
    neighbours = connectFeatures(startpoint,features,searchDistance,img)
    return neighbours
        
def connectFeatures(startpoint,features,searchDistance,img):    
    
    neighbours = []
    #Besuchte Knoten
    visited = []
    neighbours.append(startpoint)
    while len(neighbours) != 0:
        current = neighbours.pop()
        visited.append(current)
        x = current[0]
        y = current[1]
        for f in features:
        #print startpoint
            if f not in visited:
                x1 = f[0]
                y1 = f[1]
                #Befuellen der temporaeren Liste. Haelt die Punkte, die am naechsten dran vom aktuellen Punkt sind
                if x1>=x-searchDistance and x1<=x or x1<=x+searchDistance and x1>=x:
                    if y1>=y-searchDistance and y1<=y or y1<=y+searchDistance and y1>=y:        
                        neighbours.append((x1,y1))
                        cv.Line(img, (int(current[0]),int(current[1])), (int(f[0]),int(f[1])), (255,255,255), thickness=2, lineType=8, shift=0)
                        visited.append(f)
                  

    
    return visited