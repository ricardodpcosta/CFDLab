// -*- coding: utf-8 -*-
/*
===============================================================================
CFD-TESTSUITE | CHT_04
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
https://github.com/ricardodpcosta/CFDTestSuite

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
betaA_1 = 0.0;
betaA_2 = 8.0;

// interface
rAB = 0.75;
betaAB_1 = 0.04;
betaAB_2 = 8.0;

// inner boundary
rB = 0.5;
betaB_1 = 0.0;
betaB_2 = 8.0;

// refinement controls
np1 = Round(55*(1.4^(N-1)));
np2 = Round(70*(1.4^(N-1)));
np3 = Round(55*(1.4^(N-1)));
lc1 = 1.0;
lc2 = 1.0;
lc3 = 1.0;

// output controls
outdir = "../meshes";
name = "triamesh";

//============================================
// POINTS
//============================================

// outer boundary
For i In {0:np1-1}
      t = i*2.0*Pi/np1;
      r = rA*(1.0+betaA_1*Cos(betaA_2*t));
      x = r*Cos(t);
      y = r*Sin(t);
      Point(i+1) = {cx+x, cy+y, 0.0, lc1};
      // If(i == 0)
      //       p1x = cx+x;
      //       p1y = cy+y;
      // EndIf
      // If(i == 1)
      //       p2x = cx+x;
      //       p2y = cy+y;
      //       Printf("%23.16f", (p2y-p1y)/(p2x-p1x));
      // EndIf
EndFor

// interface
For i In {0:np2-1}
      t = i*2.0*Pi/np2;
      r = rAB*(1.0+betaAB_1*Cos(betaAB_2*t));
      x = r*Cos(t);
      y = r*Sin(t);
      Point(i+np1+1) = {cx+x, cy+y, 0.0, lc2};
      // If(i == 0)
      //       p1x = cx+x;
      //       p1y = cy+y;
      // EndIf
      // If(i == 1)
      //       p2x = cx+x;
      //       p2y = cy+y;
      //       Printf("%23.16f", (p2y-p1y)/(p2x-p1x));
      // EndIf
EndFor

// inner boundary
For i In {0:np3-1}
      t = i*2.0*Pi/np3;
      r = rB*(1.0+betaB_1*Cos(betaB_2*t));
      x = r*Cos(t);
      y = r*Sin(t);
      Point(i+np1+np2+1) = {cx+x, cy+y, 0.0, lc3};
      // If(i == 0)
      //       p1x = cx+x;
      //       p1y = cy+y;
      // EndIf
      // If(i == 1)
      //       p2x = cx+x;
      //       p2y = cy+y;
      //       Printf("%23.16f", (p2y-p1y)/(p2x-p1x));
      // EndIf
EndFor

//============================================
// LINES
//============================================

// outer boundary
For i In {1:np1-1}
      Line(i) = {i, i+1};
      // Printf("%10g %9g %9g", 2, i, i+1);
EndFor
Line(np1) = {np1, 1};
// Printf("%10g %9g %9g", 2, np1, 1);

// interface
For i In {1:np2-1}
      Line(i+np1) = {i+np1, i+np1+1};
      // Printf("%10g %9g %9g", 2, i+np1, i+np1+1);
EndFor
Line(np1+np2) = {np1+np2, np1+1};
// Printf("%10g %9g %9g", 2, np1+np2, np1+1);

// inner boundary
For i In {1:np3-1}
      Line(i+np1+np2) = {i+np1+np2, i+np1+np2+1};
      // Printf("%10g %9g %9g", 2, i+np1+np2, i+np1+np2+1);
EndFor
Line(np1+np2+np3) = {np1+np2+np3, np1+np2+1};
// Printf("%10g %9g %9g", 2, np1+np2+np3, np1+np2+1);

//============================================
// LINE LOOPS
//============================================

// outer boundary
Line Loop(1) = {1:np1};
// For i In {1:np1}
//       Printf("%10g", i);
// EndFor

// interface
Line Loop(2) = {np1+1:np1+np2};
// For i In {np1+1:np1+np2}
//       Printf("%10g", i);
// EndFor

// inner boundary
Line Loop(3) = {np1+np2+1:np1+np2+np3};
// For i In {np1+1:np1+np2+np3}
//       Printf("%10g", i);
// EndFor

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
Physical Point(1) = {1:np1};
Physical Line(1) = {1:np1};

// interface
Physical Point(2) = {1+np1:np1+np2};
Physical Line(2) = {1+np1:np1+np2};

// inner boundary
Physical Point(3) = {1+np1+np2:np1+np2+np3};
Physical Line(3) = {1+np1+np2:np1+np2+np3};

// outer subdomain
Physical Surface(100) = {1};

// inner subdomain
Physical Surface(200) = {2};

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
