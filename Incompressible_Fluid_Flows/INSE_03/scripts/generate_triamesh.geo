// -*- coding: utf-8 -*-
/*
===============================================================================
CFDLab | INSE_02
===============================================================================

Description:
    Generates triangular unstructured meshes in MSH format.
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
rO = 1.0;

// inner boundary
rI = 0.5;

// refinement controls
lc1 = (0.16*rO)/(1.38^(N-1));
lc2 = (0.16*rI)/(1.38^(N-1));

// output controls
outdir = "../meshes";
name = "triamesh";

//============================================
// POINTS
//============================================

// outer boundary
Point(1) = {cx-rO, cy, 0.0, lc1};
Point(2) = {cx, cy+rO, 0.0, lc1};
Point(3) = {cx+rO, cy, 0.0, lc1};
Point(4) = {cx, cy-rO, 0.0, lc1};
Point(5) = {cx, cy, 0.0, lc1};

// inner boundary
Point(6) = {cx-rI, cy, 0.0, lc2};
Point(7) = {cx, cy+rI, 0.0, lc2};
Point(8) = {cx+rI, cy, 0.0, lc2};
Point(9) = {cx, cy-rI, 0.0, lc2};
Point(10) = {cx, cy, 0.0, lc2};

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

//============================================
// LINE LOOPS
//============================================

// outer boundary
Line Loop(1) = {1:4};

// inner boundary
Line Loop(2) = {5:8};

//============================================
// SURFACES
//============================================

// domain
Plane Surface(1) = {1, 2};

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
