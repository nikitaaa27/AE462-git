// Gmsh project created on Sun Feb 22 18:27:05 2026

lc = 0.05; 

// Import CD Nozzle Points 
Include "CDPoints.geo";//+
Point(133) = {-3, 0, 0, lc};
//+
Point(134) = {10, 0, 0, lc};
//+
Line(1) = {133, 1};
//+
Line(2) = {134, 132};
//+
Line(3) = {133, 134};

//
Spline(4) = {1:132};//+
Curve Loop(1) = {1, 4, -2, -3};
//+
Plane Surface(1) = {1};
//+
Physical Curve("inlet", 5) = {1};
//+
Physical Curve("symmetry", 6) = {3};
//+
Physical Curve("outlet", 7) = {2};
//+
Physical Curve("wall", 8) = {4};
//+

