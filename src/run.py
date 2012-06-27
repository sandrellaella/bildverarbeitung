import player_segmentation
import freenect
import cv
import skeletonization
#import image_conversion
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
		
        
        #skeleton pruning
		#Theoretisch duerften hier nur die Pixel uebrigbleiben, die gleich 1 sind
		cv.CmpS(dist_img,1,dist_img,cv.CV_CMP_EQ)

        cv.ShowImage('Spieler',depth_seg)  
        cv.ShowImage('Distance Image',dist_img)
        
        if cv.WaitKey(10)==27:
            break
        

run()