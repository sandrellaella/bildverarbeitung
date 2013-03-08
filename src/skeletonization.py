# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 17:32:49 2012

@author: Sandra Schroeder

Skelettierung mittels Distanztransformation. Zur Extraktion 
der Skelettlinie wird der Gradientenbetrag der Distance-Map bestimmt. 
Eine anschließende Differenzbildung zwischen Gradientenbetrag und
Distance-Map ergibt die Skelettlinie.

"""

import cv
import image_conversion
from scipy import ndimage
import numpy

class Skeleton():

    """Berechnung des Distanzskeletts. Vier Schritte: Berechnen der Distance Map,
    bestimmen des Gradientenbetrags der Distance Maß, segmentieren des Gradientenbetrags
    und Differenzbildung zwischen Distancemap und Gradientenbetrag (segmentiert)"""
    def distance_skeleton(self,img):
        #Ein Zielbild bereitstellen, um das Ergebnis der Distance Transformation zu speichern        
        dist_img = cv.CreateImage(cv.GetSize(img),32,1)
        #Distanztransformation
        cv.DistTransform(img, dist_img, distance_type=cv.CV_DIST_L2)
        #Konvertierung von CV-Bildobjekt zu Numpy-Array
        dist_img_mat = image_conversion.cv2array(dist_img)
        #Normalisierung der Distance Map
        max_of_dist = dist_img_mat.max()
        dist_img_mat = dist_img_mat/max_of_dist
        #Zurueck konvertieren
        dist_img = image_conversion.array2cv(dist_img_mat)
        #Erste Stufe fuer das Pruning: Gradientbild berechnen und
        #segmentieren des Gradientenbildes
        dist_gradient = self.pruning(dist_img,1)
        dist_gradient_mat = image_conversion.cv2array(dist_gradient)
        dist_img_mat = image_conversion.cv2array(dist_img)
        #Zweite Stufe für das Pruning: Differenzbild aus Distanzbild und 
        #segmentiertem Gradientenbild
        diff = dist_img_mat - dist_gradient_mat
        diff = diff * 1.0
        diff_img = image_conversion.array2cv(diff)
              
        return diff_img, dist_img
        
    #Bestimmen des Gradientenbetrages des Differenzbildes        
    def pruning(self,skeleton_img,sigma):
        skeleton_img_mat = image_conversion.cv2array(skeleton_img)
        #Ausgabe-Array fuer das Ergebnis der Gradientberechnung        
        gradient_output = numpy.empty_like(skeleton_img_mat)
        #Gradienten-Berechnung
        ndimage.gaussian_gradient_magnitude(skeleton_img_mat,sigma,gradient_output)
        #Normalisierung
        gradient_output /= gradient_output.max()
        #Array ins Bild umwandeln
        grad_img = image_conversion.array2cv(gradient_output)
        #Schwellwertbasierte Segmentierung des Gradientbildes
        dist_gradient_thresh = cv.CreateImage(cv.GetSize(grad_img),8,1)
        cv.InRangeS(grad_img,0.6,1,dist_gradient_thresh)

        return dist_gradient_thresh

