# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 17:32:49 2012

@author: 8schroed
"""

import cv
import image_conversion
from scipy import ndimage
import numpy

class Skeleton():

    def distance_skeleton(self,img):
    
        #img = cv.LoadImage(img)

        #Create an image for the greyvalue image of the original image
        #grey_img = cv.CreateImage(cv.GetSize(img),8,1)
        #create an image for the distance map
        dist_img = cv.CreateImage(cv.GetSize(img),32,1)

        #conversion to greyvalue image
        #cv.CvtColor(img,grey_img,cv.CV_BGR2GRAY)
        
        #distance transform
        cv.DistTransform(img, dist_img, distance_type=cv.CV_DIST_L2)
        #conversion to numpy-array
        dist_img_mat = image_conversion.cv2array(dist_img)
        #normalise the distance image
        max_of_dist = dist_img_mat.max()
        dist_img_mat = dist_img_mat/max_of_dist
        #conversion back to cv-image
        dist_img = image_conversion.array2cv(dist_img_mat)
        
        #TEST
        #dist_img = skeleton.distance_skeleton(depth_image)        
        #Erste Stufe fuer das Pruning: Gradientbild berechnen
        dist_gradient = self.pruning(dist_img,1)
        
        dist_gradient_mat = image_conversion.cv2array(dist_gradient)
        dist_img_mat = image_conversion.cv2array(dist_img)
        #Differenzbild aus Distanzbild und segmentiertem Gradientenbild
        diff = dist_img_mat - dist_gradient_mat
        #diff = numpy.logical_and(diff>=0.2,diff<1)
        diff = diff * 1.0
        diff_img = image_conversion.array2cv(diff)
        #cv.ShowImage('Distance Image Gradientenbetrag',dist_gradient)
        #cv.ShowImage('Distance Image',dist_img)
        
        return diff_img        
        
        #show the original image and the (normalised) result
        #cv.ShowImage('Original Image',img)

        #cv.WaitKey()
        
    def pruning(self,skeleton_img,sigma):
        skeleton_img_mat = image_conversion.cv2array(skeleton_img)
        #Ausgabe Array fuer das Ergebnis der Gradientberechnung        
        gradient_output = numpy.empty_like(skeleton_img_mat)
        #Gradienten-Berechnung
        ndimage.gaussian_gradient_magnitude(skeleton_img_mat,sigma,gradient_output)
        #Normalisierung
        gradient_output /= gradient_output.max()
        #Array ins Bild umwandeln
        grad_img = image_conversion.array2cv(gradient_output)
        #Schwellwertbasierte Segmentierung des Gradientbildes
        dist_gradient_thresh = cv.CreateImage(cv.GetSize(grad_img),8,1)
        cv.InRangeS(grad_img,0.8,1,dist_gradient_thresh)

        return dist_gradient_thresh
        
        
 

