# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 17:32:49 2012

@author: 8schroed
"""
import cv
import image_conversion
import skeletonization
import numpy
import comparison

    

skeleton = skeletonization.Skeleton()

def test(image):

    grey_img = cv.CreateImage(cv.GetSize(image),8,1)
    dist_img = cv.CreateImage(cv.GetSize(image),32,1)
    cv.CvtColor(image,grey_img,cv.CV_BGR2GRAY)

    #Invertierung der Farbe, damit Objekt weiss und Hintergrund schwarz
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
    diff = 255.0 * numpy.logical_and(diff >= 0.2, diff <=1)
    #diff = diff.astype(numpy.float32)
    diff = diff.astype(numpy.uint8)
    diff_img = image_conversion.array2cv(diff)
    

    features = comparison.calcGoodFeatures(diff_img)
    
    #return features, image, dist_img, diff_img, drawImage
    return diff_img, features
    
img = cv.LoadImage("hand.jpg")
#img2 = cv.LoadImage("person.jpg")

#corners1, image1, dist_img1, diff_img1, drawImage = test(img)
#corners2, image2, dist_img2, diff_img2 = test(img2)
diff_img, features = test(img)
comparison.drawFeatures(features,diff_img)
comparison.connectFeatures(diff_img,features,10)
#print corners1
#print corners2
#print features
cv.ShowImage("Diff-Image", diff_img)
#cv.ShowImage('Originalbild', image1)
#cv.ShowImage('Distance Map',dist_img1)
#cv.ShowImage('Differenz',diff_img1)
#cv.ShowImage("Zeichnung",drawImage)

#cv.ShowImage('Originalbild2', image2)
#cv.ShowImage('Distance Map2',dist_img2)
#cv.ShowImage('Differenz2',diff_img2)

cv.WaitKey()
