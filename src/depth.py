# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 10:05:56 2012

@author: Sandra Schroeder

Funktionen fuer den Zugriff auf die Tiefenwerte, die die Kinect liefert."""

import cv
import freenect
import frame_convert
import image_conversion
import numpy


def get_depth():
    return frame_convert.pretty_depth(freenect.sync_get_depth()[0])

#def get_depth2():
 #   return freenect.sync_get_depth()[0]
    
#def save_depth_map(depth_list,depth_map):
 #   depth_list.append(depth_map)
    
#def get_depth_map(depth_list,index):
 #   depth_map = depth_list[index]
  #  return depth_map
    
"""Kleine Verbesserungen des Tiefenbildes."""
def get_better_depth():    
    depth = get_depth()
    #Tiefenwert gleich 255. Dies ist der Fall, wenn die Tiefe von der
    #Kinect nicht gemessen werden kann. Diese Werte werden auf null gesetzt.
    depth = numpy.where(depth == 255, 0, depth)
    depth_img = image_conversion.array2cv(depth)
    #Glätten des Tiefenbildes
    cv.Smooth(depth_img, depth_img, smoothtype=cv.CV_MEDIAN, param1=5, param2=5)
   
    return depth_img