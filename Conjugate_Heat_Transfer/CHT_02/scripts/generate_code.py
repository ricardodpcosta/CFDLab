#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
CFD-TESTSUITE | CHT_02
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

# constant parameters
rA, rAB, rB = sympy.symbols("rA rAB rB", real=True)
beta1, beta2 = sympy.symbols("beta1 beta2", real=True)
alphaA, alphaB = sympy.symbols("alphaA alphaB", real=True)
wA, wB = sympy.symbols("wA wB", real=True)
n = sympy.symbols("n", real=True)

# domain parameters
gamma1, gamma2, gamma3 = sympy.symbols("gamma1 gamma2 gamma3", real=True)

# solution parameters
aA, bA, aB, bB = sympy.symbols("aA bA aB bB", real=True)

# coordinate system
r, theta = sympy.symbols("r theta", real=True)
x, y = sympy.symbols("x y", real=True)

#============================================
# DOMAIN GEOMETRY
#============================================

# interface parametrisation
T = rAB*(1 + beta1*sympy.cos(beta2*theta))

# domain mapping
D = gamma1 + gamma2*r + gamma3*r**2

# interface normal vector
dT_dtheta = sympy.diff(T, theta)
nAB = 1/sympy.sqrt(T**2 + dT_dtheta**2) \
        *sympy.Matrix([[sympy.cos(theta), sympy.sin(theta)], \
                        [sympy.sin(theta), -sympy.cos(theta)]]) \
        *sympy.Matrix([T, dT_dtheta])

#============================================
# DOMAIN PARAMETERS
#============================================

# outer boundary
eq1 = sympy.Eq(D.subs(r, rA), rA)

# inner boundary
eq2 = sympy.Eq(D.subs(r, rB), rB)

# interface
eq3 = sympy.Eq(D.subs(r, T), rAB)

# solve for coefficients
sol = sympy.solve([eq1, eq2, eq3], (gamma1, gamma2, gamma3), dict=True)
if not sol:
    raise RuntimeError("Could not solve for coefficients symbolically.")
sol = sol[0]

# substitute into domain mapping
D = sympy.simplify(D.subs(sol))

#============================================
# MANUFACTURED SOLUTIONS
#============================================

# manufactured solutions
phiA = (aA*sympy.log(D) + bA)*sympy.cos(n*theta)
phiB = (aB*sympy.log(D) + bB)*sympy.cos(n*theta)

#============================================
# SOLUTION PARAMETERS
#============================================

# dirichlet boundary conditions
eq1 = sympy.Eq(phiA.subs(D, rA), 1)
eq2 = sympy.Eq(phiB.subs(D, rB), 0)

# solution continuity at interface
eq3 = sympy.Eq(phiA.subs(r, T), phiB.subs(r, T))

# flux conservation at interface
dphiA_dr = sympy.diff(phiA, r)
dphiB_dr = sympy.diff(phiB, r)
eq4 = sympy.Eq(-alphaA*dphiA_dr.subs(r, T), -alphaB*dphiB_dr.subs(r, T))

# solve for coefficients
sol = sympy.solve([eq1, eq2, eq3, eq4], (aA, bA, aB, bB), dict=True)
if not sol:
    raise RuntimeError("Could not solve for coefficients symbolically.")
sol = sol[0]

aA=sol[aA]

sympy.pprint(sympy.simplify(aA))


sympy.pprint(phiA)
sympy.pprint(sympy.simplify(phiA))

# substitute into manufactured solutions
# phiA = sympy.simplify(phiA.subs(sol))
# phiB = sympy.simplify(phiB.subs(sol))

#============================================
# VELOCITY FIELDS
#============================================

# velocity fields
uA_r = wA*r*(r-rA)*dT_dtheta/(T-rA)
uA_theta = wA*r
uB_r = wB*r*(r-rB)*dT_dtheta/(T-rB)
uB_theta = wB*r

