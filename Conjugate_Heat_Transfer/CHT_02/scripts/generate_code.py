#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
CFDLab | CHT_02
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
nAB_norm = sympy.sqrt(RAB**2 + dRAB_dtheta**2)
nAB_r = -RAB/nAB_norm
nAB_theta = dRAB_dtheta/nAB_norm

# simplify expressions
nAB_r = nAB_r.factor().cancel()
nAB_theta = nAB_theta.factor().cancel()

# Cartesian unit basis
nAB = sympy.Matrix([[sympy.cos(theta), -sympy.sin(theta)], \
                    [sympy.sin(theta), sympy.cos(theta)]]) \
                    *sympy.Matrix([nAB_r, nAB_theta])

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

# simplify expressions
D = D.factor().cancel()

#============================================
# MANUFACTURED SOLUTIONS
#============================================

# manufactured solutions
phiA = aA*sympy.log(D) + bA
phiB = aB*sympy.log(D) + bB

# reference solutions
phiA_ref = aA*sympy.log(r) + bA
phiB_ref = aB*sympy.log(r) + bB

#============================================
# SOLUTION PARAMETERS
#============================================

# the reference solution on the circular interface is used to compute
# the solution parameters as it is not necessaryto account for the normal
# vector since the tangential derivative along the interface vanishes

# temperature at boundaries
phiA_ref_rA = phiA_ref.subs(r, rA)
phiB_ref_rB = phiB_ref.subs(r, rB)

# simplify expressions
phiA_ref_rA = phiA_ref_rA.factor().cancel()
phiB_ref_rB = phiB_ref_rB.factor().cancel()

# temperature at interface
phiA_ref_rAB = phiA_ref.subs(r, rAB)
phiB_ref_rAB = phiB_ref.subs(r, rAB)

# simplify expressions
phiA_ref_rAB = phiA_ref_rAB.factor().cancel()
phiB_ref_rAB = phiB_ref_rAB.factor().cancel()

# temperature derivatives at interface
dphiA_ref_dr_rAB = (sympy.diff(phiA_ref, r)).subs(r, rAB)
dphiB_ref_dr_rAB = (sympy.diff(phiB_ref, r)).subs(r, rAB)

# simplify expressions
dphiA_ref_dr_rAB = dphiA_ref_dr_rAB.factor().cancel()
dphiB_ref_dr_rAB = dphiB_ref_dr_rAB.factor().cancel()

# boundary conditions
eq1 = sympy.Eq(phiA_ref_rA, 1)
eq2 = sympy.Eq(phiB_ref_rB, 0)

# interface conditions
eq3 = sympy.Eq(phiA_ref_rAB, phiB_ref_rAB)
eq4 = sympy.Eq(-alphaA*dphiA_ref_dr_rAB, -alphaB*dphiB_ref_dr_rAB)

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
# diffA = diffA.factor().cancel()
# diffB = diffB.factor().cancel()

# source terms
fA = convA + diffA
fB = convB + diffB

# simplify expressions
# fA = fA.factor().cancel()
# fB = fB.factor().cancel()

#============================================
# OUTPUT
#============================================

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

# arguments list
args_list = [("x", x), ("y", y)]

# constants list
consts_list = [("rA", rA), ("rAB", rAB), ("rB", rB), ("betaAB_1", betaAB_1), ("betaAB_2", betaAB_2), \
                ("alphaA", alphaA), ("alphaB", alphaB), ("wA", wA), ("wB", wB)]

# parameters list
params_list = [("r", r), ("theta", theta)]
paramsA_list = [("r", r), ("theta", theta), ("aA", sol2[aA]), ("bA", sol2[bA])]
paramsB_list = [("r", r), ("theta", theta), ("aB", sol2[aB]), ("bB", sol2[bB])]

# functions list
funcs_list = [("RAB", RAB, args_list, params_list), ("nAB", nAB, args_list, params_list), \
                ("uA", uA, args_list, params_list), ("uB", uB, args_list, params_list), \
                ("phiA", phiA, args_list, paramsA_list), ("phiB", phiB, args_list, paramsB_list), \
                ("fA", fA, args_list, paramsA_list), ("fB", fB, args_list, paramsB_list)]

# generate code
outdir = "../codes"
name = "cht_02"
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
