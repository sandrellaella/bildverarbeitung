import cv
import freenect
import frame_convert

def get_depth():
    	return frame_convert.pretty_depth_cv(freenect.sync_get_depth()[0])

def get_pixel_3d(image,x,y,depth):
	return 0

def get_north_neighbourhood(image,x,y,depth):
	north = get_pixel(image,x-1,y,depth)

def get_south_neighbourhood(image,x,y,depth):
	south = get_pixel(image,x+1,y,depth)

def get_east_neighbourhood(image,x,y,depth):
	east = get_pixel(image,x,y-1,depth)

def get_west_neighbourhood(image,x,y,depth):
	west = get_pixel(image,x,y+1,depth)

def get_depth_before(image,x,y,depth):
	before = get_pixel(image,x,y,depth+1)

def get_depth_behind(image,x,y,depth):
	behind = get_pixel(image,x,y,depth+1)	
	
