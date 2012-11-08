import player_segmentation
import freenect
import cv
import skeletonization
import image_conversion
import numpy
import depth
def run():
    threshold_value = 40 
    depth_value = 90
    skeleton = skeletonization.Skeleton()
    count = 0
    while True:
        
        #Kinect starten (Tiefenbild)
        #depth, timestamp = freenect.sync_get_depth()
        depth_image2 = depth.get_better_depth()
        #spielersegmentierung 
        depth_seg,depth_image = player_segmentation.player_segmentation(depth_image2,threshold_value,depth_value)        
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
        #diff = numpy.logical_and(diff>=0.2,diff<1)
        diff = diff * 1.0
        diff_img = image_conversion.array2cv(diff)
        #cv.ShowImage('Distance Image Gradientenbetrag',dist_gradient)
        #cv.ShowImage('Distance Image',dist_img)
       
        count = count + 1        
        
        cv.ShowImage('Spieler', depth_seg)
        cv.ShowImage('diff', diff_img)
        cv.ShowImage('dist_gradient',dist_gradient)
        cv.ShowImage('Better Depth', depth_image2)
         
                
        if cv.WaitKey(10)==27:
            break
        

run()