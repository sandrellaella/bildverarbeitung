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
        depth, timestamp = freenect.sync_get_depth()
        depth_seg = player_segmentation.player_segmentation(depth,timestamp,threshold_value,depth_value)
        dist_img = skeleton.distance_skeleton(depth_seg)

        cv.ShowImage('Spieler',depth_seg)  
        cv.ShowImage('Distance Image',dist_img)
        
        if cv.WaitKey(10)==27:
            break
        

run()