# Cartesian unit basis
uA = sympy.Matrix([uA_r*sympy.cos(theta) - uA_theta*sympy.sin(theta),
                    uA_r*sympy.sin(theta) + uA_theta*sympy.cos(theta)])
uB = sympy.Matrix([uB_r*sympy.cos(theta) - uB_theta*sympy.sin(theta),
                    uB_r*sympy.sin(theta) + uB_theta*sympy.cos(theta)])

#============================================
# SOURCE-TERMS
#============================================

# diffusive terms
diffA = -alphaA*((1/r)*sympy.diff(r*sympy.diff(phiA, r), r) + (1/r**2)*sympy.diff(sympy.diff(phiA, theta), theta))
diffB = -alphaB*((1/r)*sympy.diff(r*sympy.diff(phiB, r), r) + (1/r**2)*sympy.diff(sympy.diff(phiB, theta), theta))

# convective terms
convA = uA_r*sympy.diff(phiA, r) + (uA_theta/r)*sympy.diff(phiA, theta)
convB = uB_r*sympy.diff(phiB, r) + (uB_theta/r)*sympy.diff(phiB, theta)

# source-terms
fA = sympy.simplify(convA + diffA)
fB = sympy.simplify(convB + diffB)

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
alphaA = 2.0
alphaB = 1.0
wA = 1.0
wB = -1.0
n = 4

# arguments list
args_list = [("x", x), ("y", y)]

# constants list
consts_list = [("rA", rA), ("rAB", rAB), ("rB", rB), ("alphaA", alphaA), ("alphaB", alphaB),
                ("wA", wA), ("wB", wB), ("n", n)]

# parameters list
params_list = [("r", r), ("theta", theta)]
paramsA_list = [("r", r), ("theta", theta), ("aA", sol[aA]), ("bA", sol[bA])]
paramsB_list = [("r", r), ("theta", theta), ("aB", sol[aB]), ("bB", sol[bB])]

# functions list
funcs_list = [("uA", uA, args_list, params_list),("uB", uB, args_list, params_list),
                ("phiA", phiA, args_list, paramsA_list), ("phiB", phiB, args_list, paramsB_list),
                ("fA", fA, args_list, paramsA_list), ("fB", fB, args_list, paramsB_list)]

# generate implementations in C/C++
contents = ["// Auto-generated by generate_code.py", "#ifndef CHT_02_H",
            "#define CHT_02_H", "#include <cmath>"]
contents.append(write_cpp_constants(consts_list))
for (name, expr, args_list, params_list) in funcs_list:
    try:
        code = write_cpp_function(name, expr, args_list, params_list)
        contents.append(code)
    except Exception as e:
        print("C/C++ generation failed for", name, ":", e)
contents.append("#endif")
contents = "\n\n".join(contents) + "\n"
write_file(os.path.join(outdir, "cht_02.h"), contents)

# write test file in C/C++
contents = write_cpp_test("cht_02")
write_file(os.path.join(outdir, "test.cpp"), contents)

# generate implementations in Fortran
contents = ["! Auto-generated by generate_code.py", "module cht_02", "implicit none"]
contents.append(write_fortran_constants(consts_list))
contents.append("contains")
for (name, expr, args_list, params_list) in funcs_list:
    try:
        code = write_fortran_function(name, expr, args_list, params_list)
        contents.append(code)
    except Exception as e:
        print("Fortran generation failed for", name, ":", e)
contents.append("end module cht_02")
contents = "\n\n".join(contents) + "\n"
write_file(os.path.join(outdir, "cht_02.f90"), contents)

# write test file in Fortran
contents = write_fortran_test("cht_02")
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
write_file(os.path.join(outdir, "cht_02.m"), contents)

# write test file in Octave/Matlab
contents = write_octave_test("cht_02")
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
write_file(os.path.join(outdir, "cht_02.py"), contents)

# write test file in Python
contents = write_python_test("cht_02")
write_file(os.path.join(outdir, "test.py"), contents)

print("\nGeneration complete. Files are in:", outdir)

# end of file
