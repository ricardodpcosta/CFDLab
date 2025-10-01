// -*- coding: utf-8 -*-
/*
===============================================================================
CFDLab | CHT_01
===============================================================================

DESCRIPTION:
------------
Generates triangular unstructured meshes in MSH format.
Mesh refinement can be controlled through the command-line option `-setnumber N <value>`
where `<value>` is a numerical argument specifying the desired refinement level
(default: `1`).
Outputs are saved in `meshes/`.

AUTHOR:
-------
Ricardo Costa (rcosta@dep.uminho.pt)

LICENSE:
--------
MIT License (see LICENSE file for details)

REPOSITORY:
-----------
https://github.com/ricardodpcosta/CFDLab

DEPENDENCIES:
-------------
Gmsh (version >= 4.8.4)

USAGE:
------
gmsh -setnumber N 1 generate_triamesh.geo

===============================================================================
*/

//============================================
// PARAMETERS
//============================================

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
lc1 = (0.1*rA)/(1.38^(N-1));
lc2 = (0.1*rAB)/(1.38^(N-1));
lc3 = (0.1*rB)/(1.38^(N-1));

// output controls
outdir = "../meshes";
name = "triamesh";

//============================================
// POINTS
//============================================

// outer boundary
Point(1) = {cx-rA, cy, 0.0, lc1};
Point(2) = {cx, cy+rA, 0.0, lc1};
Point(3) = {cx+rA, cy, 0.0, lc1};
Point(4) = {cx, cy-rA, 0.0, lc1};
Point(5) = {cx, cy, 0.0, lc1};

// interface
Point(6) = {cx-rAB, cy, 0.0, lc2};
Point(7) = {cx, cy+rAB, 0.0, lc2};
Point(8) = {cx+rAB, cy, 0.0, lc2};
Point(9) = {cx, cy-rAB, 0.0, lc2};
Point(10) = {cx, cy, 0.0, lc2};

// inner boundary
Point(11) = {cx-rB, cy, 0.0, lc3};
Point(12) = {cx, cy+rB, 0.0, lc3};
Point(13) = {cx+rB, cy, 0.0, lc3};
Point(14) = {cx, cy-rB, 0.0, lc3};
Point(15) = {cx, cy, 0.0, lc3};

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

//============================================
// LINE LOOPS
//============================================

// outer boundary
Line Loop(1) = {1:4};

// interface
Line Loop(2) = {5:8};

// inner boundary
Line Loop(3) = {9:12};

//============================================
// SURFACES
//============================================

// outer subdomain
Plane Surface(1) = {1, 2};

// inner subdomain
Plane Surface(2) = {2, 3};

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
Physical Surface(100) = {1:4};

// inner subdomain
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
