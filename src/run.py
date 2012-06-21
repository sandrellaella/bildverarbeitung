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
        depth, timestamp = freenect.sync_get_depth()
        depth_seg = player_segmentation.player_segmentation(depth,timestamp,threshold_value,depth_value)
        
        dist_img = skeleton.distance_skeleton(depth_seg)
        
        dst = cv.CreateImage(cv.GetSize(dist_img),8,1)

        cv.AdaptiveThreshold(dist_img, dst, 1)
        #dist_img_mat = image_conversion.cv2array(dist_img)   
        
        #rows = len(dist_img_mat[:,1])
        #coloumns = len(dist_img_mat[1,:])
        
        #for i in range(rows):
         #   for j in range(coloumns):
          #      if dist_img_mat[i,j] < 0.9:
           #         dist_img_mat[i,j] = 0
        
        #dist_img = image_conversion.array2cv(dist_img_mat)

        cv.ShowImage('Spieler',depth_seg)  
        cv.ShowImage('Distance Image',dist_img)
        
        if cv.WaitKey(10)==27:
            break
        

run()