def distance_skeleton(self,img):
        #Ein Zielbild bereitstellen, um das Ergebnis der Distanztransformation zu speichern        
        dist_img = cv.CreateImage(cv.GetSize(img),32,1)

        #Distanztransformation
        cv.DistTransform(img, dist_img, distance_type=cv.CV_DIST_L2)
        #Konvertierung
        dist_img_mat = image_conversion.cv2array(dist_img)
        #Normalisierung der Distance Map
        max_of_dist = dist_img_mat.max()
        dist_img_mat = dist_img_mat/max_of_dist
        #Konvertierung
        dist_img = image_conversion.array2cv(dist_img_mat)
        #Berechnung Gradientenbild
        dist_gradient = self.pruning(dist_img,1)
        dist_gradient_mat = image_conversion.cv2array(dist_gradient)
        dist_img_mat = image_conversion.cv2array(dist_img)
        #Berechnung Differenzbild
        diff = dist_img_mat - dist_gradient_mat
        diff = diff * 1.0
	#Konvertierung
        diff_img = image_conversion.array2cv(diff)
        
        return diff_img, dist_img
