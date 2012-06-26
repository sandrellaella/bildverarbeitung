import numpy as np
import cv

#CV-Bilder nach numpy konvertieren
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

#Numpy-Arrays nach cv-Bild konvertieren    
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
    
#In ein Graubild umwandeln (mit numpy)
#FIXME: Brauchen wir das ueberhaupt? Geht ja auch mit opencv
def convert_to_grey(img_col): 
    #cv Bild in numpy-array umwandeln
    img_num = cv2array(img_col)
    #Datentyp von img_num erweitern, da sonst Overflow, denn 
    #img_num hat den Datentyp uint8. Hiermit wird der Datentyp
    #auf int32 erweitert.
    img_num = img_num.astype(np.int)
    
    #Kanaele separieren
    #roter Kanal
    r = img_num[:,:,0]
    #gruener Kanal
    g = img_num[:,:,1]
    #blauer Kanal
    b = img_num[:,:,2]
    
    #In Graubild umwandeln
    img_gray = (r+g+b)/3
    #und zurueckkonvertieren in uint8 (sonst kommt ein schwarzes Bild)
    img_gray = img_gray.astype(np.uint8)
    #umgewandeltes Bild zurueckgeben
    return img_gray
    
#path="/home/sandra/papagei.jpg"
#image=cv.LoadImage(path,cv.CV_LOAD_IMAGE_COLOR)
#cv.NamedWindow("Window",cv.CV_WINDOW_AUTOSIZE)
#cv.ShowImage("Window",image)
#cv.WaitKey()
