# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 12:27:19 2013

@author: 8schroed
"""
import cv
import image_conversion

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
    
    corners = cv.GoodFeaturesToTrack(image,eigenvalueImage,tempImage,cornerCount,qualityLevel,minDistance)
    
    #(x,y) = corners[0]
    #(m,n) = corners[1] 
       
    #cv.Circle(image,(int(x),int(y)) ,5,(255,0,0))
    #cv.Circle(image,(int(m),int(n)),5,(255,0,0))
    
    return corners
        
    #while True:
     #   cv.ShowImage("Image",image)
      #  if cv.WaitKey(10)==27:
       #     break
    #return corners
    
def drawFeatures(features,image):
    
    for point in features:
        center = int(point[0]), int(point[1])
        cv.Circle(image,(center),5,(255,0,0))
        
def connectFeatures(image,features,minDistance):
    epsilon = 5
    searchDistance = minDistance + epsilon  
    feature = features.pop()
    
    x = feature[0]
    y = feature[1]
    
    found = True
    templist = []
    while found:
        if features:
           for f in features:
               x1 = f[0]
               y1 = f[1]
               if x1>=x-searchDistance and x1<=x or x1<=x+searchDistance and x1>=x:
                   if y1>=y-searchDistance and y1<=y or y1<=y+searchDistance and y1>=y:
                       templist.append((x1,y1))
                       print templist
                       found = False

    return 0

