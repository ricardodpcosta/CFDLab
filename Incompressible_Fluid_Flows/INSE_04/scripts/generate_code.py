#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
CFDLab | INSE_04
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
import math
import sympy
from helpers import *

#============================================
# SYMBOLIC VARIABLES
#============================================

# constants
rO, rI = sympy.symbols("rO rI", real=True, positive=True)
betaO_1, betaO_2, betaI_1, betaI_2 = sympy.symbols("betaO_1 betaO_2 betaI_1 betaI_2", real=True)
nu, rho = sympy.symbols("nu rho", real=True, positive=True)
u0, alpha = sympy.symbols("u0 alpha", real=True)
pi = sympy.symbols("pi", real=True)

# coordinate system
r, theta = sympy.symbols("r theta", real=True)
x, y = sympy.symbols("x y", real=True)

#============================================
# DOMAIN GEOMETRY
#============================================

# outer boundary radius
RO = rO*(1 + betaO_1*sympy.cos(betaO_2*theta))

# inner boundary radius
RI = rI*(1 + betaI_1*sympy.cos(betaI_2*theta))

# outer boundary normal vector
dRO_dtheta = sympy.diff(RO, theta)
nO_norm = sympy.sqrt(RO**2 + dRO_dtheta**2)
nO_r = RO/nO_norm
nO_theta = -dRO_dtheta/nO_norm

# simplify expressions
nO_r = nO_r.factor().cancel().trigsimp()
nO_theta = nO_theta.factor().cancel().trigsimp()

# inner boundary normal vector
dRI_dtheta = sympy.diff(RI, theta)
nI_norm = sympy.sqrt(RI**2 + dRI_dtheta**2)
nI_r = -RI/nI_norm
nI_theta = dRI_dtheta/nI_norm

# simplify expressions
nI_r = nI_r.factor().cancel().trigsimp()
nI_theta = nI_theta.factor().cancel().trigsimp()

# Cartesian unit basis
nO = sympy.Matrix([[sympy.cos(theta), -sympy.sin(theta)], \
                    [sympy.sin(theta), sympy.cos(theta)]]) \
                    *sympy.Matrix([nO_r, nO_theta])
nI = sympy.Matrix([[sympy.cos(theta), -sympy.sin(theta)], \
                    [sympy.sin(theta), sympy.cos(theta)]]) \
                    *sympy.Matrix([nI_r, nI_theta])

#============================================
# EXACT SOLUTIONS
#============================================

# exact solutions
p=rho*(r-RI/(RO-RI))*sympy.cos(alpha*theta)
u_r=u0*(r-RI/(RO-RI))*dRO_dtheta/nO_norm
u_theta=u0*(r-RI/(RO-RI))*RO/nO_norm

# Cartesian unit basis
u = sympy.Matrix([[sympy.cos(theta), -sympy.sin(theta)], \
                    [sympy.sin(theta), sympy.cos(theta)]]) \
                    *sympy.Matrix([u_r, u_theta])

#============================================
# SOURCE TERMS
#============================================

# convective terms
conv_r = u_r*sympy.diff(u_r, r) + u_theta*sympy.diff(u_r, theta)/r - u_theta**2/r
conv_theta = u_r*sympy.diff(u_theta, r) + u_theta*sympy.diff(u_theta, theta)/r + u_r*u_theta/r

# simplify expressions
conv_r = conv_r.factor().cancel().trigsimp()
conv_theta = conv_theta.factor().cancel().trigsimp()

# diffusive terms
diff_r = -nu*(sympy.diff(r*sympy.diff(u_r, r), r)/r \
            + sympy.diff(sympy.diff(u_r, theta), theta)/r**2 - u_r/r**2 \
            - 2*sympy.diff(u_theta, theta)/r**2)
diff_theta = -nu*(sympy.diff(r*sympy.diff(u_theta, r), r)/r \
            + sympy.diff(sympy.diff(u_theta, theta), theta)/r**2 - u_theta/r**2 \
            + 2*sympy.diff(u_r, theta)/r**2)

# simplify expressions
diff_r = diff_r.factor().cancel().trigsimp()
diff_theta = diff_theta.factor().cancel().trigsimp()

# pressure term
pres_r = sympy.diff(p, r)/rho
pres_theta = sympy.diff(p, theta)/(rho*r)

# simplify expressions
pres_r = pres_r.factor().cancel().trigsimp()
pres_theta = pres_theta.factor().cancel().trigsimp()

# source terms
f_r = conv_r + diff_r + pres_r
f_theta = conv_theta + diff_theta + pres_theta

# simplify expressions
f_r = f_r.factor().cancel().trigsimp()
f_theta = f_theta.factor().cancel().trigsimp()

# Cartesian unit basis
f = sympy.Matrix([[sympy.cos(theta), -sympy.sin(theta)], \
                    [sympy.sin(theta), sympy.cos(theta)]]) \
                    *sympy.Matrix([f_r, f_theta])

#============================================
# VELOCITY DIVERGENCE
#============================================

# divergence terms
div_r = sympy.diff(r*u_r, r)/r
div_theta = sympy.diff(u_theta, theta)/r

# simplify expressions
div_r = div_r.factor().cancel().trigsimp()
div_theta = div_theta.factor().cancel().trigsimp()

# velocity divergence
g = div_r + div_theta

# simplify expressions
g = g.factor().cancel().trigsimp()

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
rO = 1.0
rI = 0.5
betaO_1 = 0.1
betaO_2 = 8.0
betaI_1 = 0.1
betaI_2 = 8.0
nu = 1.0
rho = 1.0
u0 = 1.0
alpha = 4.0
pi = math.pi

# arguments list
args_list = [("x", x), ("y", y)]

# constants list
consts_list = [("rO", rO), ("rI", rI), ("betaO_1", betaO_1), ("betaO_2", betaO_2), \
                ("betaI_1", betaI_1), ("betaI_2", betaI_2), ("nu", nu), ("rho", rho), \
                ("u0", u0), ("alpha", alpha), ("beta", beta), ("pi", pi)]

# parameters list
params_list = [("r", r), ("theta", theta)]

# functions list
funcs_list = [("RO", RO, args_list, params_list), ("RI", RI, args_list, params_list), \
                ("nO", nO, args_list, params_list), ("nI", nI, args_list, params_list), \
                ("p", p, args_list, params_list),("u", u, args_list, params_list), \
                ("f", f, args_list, params_list), ("g", g, args_list, params_list)]

# generate code
outdir = "../codes"
name = "inse_04"
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
