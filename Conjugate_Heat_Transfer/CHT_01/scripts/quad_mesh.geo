// Ricardo Costa, July, 2022
// parameters
N=1.0;
cx=0.0;
cy=0.0;
rA=1.0;
rAB=0.75;
rB=0.5;
lc1=0.05/N;
lc2=0.15/N;
// points
Point(1)={cx-rA,cy,0.0};
Point(2)={cx,cy+rA,0.0};
Point(3)={cx+rA,cy,0.0};
Point(4)={cx,cy-rA,0.0};
Point(5)={cx,cy,0.0};
Point(6)={cx-rAB,cy,0.0};
Point(7)={cx,cy+rAB,0.0};
Point(8)={cx+rAB,cy,0.0};
Point(9)={cx,cy-rAB,0.0};
Point(10)={cx,cy,0.0};
Point(11)={cx-rB,cy,0.0};
Point(12)={cx,cy+rB,0.0};
Point(13)={cx+rB,cy,0.0};
Point(14)={cx,cy-rB,0.0};
Point(15)={cx,cy,0.0};
// lines
Circle(1)={1,5,2};
Circle(2)={2,5,3};
Circle(3)={3,5,4};
Circle(4)={4,5,1};
Circle(5)={6,10,7};
Circle(6)={7,10,8};
Circle(7)={8,10,9};
Circle(8)={9,10,6};
Circle(9)={11,15,12};
Circle(10)={12,15,13};
Circle(11)={13,15,14};
Circle(12)={14,15,11};
Line(13)={1,6};
Line(14)={2,7};
Line(15)={3,8};
Line(16)={4,9};
Line(17)={6,11};
Line(18)={7,12};
Line(19)={8,13};
Line(20)={9,14};
// line loops
Line Loop(1)={1,14,-5,-13};
Line Loop(2)={2,15,-6,-14};
Line Loop(3)={3,16,-7,-15};
Line Loop(4)={4,13,-8,-16};
Line Loop(5)={5,18,-9,-17};
Line Loop(6)={6,19,-10,-18};
Line Loop(7)={7,20,-11,-19};
Line Loop(8)={8,17,-12,-20};
// surfaces
Plane Surface(1)={1};
Plane Surface(2)={2};
Plane Surface(3)={3};
Plane Surface(4)={4};
Plane Surface(5)={5};
Plane Surface(6)={6};
Plane Surface(7)={7};
Plane Surface(8)={8};
// structured mesh
Transfinite Line{1:12}=Round(1.0/lc1);
Transfinite Line{13:20}=Round(1.0/lc2);
Transfinite Surface{1}={1,2,6,7};
Transfinite Surface{2}={2,3,7,8};
Transfinite Surface{3}={3,4,8,9};
Transfinite Surface{4}={1,4,6,9};
Transfinite Surface{5}={6,7,11,12};
Transfinite Surface{6}={7,8,12,13};
Transfinite Surface{7}={8,9,13,14};
Transfinite Surface{8}={6,9,11,14};
Recombine Surface{1:8};
Mesh.Smoothing=0;
// physicals
Physical Point(1)={1:5};
Physical Point(2)={6:10};
Physical Point(3)={11:15};
Physical Line(1)={1:4};
Physical Line(2)={5:8};
Physical Line(3)={9:12};
Physical Line(100)={13:16};
Physical Surface(100)={1:4};
Physical Line(200)={17:20};
Physical Surface(200)={5:8};
// mesh options
Mesh.Algorithm=5;
Mesh.Algorithm3D=1;
Mesh.OptimizeNetgen=1;
Mesh.Format=1;
Mesh.MshFileVersion=2.0;
// end of file
