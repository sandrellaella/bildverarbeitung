# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 10:23:38 2013

@author: 8schroed
"""

import cv
import freenect
import frame_convert
import numpy

def body_detection(frame):

    #haar_cascade = cv.Load("classifier/haarcascade_lowerbody.xml")
    haar_cascade = cv.Load("classifier/haarcascade_mcs_upperbody.xml")
    mem_storage = cv.CreateMemStorage(0)
    
    detected = cv.HaarDetectObjects(frame,haar_cascade,mem_storage,1.2,2,cv.CV_HAAR_DO_CANNY_PRUNING, (100,100))
    
    
    if detected: 
        #for body in detected:
         #  print body
        for (x,y,w,h),n in detected:
            cv.Rectangle(frame,(x,y), (x+w,y+h), 255)
    
    return frame

def motion_detection():
    
    #Initialisierungen:
    
    #Das erste Bild des Videos speichern, um Bildeigenschaften zu erhalten
    frame = frame_convert.video_cv(freenect.sync_get_video()[0])
    frame_size = cv.GetSize(frame)
    
    #Graubild
    grey_image = cv.CreateImage(frame_size,cv.IPL_DEPTH_8U,1)
    
    #Bild fuer den RunningAverage-Algorithmus (aus Opencv): Braucht 32 oder 64 Bit - Bild
    running_average_image = cv.CreateImage((frame_size), cv.IPL_DEPTH_32F, 3)
    #Fuer die Konvertierung
    running_average_image_converted = cv.CloneImage(frame)
    #Konstante Alpha fuer RunningAvg
    #Kleines Alpha: Schnelle Bewegung werden kaum wahrgenommen
    #Grosses Alpha: Schnelle Bewegung werden wahrgenommen
    alpha = 0.320
    
    #Fuer Clone-Image
    mem_storage = cv.CreateMemStorage(0)
    
    #Differenzbild fuer AbsDiff
    difference = cv.CloneImage(frame)

    
    while True:
        
        video = frame_convert.video_cv(freenect.sync_get_video()[0])
        
        #Kopie von video
        color_image = cv.CloneImage(video)
        #Glaetten
        cv.Smooth(color_image,color_image,cv.CV_GAUSSIAN,19,0)
        
        #RunningAverage-Algorithmus
        cv.RunningAvg(color_image,running_average_image,alpha,None)
        #Ergebnis ist ein weisses Bild. Deshalb konvertieren
        cv.ConvertScale(running_average_image,running_average_image_converted,1.0,0.0)
        
        #Aktuelles Bild von vom RunningAverage abziehen
        cv.AbsDiff(color_image,running_average_image_converted,difference)
        
        #In Graubild konvertieren
        cv.CvtColor(difference,grey_image,cv.CV_RGB2GRAY)
        
        #Schwellwertbild, um Schwarz-Weiß Bild zu bekommen
        cv.Threshold(grey_image,grey_image,2,255,cv.CV_THRESH_BINARY)
        #Weiterverarbeitung
        cv.Smooth(grey_image,grey_image,cv.CV_GAUSSIAN,19,0)
        cv.Threshold(grey_image,grey_image,240,255,cv.CV_THRESH_BINARY)
        
        #Speichern der Koordinaten der Nicht-Schwarzen-Pixel (weiße Pixel). Weiße Pixel sind Indikator fuer Bewegung 
        #grey_image_mat = numpy.asarray(cv.GetMat(grey_image))
        #non_black_coords_array = numpy.where(grey_image_mat>3)
        
        bounding_box_list = []
        #Konturen berechnen, um Bewegung zu finden
        contours = cv.FindContours(grey_image,mem_storage,cv.CV_RETR_CCOMP,cv.CV_CHAIN_APPROX_SIMPLE)
        liste = list(contours)
        print "Liste: ", liste
        while contours:        
            if liste:
                cv.DrawContours(color_image,contours,(255,0,0),(255,0,0),0,thickness=-1)
                bounding_rect = cv.BoundingRect(liste)
                #print bounding_rect
                bounding_box_list.append(bounding_rect)                
                contours = contours.h_next() 
                
        print "Bounding Box List: ", bounding_box_list
        #cv.DrawContours(color_image,contours,(255,0,0),(255,0,0),0,thickness=-1)    

         
        print "Beginn"    
        for box in bounding_box_list:
            #print len(bounding_box_list)
            (x,y,w,h) = box
            print "Box: ", box
            cv.Rectangle(color_image,(x,y),(x+w,y+h),(0,0,255))
        print "Ende"
            
        #Ausgabe der Videos zur Ueberpruefung
        #cv.ShowImage('Video',video)
        cv.ShowImage('Color Image',color_image)
        #cv.ShowImage('Running Average', running_average_image_converted)
        cv.ShowImage('Differenz', grey_image)
        if cv.WaitKey(10)==27:
            break
        
        
motion_detection()

#while True:
 #   frame = frame_convert.video_cv(freenect.sync_get_video()[0])
  #  frame_detect = body_detection(frame)
   # cv.ShowImage('Body', frame_detect)
    
    #if cv.WaitKey(10)==27:
     #       break

