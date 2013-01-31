# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 12:27:19 2013

@author: 8schroed
"""
import cv

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
        cv.Circle(image,(center),2,(255,0,0))


