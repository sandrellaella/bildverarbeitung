"""Konvertierung von Numpy-Arrays zu OpenCV-Bildobjekten und zurueck.
Wurde aus einem OpenCV-Tutorial uebernommen."""

import numpy as np
import cv

"""CV-Bilder nach numpy konvertieren"""
def cv2array(im):
    depth2dtype = { 
        cv.IPL_DEPTH_8U: 'uint8',
        cv.IPL_DEPTH_8S: 'int8',
        cv.IPL_DEPTH_16U: 'uint16',
        cv.IPL_DEPTH_16S: 'int16',
        cv.IPL_DEPTH_32S: 'int32',
        cv.IPL_DEPTH_32F: 'float32',
        cv.IPL_DEPTH_64F: 'float64',
    }
    
    arrdtype=im.depth
    a = np.fromstring(im.tostring(),dtype=depth2dtype[im.depth],
                        count=im.width*im.height*im.nChannels)
    a.shape = (im.height,im.width,im.nChannels)
    
    return a

"""Numpy-Arrays nach cv-Bild konvertieren """
def array2cv(image_num):
    dtype2depth = { 
        'uint8': cv.IPL_DEPTH_8U,
        'int8': cv.IPL_DEPTH_8S,
        'uint16': cv.IPL_DEPTH_16U,
        'int16': cv.IPL_DEPTH_16S,
        'int32': cv.IPL_DEPTH_32S,
        'float32': cv.IPL_DEPTH_32F,
        'float64': cv.IPL_DEPTH_64F,
    }
    
    try:
        nChannels=image_num.shape[2]
    except:
        nChannels=1
    cv_im=cv.CreateImageHeader((image_num.shape[1],image_num.shape[0]),dtype2depth[str(image_num.dtype)],nChannels)
    
    cv.SetData(cv_im, image_num.tostring(),image_num.dtype.itemsize*nChannels*image_num.shape[1])
    
    return cv_im