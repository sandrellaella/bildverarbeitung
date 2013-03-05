import cv
import image_conversion
#import freenect
#import frame_convert
import numpy as np
      
def player_segmentation(depth_image_input,threshold_value,depth_value):
    
    
   depth = image_conversion.cv2array(depth_image_input)
   #print depth
   #capture=cv.CaptureFromCAM(CAM_NUMBER)
   threshold = threshold_value
   current_depth = depth_value
   #Tiefenbild -> kommt jetzt von run.py
   #depth, timestamp = freenect.sync_get_depth()
        
   #Segmentierung
   depth = 255 * np.logical_and(depth >= current_depth - threshold,
                                 depth <= current_depth + threshold)
   #depth in ein Bild umwandeln (ist bis hierhin ein numpy-array)
   depth = depth.astype(np.uint8)
   depth_image = cv.CreateImageHeader((depth.shape[1], depth.shape[0]), cv.IPL_DEPTH_8U,1)
   #mit Daten fuellen
   cv.SetData(depth_image, depth.tostring(),
               depth.dtype.itemsize * depth.shape[1])
      
   #Glaetten
   cv.Smooth(depth_image, depth_image, smoothtype=cv.CV_GAUSSIAN, param1=3, param2=0, param3=0, param4=0)
   #Dilatation um Loecher und Rauschen zu mindern
   depth_seg = dilate_image(depth_image)        

   return depth_seg, depth_image

#Dilatation anwenden    
def dilate_image(img):
    #kernel=cv.CreateStructuringElementEx(3, 3, 0, 0, cv.CV_SHAPE_RECT)
    kernel=cv.CreateStructuringElementEx(5, 5, 0, 0,cv.CV_SHAPE_ELLIPSE)
    #In einem neuen Bild speichern
    img_dil = cv.CreateImage(cv.GetSize(img),8,1)
    #Dilatation
    cv.Dilate(img,img_dil,kernel,iterations=2)
    #img_dil = erode_image(img_dil)
    return img_dil
    
def erode_image(img,iters):
    kernel=cv.CreateStructuringElementEx(3, 3, 0, 0, cv.CV_SHAPE_RECT)
    img_erode = cv.CreateImage(cv.GetSize(img),8,1)
    img_mat = image_conversion.cv2array(img)
    img_uint8 = cv.CreateImage(cv.GetSize(img),8,1)
    
    if img_mat.dtype == 'float32':
        cv.ConvertScale(img, img_uint8)
        img_erode = cv.CreateImage(cv.GetSize(img_uint8),8,1)
        cv.Erode(img_uint8,img_erode,kernel,iterations=iters)
        return img_erode
    else:
        cv.Erode(img,img_erode,kernel,iterations=iters)
        return img_erode

