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

depth_list_global = [] 

def get_depth():
    return frame_convert.pretty_depth(freenect.sync_get_depth()[0])

def get_depth2():
    return freenect.sync_get_depth()[0]
    
def save_depth_map(depth_list,depth_map):
    depth_list.append(depth_map)
    
def get_depth_map(depth_list,index):
    depth_map = depth_list[index]
    return depth_map
    

def get_better_depth():    
    depth = get_depth()
   
    depth = numpy.where(depth == 255, 0, depth)
    
    
    depth_img = image_conversion.array2cv(depth)
    #cv.Smooth(depth_img, depth_img, smoothtype=cv.CV_GAUSSIAN, param1=3, param2=0, param3=0, param4=0)
   
    return depth_img

#while 1:
 #   cv.ShowImage('Depth Image', get_better_depth())
  #  if cv.WaitKey(10)==27:
   #     break