R = 1;
ff = 100;

Point(1) = {0, 0, 0, 1.0};
Point(2) = {R, 0, 0, 1.0};
Point(3) = {-R, 0, 0, 1.0};
Point(4) = {ff, 0, 0, 1.0};
Point(5) = {-ff, 0, 0, 1.0};
Circle(1) = {3, 1, 2};
Circle(2) = {2, 1, 3};
Circle(3) = {5, 1, 4};
Circle(4) = {4, 1, 5};
Physical Curve("cylinder", 5) = {2, 1};
Physical Curve("farfield", 6) = {4, 3};
Line(5) = {3, 5};
Line(6) = {2, 4};
//+
Curve Loop(1) = {2, 5, -4, -6};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {1, 6, -3, -5};
//+
Plane Surface(2) = {2};
//+
Transfinite Curve {2, 1, 4, 3} = 200;
//+
Transfinite Curve {6, 5} = 360 Using Progression 1.03;
//+
Recombine Surface {2, 1};

//+
Transfinite Surface {1};
//+
Transfinite Surface {2};
