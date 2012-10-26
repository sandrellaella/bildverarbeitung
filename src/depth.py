# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 10:05:56 2012

@author: 8schroed
"""

import cv
import freenect
import frame_convert
import image_conversion
import numpy

def get_depth():
    return frame_convert.pretty_depth(freenect.sync_get_depth()[0])

def depth2():
    return freenect.sync_get_depth()[0]
    
#def depth3():
#    return freenect.sync_get_depth()

def correct():
    depth = image_conversion.cv2array(get_depth())
    numpy.where(depth == 0, 0, 255)    
    depth_image=image_conversion.array2cv(depth)
    return depth_image
    
def correct2():
    depth = depth2()
    #depth = depth2()
    depth = numpy.where(depth == 2047, 750, depth)
    #depth_image = image_conversion.array2cv(depth)  
    return depth
    
    
def show(): 
    depth_image = correct2()
    cv.ShowImage('Korrektur',depth_image)

#while True:
 #   show()
  #  #cv.ShowImage('Normal', get_depth())
   # if cv.WaitKey(10) == 27:
    #    break