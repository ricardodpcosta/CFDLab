// -*- coding: utf-8 -*-
/*
===============================================================================
CFD-TESTSUITE | CHT_04
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
np = Round(55*(1.38^(N-1)));
lc = 1.0/Round(6*(1.4^(N-1)));

// output controls
outdir = "../meshes";
name = "quadmesh";

//============================================
// POINTS
//============================================

// outer boundary
For i In {0:np-1}
      t = i*2.0*Pi/np;
      r = rA*(1.0+betaA_1*Cos(betaA_2*t));
      x = r*Cos(t);
      y = r*Sin(t);
      Point(i+1) = {cx+x, cy+y, 0.0, lc};
      // If(i==  0)
      //       p1x = cx+x;
      //       p1y = cy+y;
      // EndIf
      // If(i==  1)
      //       p2x = cx+x;
      //       p2y = cy+y;
      //       Printf("%23.16f", (p2y-p1y)/(p2x-p1x));
      // EndIf
EndFor

// interface
For i In {0:np-1}
      t = i*2.0*Pi/np;
      r = rAB*(1.0+betaAB_1*Cos(betaAB_2*t));
      x = r*Cos(t);
      y = r*Sin(t);
      Point(i+np+1) = {cx+x, cy+y, 0.0, lc};
      // If(i==  0)
      //       p1x = cx+x;
      //       p1y = cy+y;
      // EndIf
      // If(i==  1)
      //       p2x = cx+x;
      //       p2y = cy+y;
      //       Printf("%23.16f", (p2y-p1y)/(p2x-p1x));
      // EndIf
EndFor

// inner boundary
For i In {0:np-1}
      t = i*2.0*Pi/np;
      r = rB*(1.0+betaB_1*Cos(betaB_2*t));
      x = r*Cos(t);
      y = r*Sin(t);
      Point(i+2*np+1) = {cx+x, cy+y, 0.0, lc};
      // If(i==  0)
      //       p1x = cx+x;
      //       p1y = cy+y;
      // EndIf
      // If(i==  1)
      //       p2x = cx+x;
      //       p2y = cy+y;
      //       Printf("%23.16f", (p2y-p1y)/(p2x-p1x));
      // EndIf
EndFor

//============================================
// LINES
//============================================

// outer boundary
For i In {1:np-1}
      Line(i) = {i, i+1};
      // Printf("%10g %9g %9g", 2, i, i+1);
EndFor
Line(np) = {np, 1};
// Printf("%10g %9g %9g", 2, np, 1);

// interface
For i In {1:np-1}
      Line(i+np) = {i+np, i+np+1};
      // Printf("%10g %9g %9g", 2, i+np, i+np+1);
EndFor
Line(2*np) = {2*np, np+1};
// Printf("%10g %9g %9g", 2, 2*np, np+1);

// inner boundary
For i In {1:np-1}
      Line(i+2*np) = {i+2*np, i+2*np+1};
      // Printf("%10g %9g %9g", 2, i+2*np, i+2*np+1);
EndFor
Line(3*np) = {3*np, 2*np+1};
// Printf("%10g %9g %9g", 2, 3*np, 2*np+1);

// outer subdomain
For i In {1:np}
      Line(i+3*np) = {i, i+np};
EndFor

// inner subdomain
For i In {1:np}
      Line(i+4*np) = {i+np, i+2*np};
EndFor

//============================================
// LINE LOOPS
//============================================

// outer subdomain
For i In {1:np-1}
      Line Loop(i) = {i, i+3*np+1, -(i+np), -(i+3*np)};
EndFor
Line Loop(np) = {np, 3*np+1, -2*np, -4*np};

// inner subdomain
For i In {1:np-1}
      Line Loop(i+np) = {i+np, i+4*np+1, -(i+2*np), -(i+4*np)};
EndFor
Line Loop(2*np) = {2*np, 4*np+1, -3*np, -5*np};

//============================================
// SURFACES
//============================================

// outer subdomain
For i In {1:np-1}
      Plane Surface(i) = {i};
EndFor
Plane Surface(np) = {np};

// inner subdomain
For i In {1:np-1}
      Plane Surface(i+np) = {i+np};
EndFor
Plane Surface(2*np) = {2*np};

//============================================
// TRANSFINITES
//============================================

// outer subdomain
Transfinite Line{1:2*np} = lc;
Transfinite Line{3*np+1:4*np} = Round(1.0/lc);
For i In {1:np-1}
      Transfinite Surface{i} = {i, i+1, i+np, i+np+1};
EndFor
Transfinite Surface{np} = {np, 1, np+1, 2*np};

// inner subdomain
Transfinite Line{1:2*np} = lc;
Transfinite Line{4*np+1:5*np} = Round(1.0/lc);
For i In {1:np-1}
      Transfinite Surface{i+np} = {i+np, i+np+1, i+2*np, i+2*np+1};
EndFor
Transfinite Surface{2*np} = {2*np, 1+np, 2*np+1, 3*np};

// quadrilateral mesh
Recombine Surface{1:2*np};
Mesh.Smoothing = 0;

//============================================
// PHYSICALS
//============================================

// outer boundary
Physical Point(1) = {1:np};
Physical Line(1) = {1:np};

// interface
Physical Point(2) = {1+np:2*np};
Physical Line(2) = {1+np:2*np};

// inner boundary
Physical Point(3) = {1+2*np:3*np};
Physical Line(3) = {1+2*np:3*np};

// outer subdomain
Physical Line(100) = {3*np+1:4*np};
Physical Surface(100) = {1:np};

// inner subdomain
Physical Line(200) = {4*np+1:5*np};
Physical Surface(200) = {np:2*np};

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
