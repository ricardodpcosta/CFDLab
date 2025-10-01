// -*- coding: utf-8 -*-
/*
===============================================================================
CFDLab | INSE_01
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

// domain
cx = 0.0;
cy = 0.0;

// length
L = 1.0;

// height
H = 1.0;

// refinement controls
lc1 = 0.1/(2.0^(N-1));
lc2 = 0.1/(2.0^(N-1));
lc3 = 0.1/(2.0^(N-1));
lc4 = 0.1/(2.0^(N-1));

// output controls
outdir = "../meshes";
name = "triamesh";

//============================================
// POINTS
//============================================

// boundary
Point(1) = {cx, cy, 0.0, lc1};
Point(2) = {cx+L, cy, 0.0, lc2};
Point(3) = {cx+L, cy+H, 0.0, lc3};
Point(4) = {cx, cy+H, 0.0, lc4};

//============================================
// LINES
//============================================

// boundary
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};

//============================================
// REFINEMENT
//============================================

// boundary
// Transfinite Curve{1, 2, 3, 4} = 20*N Using Bump 0.5;
// Mesh.CharacteristicLengthMin = 0.0;
// Mesh.CharacteristicLengthMax = 1.0;

//============================================
// LINE LOOPS
//============================================

// boundary
Line Loop(1) = {1, 2, 3, 4};

//============================================
// SURFACES
//============================================

// domain
Plane Surface(1) = {1};

//============================================
// PHYSICALS
//============================================

// bottom boundary
Physical Point(1) = {1};
Physical Line(1) = {1};

// top boundary
Physical Point(2) = {2};
Physical Line(2) = {2};

// left boundary
Physical Point(3) = {3};
Physical Line(3) = {3};

// right boundary
Physical Point(4) = {4};
Physical Line(4) = {4};

// domain
Physical Surface(100) = {1};

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
Save Sprintf(StrCat(outdir, "/", name, "_%g.msh"), N);

// end of file
