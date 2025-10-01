#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
CFDLab | INSE_01
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
import math
import sympy
from helpers import *

#============================================
# SYMBOLIC VARIABLES
#============================================

# constants
L, T = sympy.symbols("L T", real=True, positive=True)
nu, rho = sympy.symbols("nu rho", real=True, positive=True)
u0, alpha = sympy.symbols("u0 alpha", real=True)
pi = sympy.symbols("pi", real=True)

# coordinate system
x, y, t = sympy.symbols("x y t", real=True)

#============================================
# EXACT SOLUTIONS
#============================================

# exact solutions
p = (rho*u0**2/4)*sympy.exp(-16*pi**2*alpha**2*nu*t/L**2) \
        *(sympy.cos(4*pi*alpha*x/L) + sympy.cos(4*pi*alpha*y/L))
u_x = u0*sympy.exp(-8*pi**2*alpha**2*nu*t/L**2) \
        *sympy.sin(2*pi*alpha*x/L)*sympy.cos(2*pi*alpha*y/L)
u_y = -u0*sympy.exp(-8*pi**2*alpha**2*nu*t/L**2) \
        *sympy.cos(2*pi*alpha*x/L)*sympy.sin(2*pi*alpha*y/L)
u = sympy.Matrix([u_x, u_y])

#============================================
# SOURCE TERMS
#============================================

# rate terms
rate_x = sympy.diff(u_x, t)
rate_y = sympy.diff(u_y, t)

# simplify expressions
rate_x = rate_x.factor().cancel().trigsimp()
rate_y = rate_y.factor().cancel().trigsimp()

# convective terms
conv_x = u.dot(sympy.Matrix([sympy.diff(u_x, x), sympy.diff(u_x, y)]))
conv_y = u.dot(sympy.Matrix([sympy.diff(u_y, x), sympy.diff(u_y, y)]))

# simplify expressions
conv_x = conv_x.factor().cancel().trigsimp()
conv_y = conv_y.factor().cancel().trigsimp()

# diffusive terms
diff_x = -nu*(sympy.diff(sympy.diff(u_x, x), x) + sympy.diff(sympy.diff(u_x, y), y))
diff_y = -nu*(sympy.diff(sympy.diff(u_y, x), x) + sympy.diff(sympy.diff(u_y, y), y))

# simplify expressions
diff_x = diff_x.factor().cancel().trigsimp()
diff_y = diff_y.factor().cancel().trigsimp()

# pressure term
pres_x = sympy.diff(p, x)/rho
pres_y = sympy.diff(p, y)/rho

# simplify expressions
pres_x = pres_x.factor().cancel().trigsimp()
pres_y = pres_y.factor().cancel().trigsimp()

# source terms
f_x = rate_x + conv_x + diff_x + pres_x
f_y = rate_y + conv_y + diff_y + pres_y

# simplify expressions
f_x = f_x.factor().cancel().trigsimp()
f_y = f_y.factor().cancel().trigsimp()
f = sympy.Matrix([f_x, f_y])

#============================================
# VELOCITY DIVERGENCE
#============================================

# divergence terms
div_x = sympy.diff(u_x, x)
div_y = sympy.diff(u_y, y)

# simplify expressions
div_x = div_x.factor().cancel().trigsimp()
div_y = div_y.factor().cancel().trigsimp()

# velocity divergence
g = div_x + div_y

# simplify expressions
g = g.factor().cancel().trigsimp()

#============================================
# OUTPUT
#============================================

# output directory
outdir = "../codes"
os.makedirs(outdir, exist_ok=True)

# constant parameters values
L = 1.0
T = 1.0
nu = 1.0
rho = 1.0
u0 = 1.0
alpha = 2.0
pi = math.pi

# arguments list
args_list = [("x", x), ("y", y)]

# constants list
consts_list = [("L", L), ("T", T), ("nu", nu), ("rho", rho), ("u0", u0), \
                ("alpha", alpha), ("pi", pi)]

# parameters list
params_list = []

# functions list
funcs_list = [("p", p, args_list, params_list),("u", u, args_list, params_list), \
                ("f", f, args_list, params_list), ("g", g, args_list, params_list)]

# generate code
outdir = "../codes"
name = "inse_01"
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
