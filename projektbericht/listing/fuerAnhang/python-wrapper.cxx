#include <vigra/basicimageview.hxx>
#include <cstdlib>
#include <stdlib.h>


#ifdef _WIN32
#define LIBEXPORT extern "C" __declspec(dllexport) 
#else
#define LIBEXPORT  extern "C" 
#endif



#include </opt/local/include/opencv2/highgui/highgui.hpp>
#include </opt/local/include/opencv2/imgproc/imgproc.hpp>
#include <iostream>

/**
 * Perform one thinning iteration.
 * Normally you wouldn't call this function directly from your code.
 *
 * @param  im    Binary image with range = 0-1
 * @param  iter  0=even, 1=odd
 */
void thinningGuoHallIteration(cv::Mat& im, int iter)
{
    cv::Mat marker = cv::Mat::zeros(im.size(), CV_8UC1); 
    for (int i = 1; i < im.rows; i++)
    {
        for (int j = 1; j < im.cols; j++)
        {
            
            uchar p2 = im.at<uchar>(i-1, j);
            uchar p3 = im.at<uchar>(i-1, j+1);
            uchar p4 = im.at<uchar>(i, j+1);
            uchar p5 = im.at<uchar>(i+1, j+1);
            uchar p6 = im.at<uchar>(i+1, j);
            uchar p7 = im.at<uchar>(i+1, j-1);
            uchar p8 = im.at<uchar>(i, j-1); 
            uchar p9 = im.at<uchar>(i-1, j-1);
            
            int C  = (!p2 & (p3 | p4)) + (!p4 & (p5 | p6)) +
            (!p6 & (p7 | p8)) + (!p8 & (p9 | p2));
            int N1 = (p9 | p2) + (p3 | p4) + (p5 | p6) + (p7 | p8);
            int N2 = (p2 | p3) + (p4 | p5) + (p6 | p7) + (p8 | p9);
            int N  = N1 < N2 ? N1 : N2;
            int m  = iter == 0 ? ((p6 | p7 | !p9) & p8) : ((p2 | p3 | !p5) & p4);
            
            if (C == 1 && (N >= 2 && N <= 3) & m == 0)
                marker.at<uchar>(i,j) = 1;
        }
    }
    im &= ~marker;
}

/**
 * Function for thinning the given binary image
 *
 * @param  im  Binary image with range = 0-255
 */
void thinningGuoHall(cv::Mat& im)
{
    im /= 255;
    cv::Mat prev = cv::Mat::zeros(im.size(), CV_8UC1);
    cv::Mat diff;
    do {
        thinningGuoHallIteration(im, 0);
        thinningGuoHallIteration(im, 1);
        cv::absdiff(im, prev, diff);
        im.copyTo(prev);
    } 
    while (cv::countNonZero(diff) > 0);
    im *= 255;
}

/**
 * This is an example on how to call the thinning function above.
 */
LIBEXPORT int vigra_reflectimage_c( int *arr,  int *arr2, const  int width, const  int height, const int reflect_method){ 

    cv::Mat source(height,width,CV_8UC1,arr);
    if (source.empty())
        return -1;
    
    cv::Mat bw = cv::Mat::zeros(source.size(), CV_8UC1);
    cv::threshold(source, bw, 10, 255, CV_THRESH_BINARY);
    thinningGuoHall(source);
    cv::imshow("Thinning", source);
    return 0;
}