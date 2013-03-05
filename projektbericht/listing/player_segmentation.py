#Die Segmentierung des Spielers
def player_segmentation(depth_image_input,
				threshold_value,depth_value):
    
   #Umwandlung des OpenCV-Bildes in ein Numpy-Array
   depth = image_conversion.cv2array(depth_image_input)
   #Tiefenschwellwert
   threshold = threshold_value
   #Wert, um ein Intervall nach "hinten" und nach "vorne" zu definieren.
   current_depth = depth_value
   #Segmentierung des Tiefenbildes
   depth = 255 * np.logical_and
			(depth >= current_depth - threshold,
			 depth <= current_depth + threshold)
