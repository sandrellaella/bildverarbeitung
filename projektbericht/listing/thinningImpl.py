int C  = (!p2 & (p3 | p4)) + (!p4 & (p5 | p6)) + (!p6 & (p7 | p8)) + (!p8 & (p9 | p2));
int N1 = (p9 | p2) + (p3 | p4) + (p5 | p6) + (p7 | p8);
int N2 = (p2 | p3) + (p4 | p5) + (p6 | p7) + (p8 | p9);
int N  = N1 < N2 ? N1 : N2;
int m  = iter == 0 ? ((p6 | p7 | !p9) & p8) : ((p2 | p3 | !p5) & p4);

if (C == 1 && (N >= 2 && N <= 3) & m == 0)
    marker.at<uchar>(i,j) = 1;
