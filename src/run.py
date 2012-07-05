import player_segmentation
import freenect
import cv
import skeletonization

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
        
        dist_gradient_thresh = cv.CreateImage(cv.GetSize(dist_gradient),8,1)
        
        cv.InRangeS(dist_gradient,0.9,1,dist_gradient_thresh)
        
        cv.ShowImage('Distance Image Gradientenbetrag',dist_gradient_thresh)
        cv.ShowImage('Distance Image',dist_img)
        #cv.ShowImage("Compare",compare_img)        
        if cv.WaitKey(10)==27:
            break
        

run()