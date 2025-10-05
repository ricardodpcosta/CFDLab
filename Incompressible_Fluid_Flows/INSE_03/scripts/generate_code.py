#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
CFDTestSuite | INSE_03
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
https://github.com/ricardodpcosta/CFDTestSuite

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
import math
import sympy
from helpers import *

#============================================
# SYMBOLIC VARIABLES
#============================================

# constants
rO, rI = sympy.symbols("rO rI", real=True, positive=True)
nu, rho = sympy.symbols("nu rho", real=True, positive=True)
u0, alpha, beta = sympy.symbols("u0 alpha beta", real=True)
pi = sympy.symbols("pi", real=True)

# coordinate system
r, theta = sympy.symbols("r theta", real=True)
x, y = sympy.symbols("x y", real=True)

#============================================
# EXACT SOLUTIONS
#============================================

# exact solutions
p=rho*rI*sympy.cos(alpha*theta/2)/r
u_r=u0*alpha*(rO-rI)*sympy.sin(beta*pi*(r-rI)/(rO-rI))*sympy.sin(alpha*theta/2)/(2*beta*pi*r)
u_theta=u0*sympy.cos(beta*pi*(r-rI)/(rO-rI))*sympy.cos(alpha*theta/2)

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
nu = 1.0
rho = 1.0
u0 = 1.0
alpha = 4.0
beta = 1.0
pi = math.pi

# arguments list
args_list = [("x", x), ("y", y)]

# constants list
consts_list = [("rO", rO), ("rI", rI), ("nu", nu), ("rho", rho), ("u0", u0), \
                ("alpha", alpha), ("beta", beta), ("pi", pi)]

# parameters list
params_list = [("r", r), ("theta", theta)]

# functions list
funcs_list = [("p", p, args_list, params_list),("u", u, args_list, params_list), \
                ("f", f, args_list, params_list), ("g", g, args_list, params_list)]

# generate code
outdir = "../codes"
name = "inse_03"
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
