"""Spielersegmentierung anhand von Tiefeninformationen

@author: Sandra Schroeder, Johannes Boehler, Christopher Kroll"""

import cv
import image_conversion
import numpy as np

"""Hauptfunktion fuer die Spielersegmentiert. Hier findet die eigentliche
Segmentierung und nachtraegliche Verbesserungen des segmentierten
Bildes statt."""      
def player_segmentation(depth_image_input,
			threshold_value,depth_value):
    
   #Umwandlung in ein Numpy-Array
   depth = image_conversion.cv2array(depth_image_input)
   
   #Schwellwerte
   threshold = threshold_value
   current_depth = depth_value
        
   #Segmentierung
   depth = 255 * np.logical_and(depth >= current_depth - threshold,
                                 depth <= current_depth + threshold)
                                 
   #depth in ein Bild umwandeln (ist bis hierhin ein Numpy-Array)
   depth = depth.astype(np.uint8)
   depth_image = cv.CreateImageHeader((depth.shape[1], depth.shape[0]), cv.IPL_DEPTH_8U,1)
   #Mit den Daten aus dem Array fuellen
   cv.SetData(depth_image, depth.tostring(),
               depth.dtype.itemsize * depth.shape[1])  
   #Glaetten
   cv.Smooth(depth_image, depth_image, smoothtype=cv.CV_GAUSSIAN, 
		param1=3, param2=0, param3=0, param4=0)
   #Dilatation um Loecher und Rauschen zu mindern
   depth_seg = dilate_image(depth_image)        

   return depth_seg, depth_image

"""Dilatation"""   
def dilate_image(img):
    #Kernels sind die strukturierten Elemente fuer die Dilatation. 
    #Hier wurden rechteckige und elliptische Elemente gewaehlt.
    #kernel=cv.CreateStructuringElementEx(3, 3, 0, 0, cv.CV_SHAPE_RECT)
    kernel=cv.CreateStructuringElementEx(5, 5, 0, 0,cv.CV_SHAPE_ELLIPSE)
    #In einem neuen Bild speichern
    img_dil = cv.CreateImage(cv.GetSize(img),8,1)
    #Dilatation
    cv.Dilate(img,img_dil,kernel,iterations=2)
    return img_dil
