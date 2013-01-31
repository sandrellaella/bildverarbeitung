import player_segmentation
import cv
import skeletonization
import image_conversion
import numpy
import depth
import comparison
import pythonWrapper

def run():
    threshold_value = 40 
    depth_value = 170
    skeleton = skeletonization.Skeleton()
    i=0
    while True:          
        i=i+1
        #image = frame_convert.video_cv(freenect.sync_get_video()[0])
        #Tiefenbild: geglaettet und fehlende Tiefeninformationen "kuenstlich" ersetzt. 
        depth_image2 = depth.get_better_depth()
        #Spielersegmentierung 
        depth_seg,depth_image = player_segmentation.player_segmentation(depth_image2,threshold_value,depth_value)        
        cv.Smooth(depth_seg, depth_seg, smoothtype=cv.CV_MEDIAN, param1=5, param2=5)
        #Distance Map berechnen und das Skelett daraus extrahieren
        diff_img,dist_gradient = skeleton.distance_skeleton(depth_seg)
        diff = image_conversion.cv2array(diff_img)
        diff = 255.0 * numpy.logical_and(diff >= 0.2, diff<=1)
        diff = diff.astype(numpy.uint8)
        diff_img = image_conversion.array2cv(diff)

        #Thinning
        
#        if(i%5==0):
        greyscale_array = image_conversion.cv2array(depth_seg)
        new_g = greyscale_array.reshape((480,640))
        new_g = pythonWrapper.reflectimage_band(new_g,1)              
        
        
        #diff_img = player_segmentation.erode_image(diff_img,1)    
        
        #features = comparison.calcGoodFeatures(diff_img) 
        #comparison.drawFeatures(features,diff_img)
        
        cv.ShowImage('Spieler', depth_seg)
        cv.ShowImage('Distance Map', diff_img)
        
        #cv.ShowImage('Better Depth', depth_image2)  
        #cv.ShowImage('Dist Gradient', dist_gradient)
         
        if cv.WaitKey(10)==27:
            break

run()