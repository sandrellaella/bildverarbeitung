import numpy as N
import image_conversion
import cv

lib = N.ctypeslib.load_library('libpython-wrapper','.')


###############################################################################
###################         Reflect image                  ####################

lib.vigra_reflectimage_c.restype=int 
#lib.vigra_reflectimage_c.argtypes = [ N.ctypeslib.ndpointer(N.float32, ndim=2, flags='aligned,contiguous, writeable'), N.ctypeslib.ndpointer(N.float32, ndim=2, flags='aligned, contiguous, writeable'), N.ctypeslib.ctypes.c_int, N.ctypeslib.ctypes.c_int, N.ctypeslib.ctypes.c_int] 
lib.vigra_reflectimage_c.argtypes = [ N.ctypeslib.ndpointer(N.uint8, ndim=2, flags='aligned,contiguous, writeable'), N.ctypeslib.ndpointer(N.uint8, ndim=2, flags='aligned, contiguous, writeable'), N.ctypeslib.ctypes.c_int, N.ctypeslib.ctypes.c_int, N.ctypeslib.ctypes.c_int, N.ctypeslib.ctypes.c_int] 
#lib.static_function.argtypes = [ N.ctypeslib.ndpointer(N.uint8, ndim=2, flags='aligned,contiguous, writeable'), N.ctypeslib.ndpointer(N.uint8, ndim=2, flags='aligned, contiguous, writeable'), N.ctypeslib.ctypes.c_int, N.ctypeslib.ctypes.c_int, N.ctypeslib.ctypes.c_int] 
def reflectimage_band(arr, reflect_mode,count): 
    #arr  = N.require(arr, N.float32, ['ALIGNED']) 
    arr = N.require(arr, N.uint8, ['ALIGNED']) 
    #arr2  = N.require(arr, N.float32, ['ALIGNED']) 
    arr2 = N.require(arr,N.uint8,['ALIGNED'])    
    #arr2 = N.zeros_like(arr) 
    #print "Python: ", arr.dtype
    lib.vigra_reflectimage_c(arr, arr2, arr.shape[1], arr.shape[0], reflect_mode,count) 
    #print(lib.vigra_reflectimage_c(arr, arr2, arr.shape[0], arr.shape[1], reflect_mode) )

    #if res==1:
    #    raise Exception("Error in vigrapy.imgproc:reflectimage: Reflection of image failed!!")
    #elif res==2:
    #   raise Exception("Error in vigrapy.imgproc:reflectimage: Reflection mode must be in {1 (= horizontal), 2 (= vertical)}!")
   
    return arr2
    
def reflectimage(arr,reflect_mode): 
    arr2 = N.zeros_like(arr) 
    for dim in range(arr.ctypes.shape[0]):
        arr2[dim,:,:] = reflectimage_band(arr[dim,:,:], reflect_mode)
    return arr2
    
def static():
    #Invertierung der Farbe, damit Objekt weiss und Hintergrund schwarz
    img = cv.LoadImage("hand.jpg")
    grey_img = cv.CreateImage(cv.GetSize(img),8,1)
    grey_img_mat = image_conversion.cv2array(grey_img)

    for i in xrange(len(grey_img_mat[:,1])):
        for j in xrange(len(grey_img_mat[1,:])):
            if grey_img_mat[i,j] == 255:
                grey_img_mat[i,j] = 0
            else:
                grey_img_mat[i,j] = 1   
                
    print(lib.static_function(grey_img_mat,grey_img_mat.shape[1],grey_img_mat.shape[0]))
