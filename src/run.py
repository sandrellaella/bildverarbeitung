import player_segmentation
import freenect
import cv
import skeletonization
import image_conversion

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
        #Erste Stufe fuer das Pruning: Gradientbild berechnen
        dist_gradient = skeleton.pruning(dist_img,1)
        
        dist_gradient_mat = image_conversion.cv2array(dist_gradient)
        dist_img_mat = image_conversion.cv2array(dist_img)
        
        diff = dist_img_mat - dist_gradient_mat
        
        diff_img = image_conversion.array2cv(diff)
        
        cv.ShowImage('Distance Image Gradientenbetrag',dist_gradient)
        cv.ShowImage('Distance Image',dist_img)
        cv.ShowImage('Differnzbild', diff_img)
        #cv.ShowImage("Compare",compare_img)        
        if cv.WaitKey(10)==27:
            break
        

run()