import player_segmentation
import freenect
import cv
import skeletonization
import image_conversion
import numpy

def run():
    threshold_value = 170 
    depth_value = 745
    skeleton = skeletonization.Skeleton()
    count = 0
    depth_list = []
    while True:
        
        #Kinect starten (Tiefenbild)
        depth, timestamp = freenect.sync_get_depth()
        
        #spielersegmentierung 
        depth_seg,depth_image = player_segmentation.player_segmentation(depth,timestamp,threshold_value,depth_value)
        depth_list.insert(count,depth_image)
        img_contour = player_segmentation.find_contour(depth_image)
        #distance map berechnen
        dist_img = skeleton.distance_skeleton(depth_seg)
        #TEST
        #dist_img = skeleton.distance_skeleton(depth_image)        
        #Erste Stufe fuer das Pruning: Gradientbild berechnen
        dist_gradient = skeleton.pruning(dist_img,1)
        
        dist_gradient_mat = image_conversion.cv2array(dist_gradient)
        dist_img_mat = image_conversion.cv2array(dist_img)
        #Differenzbild aus Distanzbild und segmentiertem Gradientenbild
        diff = dist_img_mat - dist_gradient_mat
        
        
        diff = numpy.logical_and(diff > 0.2, diff <= 0.2)
        diff_img = image_conversion.array2cv(diff*1.0)
        #cv.ShowImage('Distance Image Gradientenbetrag',dist_gradient)
        #cv.ShowImage('Distance Image',dist_img)
        
        cv.ShowImage('Tiefenbild',depth_image)
        cv.ShowImage('Spieler', depth_seg)
        cv.ShowImage('diff', diff_img)
        cv.ShowImage('Kontur', img_contour)
        
        
       
        
        count = count + 1
       
                
        if cv.WaitKey(10)==27:
            break
        

run()