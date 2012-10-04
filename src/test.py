# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 17:32:49 2012

@author: 8schroed
"""

import cv
import image_conversion
import skeletonization
import numpy


skeleton = skeletonization.Skeleton()

img = cv.LoadImage("person.jpg")
grey_img = cv.CreateImage(cv.GetSize(img),8,1)
bin_img = cv.CreateImage(cv.GetSize(img),8,1)
dist_img = cv.CreateImage(cv.GetSize(img),32,1)
cv.CvtColor(img,grey_img,cv.CV_BGR2GRAY)

#Invertierung der Farbe, damit Mensch weiss und Hintergrund schwarz
grey_img_mat = image_conversion.cv2array(grey_img)

for i in xrange(len(grey_img_mat[:,1])):
    for j in xrange(len(grey_img_mat[1,:])):
        if grey_img_mat[i,j] == 255:
            grey_img_mat[i,j] = 0
        else:
            grey_img_mat[i,j] = 1       
grey_img = image_conversion.array2cv(grey_img_mat)
#Distance Transform
dist_img = skeleton.distance_skeleton(grey_img)

#Pruning/Segmentierung des Skeletts
dist_gradient = skeleton.pruning(dist_img,1)
dist_gradient_thresh_mat = image_conversion.cv2array(dist_gradient)
#Differenz der Distance-Map und dem segmentierten Gradientbild
dist_img_mat = image_conversion.cv2array(dist_img)
diff = dist_img_mat - dist_gradient_thresh_mat      
#Schwellwertbasierte Segmentierung des Differenzbildes. Ergibt ein schoenes Skelett
diff = 1.0 * numpy.logical_and(diff >= 0.2, diff <=1)

diff_img = image_conversion.array2cv(diff)

skeleton.component_labeling(diff)

#tracking = skeleton.tracking(diff_img) 

cv.ShowImage('Originalbild', img)
#cv.ShowImage('Distance Map',dist_img)
cv.ShowImage('Differenz',diff_img)
#cv.ShowImage('dist gradient mit Schwell', dist_gradient)

#cv.ShowImage('Tracking the Skeleton', tracking)
#cv.ShowImage('Gradient ohne Schwell', gradient)

cv.WaitKey()
