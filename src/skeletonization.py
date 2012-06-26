# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 17:32:49 2012

@author: 8schroed
"""

import cv
import image_conversion

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
        
        return dist_img        
        
        #show the original image and the (normalised) result
        #cv.ShowImage('Original Image',img)

        #cv.WaitKey()
        
    def morph_skeleton(self,img):
        #TODO 
        return 0

#skeleton = Skeleton()
#img = "barcode.png"
#skeleton.distance_skeleton(img)
