#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
CFDLab | CHT_01
===============================================================================

DESCRIPTION:
------------
    Generates code for the symbolic expressions of parameters and functions in
    multiple programming languages: C/C++, Fortran, Octave/Matlab, and Python.
    Outputs are saved in `codes/`.

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
– Python (version >= 3.9)
– SymPy (version >= 1.6)

USAGE:
------
python generate_code.py

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
alphaA, alphaB = sympy.symbols("alphaA alphaB", real=True, positive=True)
wA, wB = sympy.symbols("wA wB", real=True)
n = sympy.symbols("n", real=True)

# parameters
aA, bA, aB, bB = sympy.symbols("aA bA aB bB", real=True)

# coordinate system
r, theta = sympy.symbols("r theta", real=True)
x, y = sympy.symbols("x y", real=True)

#============================================
# MANUFACTURED SOLUTIONS
#============================================

# manufactured solutions
phiA = (aA*sympy.log(r) + bA)*sympy.cos(n*theta)
phiB = (aB*sympy.log(r) + bB)*sympy.cos(n*theta)

#============================================
# SOLUTION PARAMETERS
#============================================

# temperature at boundaries
phiA_rA = phiA.subs(r, rA)
phiB_rB = phiB.subs(r, rB)

# simplify expressions
phiA_rA = phiA_rA.factor().cancel()
phiB_rB = phiB_rB.factor().cancel()

# temperature at interface
phiA_rAB = phiA.subs(r, rAB)
phiB_rAB = phiB.subs(r, rAB)

# simplify expressions
phiA_rAB = phiA_rAB.factor().cancel()
phiB_rAB = phiB_rAB.factor().cancel()

# temperature derivatives at interface
dphiA_dr_rAB = (sympy.diff(phiA, r)).subs(r, rAB)
dphiB_dr_rAB = (sympy.diff(phiB, r)).subs(r, rAB)

# simplify expressions
dphiA_dr_rAB = dphiA_dr_rAB.factor().cancel()
dphiB_dr_rAB = dphiB_dr_rAB.factor().cancel()

# boundary conditions
eq1 = sympy.Eq(phiA_rA, sympy.cos(n*theta))
eq2 = sympy.Eq(phiB_rB, 0)

# solution continuity at interface
eq3 = sympy.Eq(phiA_rAB, phiB_rAB)
eq4 = sympy.Eq(-alphaA*dphiA_dr_rAB, -alphaB*dphiB_dr_rAB)

# solve for parameters
sol = sympy.solve([eq1, eq2, eq3, eq4], (aA, bA, aB, bB), dict=True)
if not sol:
    raise RuntimeError("Could not solve for parameters symbolically.")
sol = sol[0]

# simplify expressions
sol[aA] = sol[aA].factor().cancel()
sol[bA] = sol[bA].factor().cancel()
sol[aB] = sol[aB].factor().cancel()
sol[bB] = sol[bB].factor().cancel()

# substitute into manufactured solutions
# phiA = phiA.subs(sol)
# phiB = phiB.subs(sol)

# simplify expressions
# phiA = phiA.factor().cancel()
# phiB = phiB.factor().cancel()

#============================================
# VELOCITY FIELDS
#============================================

# velocity fields
uA_r = 0
uA_theta = wA*r
uB_r = 0
uB_theta = wB*r

# simplify expressions
# uA_r = uA_r.factor().cancel()
# uA_theta = uA_theta.factor().cancel()
# uB_r = uB_r.factor().cancel()
# uB_theta = uB_theta.factor().cancel()

# Cartesian unit basis
uA = sympy.Matrix([[sympy.cos(theta), -sympy.sin(theta)], \
                    [sympy.sin(theta), sympy.cos(theta)]]) \
                    *sympy.Matrix([uA_r, uA_theta])
uB = sympy.Matrix([[sympy.cos(theta), -sympy.sin(theta)], \
                    [sympy.sin(theta), sympy.cos(theta)]]) \
                    *sympy.Matrix([uB_r, uB_theta])

#============================================
# SOURCE TERMS
#============================================

# convective terms
convA = uA_r*sympy.diff(phiA, r) + (uA_theta/r)*sympy.diff(phiA, theta)
convB = uB_r*sympy.diff(phiB, r) + (uB_theta/r)*sympy.diff(phiB, theta)

# simplify expressions
convA = convA.factor().cancel()
convB = convB.factor().cancel()

# diffusive terms
diffA = -alphaA*((1/r)*sympy.diff(r*sympy.diff(phiA, r), r) \
            + (1/r**2)*sympy.diff(sympy.diff(phiA, theta), theta))
diffB = -alphaB*((1/r)*sympy.diff(r*sympy.diff(phiB, r), r) \
            + (1/r**2)*sympy.diff(sympy.diff(phiB, theta), theta))

# simplify expressions
diffA = diffA.factor().cancel()
diffB = diffB.factor().cancel()

# source terms
fA = convA + diffA
fB = convB + diffB

# simplify expressions
fA = fA.factor().cancel()
fB = fB.factor().cancel()

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
n = 4.0

# arguments list
args_list = [("x", x), ("y", y)]

# constants list
consts_list = [("rA", rA), ("rAB", rAB), ("rB", rB), ("alphaA", alphaA), ("alphaB", alphaB), \
                ("wA", wA), ("wB", wB), ("n", n)]

# parameters list
params_list = [("r", r), ("theta", theta)]
paramsA_list = [("r", r), ("theta", theta), ("aA", sol[aA]), ("bA", sol[bA])]
paramsB_list = [("r", r), ("theta", theta), ("aB", sol[aB]), ("bB", sol[bB])]

# functions list
funcs_list = [("uA", uA, args_list, params_list),("uB", uB, args_list, params_list), \
                ("phiA", phiA, args_list, paramsA_list), ("phiB", phiB, args_list, paramsB_list), \
                ("fA", fA, args_list, paramsA_list), ("fB", fB, args_list, paramsB_list)]

# generate code
outdir = "../codes"
name = "cht_01"
os.makedirs(outdir, exist_ok=True)
write_cpp_file(outdir, name, consts_list, funcs_list)
write_fortran_file(outdir, name, consts_list, funcs_list)
write_octave_file(outdir, name, consts_list, funcs_list)
write_python_file(outdir, name, consts_list, funcs_list)
write_cpp_test(outdir, name)
write_fortran_test(outdir, name)
write_octave_test(outdir, name)
write_python_test(outdir, name)
print("\nGeneration complete.")

# end of file
