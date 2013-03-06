import player_segmentation
import cv
import skeletonization
import image_conversion
import numpy
import depth
import pythonWrapper
import timeit
import cProfile

def run():
    threshold_value = 40 
    depth_value = 170
    skeleton = skeletonization.Skeleton()
    count = 0    
    while True:   
        
        #image = frame_convert.video_cv(freenect.sync_get_video()[0])
        #Tiefenbild: geglaettet und fehlende Tiefeninformationen "kuenstlich" ersetzt. 
        depth_image2 = depth.get_better_depth()
        #Spielersegmentierung 
        depth_image = player_segmentation.player_segmentation(depth_image2,threshold_value,depth_value)  
        
        cv.Smooth(depth_image, depth_image, smoothtype=cv.CV_MEDIAN, param1=5, param2=5)
        #Distance Map berechnen und das Skelett daraus extrahieren
        diff_img,dist_gradient = skeleton.distance_skeleton(depth_image)

        diff = image_conversion.cv2array(diff_img)
        diff = 255.0 * numpy.logical_and(diff >= 0.2, diff<=1)
        diff = diff.astype(numpy.uint8)
        diff_img = image_conversion.array2cv(diff)

        #Thinning
        greyscale_array = image_conversion.cv2array(depth_image)
        new_g = greyscale_array.reshape((480,640))
        new_g = pythonWrapper.reflectimage_band(new_g,1,count)              
        
        
        #diff_img = player_segmentation.erode_image(diff_img,1)    
        
        #features = comparison.calcGoodFeatures(diff_img) 
        #comparison.drawFeatures(features,diff_img)
        
        cv.ShowImage('Spieler', depth_image)
        cv.ShowImage('Distance Map', diff_img)
        #cv.ShowImage('Gradient', dist_gradient)
        
        cv.SaveImage('Screenshots/Distance_und_Thinning/Screenshot_Distance_Map'+ str(count) + '.png',diff_img)
        cv.SaveImage('Screenshots/Distance_und_Thinning/Screenshot_Spieler'+ str(count) + '.png',depth_image)
        #cv.SaveImage('Screenshots/Screenshot_Gradient'+ str(count) + '.png',dist_gradient)
        #cv.ShowImage('Better Depth', depth_image2)  
        #cv.ShowImage('Dist Gradient', dist_gradient)
        count = count + 1 
        #if cv.WaitKey(10)==27:
         #   break
     
        cv.WaitKey()

run()
#cProfile.run("run()")