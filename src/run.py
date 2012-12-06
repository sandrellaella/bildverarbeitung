import player_segmentation
import freenect
import cv
import skeletonization
import image_conversion
import numpy
import depth
def run():
    threshold_value = 40 
    depth_value = 170
    skeleton = skeletonization.Skeleton()
    while True:          
        image=freenect.get_video()
        #Kinect starten (Tiefenbild)
        #depth, timestamp = freenect.sync_get_depth()
        depth_image2 = depth.get_better_depth()
        
        #spielersegmentierung 
        depth_seg,depth_image = player_segmentation.player_segmentation(depth_image2,threshold_value,depth_value)        
        #distance map berechnen und das Skelett daraus extrahieren
        diff_img = skeleton.distance_skeleton(depth_seg)
        
        feature = skeleton.goodFeatures(diff_img)
        
        for point in feature:
            center = int(point[0]), int(point[1])
            #cv.Circle(colorImage, (center), 2, (0,255,255))
        
        cv.ShowImage('Spieler', depth_seg)
        cv.ShowImage('diff', diff_img)
        cv.ShowImage('Better Depth', depth_image2)
        cv.ShowImage('Good Features', image)
         
                
        if cv.WaitKey(10)==27:
            break
        

run()