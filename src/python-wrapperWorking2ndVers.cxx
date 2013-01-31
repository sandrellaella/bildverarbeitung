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


void thinningIteration(cv::Mat& im, int iter)
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
            
            int A  = (p2 == 0 && p3 == 1) + (p3 == 0 && p4 == 1) + 
            (p4 == 0 && p5 == 1) + (p5 == 0 && p6 == 1) + 
            (p6 == 0 && p7 == 1) + (p7 == 0 && p8 == 1) +
            (p8 == 0 && p9 == 1) + (p9 == 0 && p2 == 1);
            int B  = p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9;
            int m1 = iter == 0 ? (p2 * p4 * p6) : (p2 * p4 * p8);
            int m2 = iter == 0 ? (p4 * p6 * p8) : (p2 * p6 * p8);
            
            if (A == 1 && (B >= 2 && B <= 6) && m1 == 0 && m2 == 0)
                marker.at<uchar>(i,j) = 1;
        }
    }
    //Ursprünglich ist das AMrker array ein schwarzes bild mti einpixeldicker weisser linie
    //negiert -->weisses bild mit ein pixel dicker schwarzer linie bei verundung wird die ein pixel dicke Linie daher abgetragen 
    //Tilde--> bitweise negation und anschliessend bitweise verundung mit img     
    im &= ~marker;
}

/**
 * Function for thinning the given binary image
 *
 * @param  im  Binary image with range = 0-255
 */
void thinning(cv::Mat& im)
{
     printf("Bin hier\n");
    im /= 255;
    
    cv::Mat prev = cv::Mat::zeros(im.size(), CV_8UC1);
    cv::Mat diff;
    
    do {
        thinningIteration(im, 0);
        thinningIteration(im, 1);
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
    cv::threshold(bw, bw, 10, 255, CV_THRESH_BINARY);
    thinning(source);
   
    //printf("C++: Aus thinningGuoHall raus\n");
    cv::imshow("src", source);
    
    
    //cv::waitKey();
    return 0;
}

/**
 * This is an example on how to call the thinning function above.
 */
int main()
{
    cv::Mat src = cv::imread("hand.jpg");
    if (src.empty())
        return -1;
    
    cv::Mat bw;
    cv::cvtColor(src, bw, CV_BGR2GRAY);
    cv::threshold(bw, bw, 10, 255, CV_THRESH_BINARY);
    
    thinning(bw);
    
    cv::imshow("src", src);
    cv::imshow("dst", bw);
    cv::waitKey(0);
    
    return 0;
}