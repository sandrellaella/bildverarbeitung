import player_segmentation
#import freenect
import cv
import skeletonization
#import image_conversion
#import numpy
import depth
#import frame_convert
#from math import sin, cos, sqrt, pi

def run():
    threshold_value = 40 
    depth_value = 170
    skeleton = skeletonization.Skeleton()
    while True:          
        #image = frame_convert.video_cv(freenect.sync_get_video()[0])
        #Tiefenbild: geglaettet und fehlende Tiefeninformationen "kuenstlich" ersetzt. 
        depth_image2 = depth.get_better_depth()
        #Spielersegmentierung 
        depth_seg,depth_image = player_segmentation.player_segmentation(depth_image2,threshold_value,depth_value)        
        cv.Smooth(depth_seg, depth_seg, smoothtype=cv.CV_MEDIAN, param1=5, param2=5)
        #Distance Map berechnen und das Skelett daraus extrahieren
        diff_img = skeleton.distance_skeleton(depth_seg)
        
        
        cv.ShowImage('Spieler', depth_seg)
        cv.ShowImage('diff', diff_img)
        cv.ShowImage('Better Depth', depth_image2)  
        #cv.ShowImage("dst", dst)
        #cv.ShowImage("color_dst",color_dst)
         
        if cv.WaitKey(10)==27:
            break

run()