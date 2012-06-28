import player_segmentation
import freenect
import cv
import skeletonization
from scipy import ndimage
import image_conversion
#import numpy

def run():
    threshold_value = 159 
    depth_value = 745
    skeleton = skeletonization.Skeleton()
    while True:
        #Kinect starten (Tiefenbild)
        depth_img, timestamp = freenect.sync_get_depth()
		#spielersegmentierung
        depth_seg = player_segmentation.player_segmentation(depth_img,timestamp,threshold_value,depth_value)
        #distance map berechnen
        dist_img = skeleton.distance_skeleton(depth_seg)
        
        dist_img_mat = image_conversion.cv2array(dist_img)       
       
        ndimage.morphological_gradient(dist_img_mat, (3,3))
        
        cv.ShowImage('Distance Image',dist_img)
        if cv.WaitKey(10)==27:
            break
        

run()