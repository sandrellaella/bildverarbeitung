#Gradienten-Berechnung
ndimage.gaussian_gradient_magnitude(distancemap,
			sigma,gradient_image)
#Vor -und Nachbearbeitungen
#Segmentierung
cv.InRangeS(gradient_image,lowerbound,upperbound,
			threshed_gradient_image)
