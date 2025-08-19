#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
CFD-TESTSUITE | CHT_04
===============================================================================

Description:
    Generates code for the symbolic expressions of parameters and functions in
    multiple programming languages: C/C++, Fortran, Octave/Matlab, and Python.
    Outputs are saved in `codes/`.

Author:
    Ricardo Costa (rcosta@dep.uminho.pt)

License:
    MIT License (see LICENSE file for details)

Repository:
    https://github.com/ricardodpcosta/CFD-TestSuite

Dependencies:
    Python (version >= 3.9)
    SymPy (version >= 1.6)

Usage:
    python symbolic_code.py
===============================================================================
"""

# import modules
import os
import sympy
from helpers import *

#============================================
# SYMBOLIC VARIABLES
#============================================

# constants
rA, rAB, rB = sympy.symbols("rA rAB rB", real=True, positive=True)
betaAB_1, betaAB_2 = sympy.symbols("betaAB_1 betaAB_2", real=True)
alphaA, alphaB = sympy.symbols("alphaA alphaB", real=True, positive=True)
wA, wB = sympy.symbols("wA wB", real=True)
h = sympy.symbols("h", real=True)

# parameters
d1, d2, d3 = sympy.symbols("d1 d2 d3", real=True)
aA, bA, aB, bB = sympy.symbols("aA bA aB bB", real=True)

# coordinate system
r, theta = sympy.symbols("r theta", real=True)
x, y = sympy.symbols("x y", real=True)

#============================================
# DOMAIN GEOMETRY
#============================================

# interface radius
RAB = rAB*(1 + betaAB_1*sympy.cos(betaAB_2*theta))

# domain mapping
D = d1 + d2*r + d3*r**2

# interface normal vector
dRAB_dtheta = sympy.diff(RAB, theta)
nAB = 1/sympy.sqrt(RAB**2 + dRAB_dtheta**2) \
        *sympy.Matrix([[sympy.cos(theta), -sympy.sin(theta)], \
                        [sympy.sin(theta), sympy.cos(theta)]]) \
        *sympy.Matrix([-RAB, dRAB_dtheta])

# simplify expressions
nAB[0] = nAB[0].factor().cancel()
nAB[1] = nAB[1].factor().cancel()

#============================================
# DOMAIN PARAMETERS
#============================================

# outer boundary
eq1 = sympy.Eq(D.subs(r, rA), rA)

# inner boundary
eq2 = sympy.Eq(D.subs(r, rB), rB)

# interface
eq3 = sympy.Eq(D.subs(r, RAB), rAB)

# solve for parameters
sol1 = sympy.solve([eq1, eq2, eq3], (d1, d2, d3), dict=True)
if not sol1:
    raise RuntimeError("Could not solve for coefficients symbolically.")
sol1 = sol1[0]

# simplify expressions
sol1[d1] = sol1[d1].factor().cancel()
sol1[d2] = sol1[d2].factor().cancel()
sol1[d3] = sol1[d3].factor().cancel()

# substitute into domain mapping
D = D.subs(sol1)

# simplify expression
D = D.factor().cancel()

#============================================
# MANUFACTURED SOLUTIONS
#============================================

# manufactured solutions
phiA = aA*sympy.log(D) + bA
phiB = aB*sympy.log(D) + bB

#============================================
# SOLUTION PARAMETERS
#============================================

# the reference solution on the circular interface is used to compute
# the solution parameters as it is not necessaryto account for the normal
# vector since the tangential derivative along the interface vanishes

# dirichlet boundary conditions
eq1 = sympy.Eq(phiA.subs(r, rA).factor().cancel(), 1)
eq2 = sympy.Eq(phiB.subs(r, rB).factor().cancel(), 0)

# solution jump at interface
dphiA_dr = sympy.diff(phiA, r)
eq3 = sympy.Eq(alphaA*dphiA_dr.subs(r, RAB).factor().cancel(),
        h*(phiA.subs(r, RAB)-phiB.subs(r, RAB)).factor().cancel())

sympy.pprint(dphiA_dr.factor().cancel())
sympy.pprint(dphiA_dr.simplify())

sympy.pprint(eq1)
sympy.pprint(eq2)
sympy.pprint(eq3)
sympy.pprint(eq4)

# flux conservation at interface
dphiB_dr = sympy.diff(phiB, r)
eq4 = sympy.Eq(-alphaA*dphiA_dr.subs(r, RAB), -alphaB*dphiB_dr.subs(r, RAB))

# solve for parameters
sol2 = sympy.solve([eq1, eq2, eq3, eq4], (aA, bA, aB, bB), dict=True)
if not sol2:
    raise RuntimeError("Could not solve for parameters symbolically.")
sol2 = sol2[0]

# simplify expressions
sol2[aA] = sol2[aA].factor().cancel()
sol2[bA] = sol2[bA].factor().cancel()
sol2[aB] = sol2[aB].factor().cancel()
sol2[bB] = sol2[bB].factor().cancel()

# substitute into manufactured solutions
# phiA = phiA.subs(sol2)
# phiB = phiB.subs(sol2)

# simplify expressions
# phiA = phiA.factor().cancel()
# phiB = phiB.factor().cancel()

#============================================
# VELOCITY FIELDS
#============================================

# velocity fields
uA_r = wA*r*(r-rA)*dRAB_dtheta/(RAB-rA)
uA_theta = wA*r
uB_r = wB*r*(r-rB)*dRAB_dtheta/(RAB-rB)
uB_theta = wB*r

# simplify expressions
uA_r = uA_r.factor().cancel()
uA_theta = uA_theta.factor().cancel()
uB_r = uB_r.factor().cancel()
uB_theta = uB_theta.factor().cancel()

# Cartesian unit basis
uA = sympy.Matrix([[sympy.cos(theta), -sympy.sin(theta)], \
                    [sympy.sin(theta), sympy.cos(theta)]]) \
                    *sympy.Matrix([uA_r, uA_theta])
uB = sympy.Matrix([[sympy.cos(theta), -sympy.sin(theta)], \
                    [sympy.sin(theta), sympy.cos(theta)]]) \
                    *sympy.Matrix([uB_r, uB_theta])

#============================================
# SOURCE-TERMS
#============================================

# diffusive terms
diffA = -alphaA*((1/r)*sympy.diff(r*sympy.diff(phiA, r), r) \
            + (1/r**2)*sympy.diff(sympy.diff(phiA, theta), theta))
diffB = -alphaB*((1/r)*sympy.diff(r*sympy.diff(phiB, r), r) \
            + (1/r**2)*sympy.diff(sympy.diff(phiB, theta), theta))

# simplify expressions
# diffA = diffA.factor().cancel()
# diffB = diffB.factor().cancel()

# convective terms
convA = uA_r*sympy.diff(phiA, r) + (uA_theta/r)*sympy.diff(phiA, theta)
convB = uB_r*sympy.diff(phiB, r) + (uB_theta/r)*sympy.diff(phiB, theta)

# simplify expressions
convA = convA.factor().cancel()
convB = convB.factor().cancel()

# source-terms
fA = convA + diffA
fB = convB + diffB

# simplify expressions
# fA = fA.factor().cancel()
# fB = fB.factor().cancel()

#============================================
# OUTPUT
#============================================

# output directory
outdir = "../codes"
os.makedirs(outdir, exist_ok=True)

# coordinate system conversion
r = sympy.sqrt(x**2 + y**2)
theta = sympy.atan2(y,x)

# constant parameters values
rA = 1.0
rAB = 0.75
rB = 0.5
betaAB_1 = 0.04
betaAB_2 = 8.0
alphaA = 2.0
alphaB = 1.0
wA = 1.0
wB = -1.0
h = 1.0

# arguments list
args_list = [("x", x), ("y", y)]

# constants list
consts_list = [("rA", rA), ("rAB", rAB), ("rB", rB), ("betaAB_1", betaAB_1), ("betaAB_2", betaAB_2),
                ("alphaA", alphaA), ("alphaB", alphaB), ("wA", wA), ("wB", wB)]

# parameters list
params_list = [("r", r), ("theta", theta)]
paramsA_list = [("r", r), ("theta", theta), ("aA", sol2[aA]), ("bA", sol2[bA])]
paramsB_list = [("r", r), ("theta", theta), ("aB", sol2[aB]), ("bB", sol2[bB])]

# functions list
funcs_list = [("RAB", RAB, args_list, params_list), ("nAB", nAB, args_list, params_list),
                ("uA", uA, args_list, params_list), ("uB", uB, args_list, params_list),
                ("phiA", phiA, args_list, paramsA_list), ("phiB", phiB, args_list, paramsB_list),
                ("fA", fA, args_list, paramsA_list), ("fB", fB, args_list, paramsB_list)]

# generate implementations in C/C++
contents = ["// Auto-generated by generate_code.py", "#ifndef CHT_04_H",
            "#define CHT_04_H", "#include <cmath>"]
contents.append(write_cpp_constants(consts_list))
for (name, expr, args_list, params_list) in funcs_list:
    try:
        code = write_cpp_function(name, expr, args_list, params_list)
        contents.append(code)
    except Exception as e:
        print("C/C++ generation failed for", name, ":", e)
contents.append("#endif")
contents = "\n\n".join(contents) + "\n"
write_file(os.path.join(outdir, "cht_04.h"), contents)

# write test file in C/C++
contents = write_cpp_test("cht_04")
write_file(os.path.join(outdir, "test.cpp"), contents)

# generate implementations in Fortran
contents = ["! Auto-generated by generate_code.py", "module cht_04", "implicit none"]
contents.append(write_fortran_constants(consts_list))
contents.append("contains")
for (name, expr, args_list, params_list) in funcs_list:
    try:
        code = write_fortran_function(name, expr, args_list, params_list)
        contents.append(code)
    except Exception as e:
        print("Fortran generation failed for", name, ":", e)
contents.append("end module cht_04")
contents = "\n\n".join(contents) + "\n"
write_file(os.path.join(outdir, "cht_04.f90"), contents)

# write test file in Fortran
contents = write_fortran_test("cht_04")
write_file(os.path.join(outdir, "test.f90"), contents)

# generate implementations in Octave/Matlab
contents = ["% Auto-generated by generate_code.py"]
contents.append(write_octave_constants(consts_list))
for (name, expr, args_list, params_list) in funcs_list:
    try:
        code = write_octave_function(name, expr, args_list, consts_list, params_list)
        contents.append(code)
    except Exception as e:
        print("Octave/Matlab generation failed for", name, ":", e)
contents = "\n\n".join(contents) + "\n"
write_file(os.path.join(outdir, "cht_04.m"), contents)

# write test file in Octave/Matlab
contents = write_octave_test("cht_04")
write_file(os.path.join(outdir, "test.m"), contents)

# generate implementations in Python
contents = ["# Auto-generated by generate_code.py", "import math"]
contents.append(write_python_constants(consts_list))
for (name, expr, args_list, params_list) in funcs_list:
    try:
        code = write_python_function(name, expr, args_list, params_list)
        contents.append(code)
    except Exception as e:
        print("Python generation failed for", name, ":", e)
contents = "\n\n".join(contents) + "\n"
write_file(os.path.join(outdir, "cht_04.py"), contents)

# write test file in Python
contents = write_python_test("cht_04")
write_file(os.path.join(outdir, "test.py"), contents)

print("\nGeneration complete.")

# end of file
