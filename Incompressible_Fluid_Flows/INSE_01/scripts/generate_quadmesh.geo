// -*- coding: utf-8 -*-
/*
===============================================================================
CFDLab | INSE_01
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

// domain
cx = 0.0;
cy = 0.0;

// length
L = 1.0;

// height
H = 1.0;

// refinement controls
lc1 = 10.0*(2.0^(N-1));
lc2 = 10.0*(2.0^(N-1));

// output controls
outdir = "../meshes";
name = "quadmesh";

//============================================
// POINTS
//============================================

// boundary
Point(1) = {cx, cy, 0.0};
Point(2) = {cx+L, cy, 0.0};

//============================================
// LINES
//============================================

// boundary
Line(1) = {1, 2};

//============================================
// LINE LOOPS
//============================================

//============================================
// SURFACES
//============================================

//============================================
// TRANSFINITES
//============================================

// domain
Transfinite Curve{1} = lc1+1;
surf[]=Extrude{0.0, H, 0.0}{Line{1}; Layers{lc2}; Recombine;};

//============================================
// PHYSICALS
//============================================

// bottom boundary
Physical Point(1) = {1};
Physical Line(1) = {1};

// top boundary
Physical Point(2) = {4};
Physical Line(2) = {2};

// left boundary
Physical Point(3) = {3};
Physical Line(3) = {3};

// right boundary
Physical Point(4) = {2};
Physical Line(4) = {4};

// domain
Physical Surface(100) = {5};

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
