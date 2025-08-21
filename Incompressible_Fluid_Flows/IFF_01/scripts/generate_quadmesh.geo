// -*- coding: utf-8 -*-
/*
===============================================================================
CFDLab | CHT_01
===============================================================================

Description:
    Generates quadrilateral structured meshes in MSH format.
    Mesh refinement can be controlled through the command-line option `-setnumber N <value>`
    where `<value>` is a numerical argument specifying the desired refinement level
    (default: `1`).
    Outputs are saved in `meshes/`.

Author:
    Ricardo Costa (rcosta@dep.uminho.pt)

License:
    MIT License (see LICENSE file for details)

Repository:
    https://github.com/ricardodpcosta/CFD-TestSuite

Dependencies:
    Gmsh (version >= 4.8.4)

Usage:
    gmsh -setnumber N 1 generate_quadmesh.geo
===============================================================================
*/

// refinement level
If (!Exists(N))
    N = 1;
EndIf

// domain center
cx = 0.0;
cy = 0.0;

// outer boundary
rA = 1.0;

// interface
rAB = 0.75;

// inner boundary
rB = 0.5;

// refinement controls
lc1 = 0.06/(1.38^(N-1));
lc2 = 0.2/(1.38^(N-1));

// output controls
outdir = "../meshes";
name = "quadmesh";

//============================================
// POINTS
//============================================

// outer boundary
Point(1) = {cx-rA, cy, 0.0};
Point(2) = {cx, cy+rA, 0.0};
Point(3) = {cx+rA, cy, 0.0};
Point(4) = {cx, cy-rA, 0.0};
Point(5) = {cx, cy, 0.0};

// interface
Point(6) = {cx-rAB, cy, 0.0};
Point(7) = {cx, cy+rAB, 0.0};
Point(8) = {cx+rAB, cy, 0.0};
Point(9) = {cx, cy-rAB, 0.0};
Point(10) = {cx, cy, 0.0};

// inner boundary
Point(11) = {cx-rB, cy, 0.0};
Point(12) = {cx, cy+rB, 0.0};
Point(13) = {cx+rB, cy, 0.0};
Point(14) = {cx, cy-rB, 0.0};
Point(15) = {cx, cy, 0.0};

//============================================
// LINES
//============================================

// outer boundary
Circle(1) = {1, 5, 2};
Circle(2) = {2, 5, 3};
Circle(3) = {3, 5, 4};
Circle(4) = {4, 5, 1};

// interface
Circle(5) = {6, 10, 7};
Circle(6) = {7, 10, 8};
Circle(7) = {8, 10, 9};
Circle(8) = {9, 10, 6};

// inner boundary
Circle(9) = {11, 15, 12};
Circle(10) = {12, 15, 13};
Circle(11) = {13, 15, 14};
Circle(12) = {14, 15, 11};

// outer subdomain
Line(13) = {1, 6};
Line(14) = {2, 7};
Line(15) = {3, 8};
Line(16) = {4, 9};

// inner subdomain
Line(17) = {6, 11};
Line(18) = {7, 12};
Line(19) = {8, 13};
Line(20) = {9, 14};

//============================================
// LINE LOOPS
//============================================

// outer subdomain
Line Loop(1) = {1, 14, -5, -13};
Line Loop(2) = {2, 15, -6, -14};
Line Loop(3) = {3, 16, -7, -15};
Line Loop(4) = {4, 13, -8, -16};

// inner subdomain
Line Loop(5) = {5, 18, -9, -17};
Line Loop(6) = {6, 19, -10, -18};
Line Loop(7) = {7, 20, -11, -19};
Line Loop(8) = {8, 17, -12, -20};

//============================================
// SURFACES
//============================================

// outer subdomain
Plane Surface(1) = {1};
Plane Surface(2) = {2};
Plane Surface(3) = {3};
Plane Surface(4) = {4};

// inner subdomain
Plane Surface(5) = {5};
Plane Surface(6) = {6};
Plane Surface(7) = {7};
Plane Surface(8) = {8};

//============================================
// TRANSFINITES
//============================================

// outer subdomain
Transfinite Line{1:12} = Round(1.0/lc1);
Transfinite Surface{1} = {1, 2, 6, 7};
Transfinite Surface{2} = {2, 3, 7, 8};
Transfinite Surface{3} = {3, 4, 8, 9};
Transfinite Surface{4} = {1, 4, 6, 9};

// inner subdomain
Transfinite Line{13:20} = Round(1.0/lc2);
Transfinite Surface{5} = {6, 7, 11, 12};
Transfinite Surface{6} = {7, 8, 12, 13};
Transfinite Surface{7} = {8, 9, 13, 14};
Transfinite Surface{8} = {6, 9, 11, 14};

// quadrilateral mesh
Recombine Surface{1:8};
Mesh.Smoothing = 0;

//============================================
// PHYSICALS
//============================================

// outer boundary
Physical Point(1) = {1:5};
Physical Line(1) = {1:4};

// interface
Physical Point(2) = {6:10};
Physical Line(2) = {5:8};

// inner boundary
Physical Point(3) = {11:15};
Physical Line(3) = {9:12};

// outer subdomain
Physical Line(100) = {13:16};
Physical Surface(100) = {1:4};

// inner subdomain
Physical Line(200) = {17:20};
Physical Surface(200) = {5:8};

//============================================
// MESH OPTIONS
//============================================

Mesh.Algorithm = 5;
Mesh.Algorithm3D = 1;
Mesh.OptimizeNetgen = 1;
Mesh.Format = 1;
Mesh.MshFileVersion = 2.0;

//============================================
// OUTPUT
//============================================

// generate mesh
Mesh 2;

// write mesh
Save Sprintf(StrCat(outdir,"/",name,"_%g.msh"), N);

// end of file
