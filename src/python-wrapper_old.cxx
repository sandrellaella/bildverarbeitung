#include <vigra/basicimageview.hxx>
#include <cstdlib>
#include <stdlib.h>


#ifdef _WIN32
#define LIBEXPORT extern "C" __declspec(dllexport) 
#else
#define LIBEXPORT  extern "C" 
#endif






//erste Bedingung    2<=P1<=6
/*int checkNeighbours(int x, int y, float* img) {
 //auf -1 gesetzt da P1 ja bereits eins ist und mitgez채hlt wird
 int numberActiveNeighb=-1;    
 int a=y;
 int b=x;
 for (a-1; a<=a+1; a++) {
 for(b-1;b<=b+1;b++){
 if(img(b,a)==255){
 
 numberActiveNeighb+=1;
 }
 }
 } 
 if(!(numberActiveNeighb>=2&&numberActiveNeighb<=6)){
 return 0;
 } 
 
 else {
 return 1;
 }
 }
 
 
 
 
 //2te Bedingung Anzahl der 01 Dolgen in geordneter Folge =1
 
 int checkSequence() {
 int secondArgument=0;
 for (int i=0; i<=7; i++) {
 if( neighbourSequ[i]==0 &&neighbourSequ[i+1]==255){
 secondArgument+=1;
 }
 
 }
 if (secondArgument==0||secondArgument>1){
 
 return 0;
 }
 else{return 1;}
 }
 */


LIBEXPORT int vigra_reflectimage_c(const float *arr, const float *arr2, const  int width, const  int height, const int reflect_method){ 
    
    
    // create a gray scale image of appropriate size
    vigra::BasicImageView<float> img(arr, width, height);
    vigra::BasicImageView<float> img2(arr, width, height);
    
    
    
    int returnValue;
    
    float temp;
    
    int counter=1;
    
    
    for(int y=0; y < height; y++)
    {
        for(int x=0; x < width; x++)
        {
            
            if(img(x,y)>128){
                
                img(x,y)=255;
                
            }
            
            else{
                img(x,y)=0;
            }
        }
    }
    
    
    
    img2=img;
    int check=0;
    while (counter!=0){ 
        counter=0;
        img=img2;
        
        //---------------------------erste Subiteration----------------------------------------
        for(int y=1; y < height-1; ++y)
        {
            for(int x=1; x < width-1; ++x)
            {
                
                float  neighbourSequ[8];
                neighbourSequ[0]=img (x,y-1);
                neighbourSequ[1]=img (x+1,y-1);
                neighbourSequ[2]=img (x+1,y);
                neighbourSequ[3]=img (x+1,y+1);
                neighbourSequ[4]=img (x,y+1);
                neighbourSequ[5]=img (x-1,y+1);
                neighbourSequ[6]=img (x-1,y);
                neighbourSequ[7]=img (x-1,y-1);
                
                
                
                if(img(x,y)==255){
                    
                    //erste Bedingung    2<=P1<=6-------------------------------------
                    
                    int numberActiveNeighb=0;    
                    for (int j=0; j<8; j++) {
                        
                        if(neighbourSequ[j]==255){
                            
                            numberActiveNeighb+=1;
                        }
                        
                    } 
                    if(numberActiveNeighb>=2&&numberActiveNeighb<=6){
                        //2te Bedingung-----------------------------------------------------
                        int secondArgument=0;
                        for (int i=0; i<7; i++) {
                            if( neighbourSequ[i]==0 &&neighbourSequ[i+1]==255){
                                secondArgument=secondArgument+1;
                            }
                            
                        }
                        
                        if (secondArgument==1){
                            
                            
                            
                            
                            
                            //3te Bedingung P2*P4*P6=0---------------------------------------
                            if((neighbourSequ[0]*neighbourSequ[2]*neighbourSequ[4])==0){
                                
                                //4te Bedingung----------------------------------------
                                if((neighbourSequ[2]*neighbourSequ[4]*neighbourSequ[6])==0){
                                    
                                    
                                    counter=counter+1;
                                    img2(x,y)= 0;
                                    
                                }
                                
                                
                            }
                            
                            
                        } 
                        
                    } 
                    
                } 
                
                
                
            }
        }
        
        if (counter==0) {
            
            
            break;
        }
        
        
        img=img2;
        counter=0;
        
        
        
        
        
        
        
        //---------------------------zweite Subiteration----------------------------------------
        
        for(int y=1; y < height-1; ++y)
        {
            for(int x=1; x < width-1; ++x)
            {
                
                float  neighbourSequ[8];
                neighbourSequ[0]=img (x,y-1);
                neighbourSequ[1]=img (x+1,y-1);
                neighbourSequ[2]=img (x+1,y);
                neighbourSequ[3]=img (x+1,y+1);
                neighbourSequ[4]=img (x,y+1);
                neighbourSequ[5]=img (x-1,y+1);
                neighbourSequ[6]=img (x-1,y);
                neighbourSequ[7]=img (x-1,y-1);
                
                
                
                if(img(x,y)==255){
                    
                    //erste Bedingung    2<=P1<=6-------------------------------------
                    
                    int numberActiveNeighb=0;    
                    for (int j=0; j<8; j++) {
                        
                        if(neighbourSequ[j]==255){
                            
                            numberActiveNeighb+=1;
                        }
                        
                    } 
                    if(numberActiveNeighb>=2&&numberActiveNeighb<=6){
                        //2te Bedingung-----------------------------------------------------
                        int secondArgument=0;
                        for (int i=0; i<7; i++) {
                            if( neighbourSequ[i]==0 &&neighbourSequ[i+1]==255){
                                secondArgument=secondArgument+1;
                            }
                            
                        }
                        
                        if (secondArgument==1){
                            
                            
                            
                            //3te Bedingung P2*P4*P8=0---------------------------------------
                            if((neighbourSequ[0]*neighbourSequ[2]*neighbourSequ[6])==0){
                                //4te Bedingung----------------------------------------
                                if((neighbourSequ[0]*neighbourSequ[4]*neighbourSequ[6])==0){
                                    
                                    counter=counter+1;
                                    img2(x,y)= 0;
                                    
                                }
                                
                                
                            }
                            
                            
                        }
                        
                    } 
                    
                    
                    
                    
                    
                }
                
                
                returnValue = x; 
            }  
        }
        
        
    }
    
    
    
    
    return width;
}


