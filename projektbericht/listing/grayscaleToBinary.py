for(int y=0; y < height; y++)  {
  for(int x=0; x < width; x++) {
    if(img(x,y)>128){
      img(x,y)=255;
    } else{
      img(x,y)=0;
    }
  }
}
