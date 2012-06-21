# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 17:32:49 2012

@author: 8schroed
"""

import player_segmentation as ps
import cv
import image_conversion

img = cv.LoadImage("barcode.png")
grey_img = cv.CreateImage(cv.GetSize(img),8,1)
bin_img = cv.CreateImage(cv.GetSize(img),8,1)
dist_img = cv.CreateImage(cv.GetSize(img),32,1)
cv.CvtColor(img,grey_img,cv.CV_BGR2GRAY)

threshold = 100
colour = 255
cv.Threshold(grey_img,bin_img,threshold,colour,cv.CV_THRESH_BINARY)

cv.DistTransform(bin_img, dist_img, distance_type=cv.CV_DIST_L2)

cv.ConvertScale(dist_img, dist_img, 5000.0, 0)
cv.Pow(dist_img, dist_img, 0.5)


cv.ShowImage('Distance',dist_img)

cv.WaitKey()
