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
    //printf("C++ %d\n",im.rows);
    //printf("C++ %d\n",im.cols);
    //cv::Mat marker = cv::Mat::zeros(im.size(), CV_32FC1); 
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
    //printf("C++ In thinningGuoHallIteration %d\n",iter);
    im &= ~marker;
    //printf("C++ Ende thinningGuoHallIteration %d\n",iter);
}

/**
 * Function for thinning the given binary image
 *
 * @param  im  Binary image with range = 0-255
 */
void thinningGuoHall(cv::Mat& im)
{
    im /= 255;
    //cv::Mat prev = cv::Mat::zeros(im.size(), CV_32FC1);
    cv::Mat prev = cv::Mat::zeros(im.size(), CV_8UC1);
    cv::Mat diff;
    do {
        thinningGuoHallIteration(im, 0);
        //printf("C++: Nach thinningGuoHallIteration 0\n");
        thinningGuoHallIteration(im, 1);
        //printf("C++: Nach thinningGuoHallIteration 1\n");
        //printf("%d\n", im.type());
        //printf("%d\n", prev.type());
        cv::absdiff(im, prev, diff);
        //printf("C++: Absdiff\n");
        im.copyTo(prev);
    } 
    while (cv::countNonZero(diff) > 0);
    //printf("C++: Nach dem Thinning\n");
    im *= 255;
    //printf("C++: Ende thinningGuoHall\n");
}

/**
 * This is an example on how to call the thinning function above.
 */
LIBEXPORT int vigra_reflectimage_c( int *arr,  int *arr2, const  int width, const  int height, const int reflect_method){ 

    //TRY: Height und Width vertauscht
    //cv::Mat source(height,width,CV_32FC1,arr);
    cv::Mat source(height,width,CV_8UC1,arr);
    if (source.empty())
        return -1;
    
    //printf("Width: %d\n",width);
    //printf("Height: %d\n",height);
    
    //cv::Mat bw = cv::Mat::zeros(source.size(), CV_32FC1);
    cv::Mat bw = cv::Mat::zeros(source.size(), CV_8UC1);
    //printf("%d\n",bw.type());
    //printf("%d\n",source.type());
    
    cv::threshold(source, bw, 10, 255, CV_THRESH_BINARY);
    //printf("%d\n",bw.type());
    thinningGuoHall(source);
    //printf("C++: Aus thinningGuoHall raus\n");
    cv::imshow("Thinning", source);
    //cv::imshow("dst", bw);
    
    //cv::waitKey();
    return 0;
}

int main()
{
    cv::Mat src = cv::imread("hand.jpg");
    
    if (src.empty())
        return -1;
    
    cv::Mat bw;
    cv::cvtColor(src, bw, CV_BGR2GRAY);
    cv::threshold(bw, bw, 10, 255, CV_THRESH_BINARY);
    
    thinningGuoHall(bw);
    
    cv::imshow("src", src);
    cv::imshow("dst", bw);
    cv::waitKey(0);
    
    return 0;
}