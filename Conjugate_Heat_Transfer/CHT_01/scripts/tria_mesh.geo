// Ricardo Costa, July, 2022
// parameters
N=1.0;
cx=0.0;
cy=0.0;
rA=1.0;
rAB=0.75;
rB=0.5;
lc1=0.1*rA/N;
lc2=0.1*rAB/N;
lc3=0.1*rB/N;
// points
Point(1)={cx-rA,cy,0.0,lc1};
Point(2)={cx,cy+rA,0.0,lc1};
Point(3)={cx+rA,cy,0.0,lc1};
Point(4)={cx,cy-rA,0.0,lc1};
Point(5)={cx,cy,0.0,lc1};
Point(6)={cx-rAB,cy,0.0,lc2};
Point(7)={cx,cy+rAB,0.0,lc2};
Point(8)={cx+rAB,cy,0.0,lc2};
Point(9)={cx,cy-rAB,0.0,lc2};
Point(10)={cx,cy,0.0,lc2};
Point(11)={cx-rB,cy,0.0,lc3};
Point(12)={cx,cy+rB,0.0,lc3};
Point(13)={cx+rB,cy,0.0,lc3};
Point(14)={cx,cy-rB,0.0,lc3};
Point(15)={cx,cy,0.0,lc3};
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
// line loops
Line Loop(1)={1:4};
Line Loop(2)={5:8};
Line Loop(3)={9:12};
// surfaces
Plane Surface(1)={1,2};
Plane Surface(2)={2,3};
// physicals
Physical Point(1)={1:5};
Physical Point(2)={6:10};
Physical Point(3)={11:15};
Physical Line(1)={1:4};
Physical Line(2)={5:8};
Physical Line(3)={9:12};
Physical Surface(100)={1:4};
Physical Surface(200)={5:8};
// mesh options
Mesh.Algorithm=5;
Mesh.Algorithm3D=1;
Mesh.OptimizeNetgen=1;
Mesh.Format=1;
Mesh.MshFileVersion=2.0;
// end of file
