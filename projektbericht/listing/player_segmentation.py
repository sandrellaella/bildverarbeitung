#Segmentierung des Tiefenbildes
depth = 255 * np.logical_and
			(depth >= current_depth - threshold,
			 depth <= current_depth + threshold)
