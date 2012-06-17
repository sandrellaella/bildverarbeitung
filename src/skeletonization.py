# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 17:32:49 2012

@author: 8schroed
"""

import player_segmentation as ps
import cv

img = cv.LoadImage("rechteck.gif")
grey_img = cv.CreateImage(cv.GetSize(img),32,1)
bin_img = cv.CreateImage(cv.GetSize(img),8,1)
cv.CvtColor(img,grey_img,cv.CV_BGR2GRAY)

threshold = 100
colour = 255
cv.Threshold(grey_img,bin_img,threshold,colour,cv.CV_THRESH_BINARY)

ps.dist_transform(bin_img)


