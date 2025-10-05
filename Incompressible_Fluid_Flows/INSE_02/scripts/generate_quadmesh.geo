// -*- coding: utf-8 -*-
/*
===============================================================================
CFDTestSuite | INSE_02
===============================================================================

DESCRIPTION:
------------
Generates quadrilateral structured meshes in MSH format.
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
https://github.com/ricardodpcosta/CFDTestSuite

DEPENDENCIES:
-------------
Gmsh (version >= 4.8.4)

USAGE:
------
gmsh -setnumber N 1 generate_quadmesh.geo

===============================================================================
*/

// refinement level
If (!Exists(N))
    N = 4;
EndIf

// domain center
cx = 0.0;
cy = 0.0;

// outer boundary
rO = 1.0;

// inner boundary
rI = 0.5;

// refinement controls
lc = 0.087/(1.38^(N-1));

// output controls
outdir = "../meshes";
name = "quadmesh";

//============================================
// POINTS
//============================================

// outer boundary
Point(1) = {cx-rO, cy, 0.0};
Point(2) = {cx, cy+rO, 0.0};
Point(3) = {cx+rO, cy, 0.0};
Point(4) = {cx, cy-rO, 0.0};
Point(5) = {cx, cy, 0.0};

// inner boundary
Point(6) = {cx-rI, cy, 0.0};
Point(7) = {cx, cy+rI, 0.0};
Point(8) = {cx+rI, cy, 0.0};
Point(9) = {cx, cy-rI, 0.0};
Point(10) = {cx, cy, 0.0};

//============================================
// LINES
//============================================

// outer boundary
Circle(1) = {1, 5, 2};
Circle(2) = {2, 5, 3};
Circle(3) = {3, 5, 4};
Circle(4) = {4, 5, 1};

// inner boundary
Circle(5) = {6, 10, 7};
Circle(6) = {7, 10, 8};
Circle(7) = {8, 10, 9};
Circle(8) = {9, 10, 6};

// outer subdomain
Line(9) = {1, 6};
Line(10) = {2, 7};
Line(11) = {3, 8};
Line(12) = {4, 9};

//============================================
// LINE LOOPS
//============================================

// domain
Line Loop(1) = {1, 10, -5, -9};
Line Loop(2) = {2, 11, -6, -10};
Line Loop(3) = {3, 12, -7, -11};
Line Loop(4) = {4, 9, -8, -12};


//============================================
// SURFACES
//============================================

// domain
Plane Surface(1) = {1};
Plane Surface(2) = {2};
Plane Surface(3) = {3};
Plane Surface(4) = {4};

//============================================
// TRANSFINITES
//============================================

// domain
Transfinite Line{1:12} = Round(1.0/lc);
Transfinite Surface{1} = {1, 2, 6, 7};
Transfinite Surface{2} = {2, 3, 7, 8};
Transfinite Surface{3} = {3, 4, 8, 9};
Transfinite Surface{4} = {1, 4, 6, 9};

// quadrilateral mesh
Recombine Surface{1:8};
Mesh.Smoothing = 0;

//============================================
// PHYSICALS
//============================================

// outer boundary
Physical Point(1) = {1:5};
Physical Line(1) = {1:4};

// inner boundary
Physical Point(2) = {6:10};
Physical Line(2) = {5:8};

// domain
Physical Line(100) = {9:12};
Physical Surface(100) = {1:4};

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
