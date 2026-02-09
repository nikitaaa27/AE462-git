// Gmsh project created on Sat Jan 24 18:29:27 2026
//+
Point(1) = {-0.06, 0, 0, 1.0};
//+
Point(2) = {-0.06, 0.03, 0, 1.0};
//+
Point(3) = {0, 0.03, 0, 1.0};
//+
Point(4) = {0.5, 0.03, 0, 1.0};
//+
Point(5) = {0.5, 0, 0, 1.0};
//+
Point(6) = {0, 0, 0, 1.0};
//+
//+
Line(1) = {1, 2};
//+
Line(2) = {5, 4};//+
Line(3) = {6, 3};
//+
Line(4) = {3, 2};
//+
Line(5) = {6, 1};
//+
Line(6) = {3, 4};
//+
Line(7) = {6, 5};
//+
Curve Loop(1) = {1, -4, -3, 5};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {6, -2, -7, 3};
//+
Plane Surface(2) = {2};
//+
Physical Curve("inlet", 8) = {1};
//+
Physical Curve("symmetry", 9) = {5};
//+
Physical Curve("wall", 10) = {7};
//+
Physical Curve("outlet", 11) = {4, 6, 2};
//+
Transfinite Surface {1} = {1, 2, 3, 6};
//+
Transfinite Surface {2} = {6, 3, 4, 5};
//+
Transfinite Curve {1, 3, 2} = 60 Using Progression 1.2;
//+
Transfinite Curve {5, 4} = 20 Using Progression 1.1;
//+
Transfinite Curve {6, 7} = 60 Using Progression 1.05;
//+
Recombine Surface {1};
//+
Recombine Surface {2};
