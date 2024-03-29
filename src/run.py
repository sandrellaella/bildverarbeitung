"""
Startup der Skelettierung. Hier findet die Segmentierung des Spielers und
die Skelettierung (nach Thinning oder Distanztransformation) statt.

@author: Sandra Schroeder
"""

import player_segmentation
import cv
import skeletonization
import image_conversion
import numpy
import depth
import pythonWrapper

def run(algorithm):
    #Schwellwerte fuer die Segmentierung des Spielers
    threshold_value = 40 
    depth_value = 170
    skeleton = skeletonization.Skeleton()
    while True:          
        #Tiefenbild erzeugen 
        depthvalues = depth.get_better_depth()
        #Spielersegmentierung 
        depth_seg,depth_image = player_segmentation.player_segmentation(depthvalues,threshold_value,depth_value)   
        #Glaetten des segmentierten Bildes
        cv.Smooth(depth_seg, depth_seg, smoothtype=cv.CV_MEDIAN, param1=5, param2=5)
        
        #Distance Map berechnen und das Skelett daraus extrahieren
        if algorithm=="distancetransform":
            diff_img,dist_gradient = skeleton.distance_skeleton(depth_seg)
            diff = image_conversion.cv2array(diff_img)
            diff = 255.0 * numpy.logical_and(diff >= 0.2, diff<=1)
            diff = diff.astype(numpy.uint8)
            diff_img = image_conversion.array2cv(diff)
        
        #Skelettierung mittels Thinning. Innerhalb von Python-Wrapper
        #wird ein C++-Programm aufgerufen, in dem das Thinning
        #implementiert ist. 
        elif algorithm=="thinning":
            greyscale_array = image_conversion.cv2array(depth_seg)
            new_g = greyscale_array.reshape((480,640))
            new_g = pythonWrapper.reflectimage_band(new_g,1)              

        #Anzeige des Spielers (segmentiert) und des Distanz-Skeletts 
        cv.ShowImage('Spieler', depth_seg)
        cv.ShowImage('Distanz-Skeltt', diff_img)
    
        if cv.WaitKey(10)==27:
            break

#Auswahl des Algorithmus und Ausfuehrung
algorithm="distancetransform"
#algorithm="thinning"
run(algorithm)