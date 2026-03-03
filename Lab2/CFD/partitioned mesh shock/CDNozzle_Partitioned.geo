// Gmsh project created on Sun Feb 22 18:27:05 2026

lc = 0.05; 

// Import CD Nozzle Points 
Include "CDPoints.geo";//+
Point(133) = {-3, 0, 0, lc};
//+
Point(134) = {2.3, 0, 0, lc};
//+
// Point(135) = {2.6, 0, 0, lc};
//+
Point(136) = {3.3, 0, 0, lc};
//+
Point(137) = {10, 0, 0, lc};

//+
Line(1) = {133, 1};
//+
Line(2) = {134, 55};
//+
Line(3) = {65, 136};
//+
Line(4) = {137, 132};
//+
Line(6) = {134, 133};
//+
Line(7) = {136, 134};
//+
Line(8) = {136, 137};
//+
Spline(9) = {1:55};
//+
Spline(10) = {55:65};
//+
Spline(11) = {65:132};//+
Curve Loop(1) = {6, 1, 9, -2};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {2, 10, 3, 7};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {-3, 11, -4, -8};
//+
Plane Surface(3) = {3};
//+
Transfinite Surface {2};
//+
Transfinite Curve {7, 10} = 60 Using Bump 12;
//+
Transfinite Curve {3, 2} = 200 Using Progression 1;
//+
Recombine Surface {2};
//+
Physical Curve("wall", 12) = {9, 10, 11};
//+
Physical Curve("inlet", 13) = {1};
//+
Physical Curve("outlet", 14) = {4};
//+
Physical Curve("symmetry", 15) = {6, 7, 8};
