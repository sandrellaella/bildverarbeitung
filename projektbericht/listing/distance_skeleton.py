def distance_skeleton(self,img):
        #Ein Zielbild bereitstellen, um das Ergebnis der Distance Transformation zu speichern        
        dist_img = cv.CreateImage(cv.GetSize(img),32,1)

        #distance transform
        cv.DistTransform(img, dist_img, distance_type=cv.CV_DIST_L2)
        #conversion to numpy-array
        dist_img_mat = image_conversion.cv2array(dist_img)
        #normalise the distance image
        max_of_dist = dist_img_mat.max()
        dist_img_mat = dist_img_mat/max_of_dist
        #conversion back to cv-image
        dist_img = image_conversion.array2cv(dist_img_mat)
        #Erste Stufe fuer das Pruning: Gradientbild berechnen
        #dist_gradient, gradient = self.pruning(dist_img,1)
        dist_gradient = self.pruning(dist_img,1)
        dist_gradient_mat = image_conversion.cv2array(dist_gradient)
        dist_img_mat = image_conversion.cv2array(dist_img)
        #Zweite Stufe fuer das Pruning: Differenzbild aus Distanzbild und segmentiertem Gradientenbild
        diff = dist_img_mat - dist_gradient_mat
        diff = diff * 1.0
        diff_img = image_conversion.array2cv(diff)
        
        #return diff_img, gradient       
        return diff_img, dist_img
