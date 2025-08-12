#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
CFD-BenchLab | CHT_01 | Code Generator
===============================================================================

Description:
    Generates code for the analytical solution, coefficients and source terms
    for the CHT_01 test case in multiple target languages: C++, Fortran, Octave,
    (Matlab) and Python (NumPy). Outputs one file per expression/language.

Author:
    Ricardo Costa (rcosta@dep.uminho.pt)

License:
    MIT License (see LICENSE file for details)

Repository:
    https://github.com/ricardodpcosta/CFD-TestSuite

Dependencies:
    pip install sympy

Usage:
    python generate_code.py
===============================================================================
"""

# Import modules
import os
import sympy
from helpers import *

# ----------------------------------------
# 1. Define symbolic variables
# ----------------------------------------

# User-defined parameters
nA, nB = sympy.symbols("nA nB", real=True)
kA, kB = sympy.symbols("kA kB", positive=True)
wA, wB = sympy.symbols("wA wB", real=True)
rA, rAB, rB = sympy.symbols("rA rAB rB", positive=True)

# Coordinate system variables
r, theta = sympy.symbols("r theta", real=True, positive=True)

# Solution parameters
aA, bA, aB, bB = sympy.symbols("aA bA aB bB", real=True)

# ----------------------------------------
# 2. Define manufactured solutions
# ----------------------------------------

# Manufactured solutions
phiA = (aA * sympy.log(r) + bA) * sympy.cos(nA * theta)
phiB = (aB * sympy.log(r) + bB) * sympy.cos(nB * theta)

# ----------------------------------------
# 3. Compute solution parameters
# ----------------------------------------

# Dirichlet boundary conditions
eq1 = sympy.Eq(phiA.subs(r, rA), sympy.cos(nA * theta))
eq2 = sympy.Eq(phiB.subs(r, rB), 0)

# Solution continuity at interface
eq3 = sympy.Eq(phiA.subs(r, rAB), phiB.subs(r, rAB))

# Flux conservation at interface
dphiA_dr = sympy.diff(phiA, r)
dphiB_dr = sympy.diff(phiB, r)
eq4 = sympy.Eq(-kA * dphiA_dr.subs(r, rAB), kB * dphiB_dr.subs(r, rAB))

# Solve for coefficients
sol = sympy.solve([eq1, eq2, eq3, eq4], (aA, bA, aB, bB), dict=True)
if not sol:
    raise RuntimeError("Could not solve for coefficients symbolically.")
sol = sol[0]

# Substitute into manufactured solutions
phiA = sympy.simplify(phiA.subs(sol))
phiB = sympy.simplify(phiB.subs(sol))

# ----------------------------------------
# 4. Compute source terms
# ----------------------------------------

# Laplacian terms
lap_phiA = (1/r) * sympy.diff(r * sympy.diff(phiA, r), r) + (1/r**2) * sympy.diff(sympy.diff(phiA, theta), theta)
lap_phiB = (1/r) * sympy.diff(r * sympy.diff(phiB, r), r) + (1/r**2) * sympy.diff(sympy.diff(phiB, theta), theta)

# Convective terms
u_theta_A = wA * r
u_theta_B = wB * r
conv_A = (u_theta_A / r) * sympy.diff(phiA, theta)
conv_B = (u_theta_B / r) * sympy.diff(phiB, theta)

# Source-terms
fA = sympy.simplify(conv_A - kA * lap_phiA)
fB = sympy.simplify(conv_B - kB * lap_phiB)

# ----------------------------------------
# 5. Write symbolic expressions
# ----------------------------------------

# Output directory
outdir = "../symbolic"
os.makedirs(outdir, exist_ok=True)

# Arguments list for functions
arg_syms = [(r, "r"), (theta, "theta"), (kA, "kA"), (kB, "kB"),
            (wA, "wA"), (wB, "wB"), (nA, "nA"), (nB, "nB"),
            (rA, "rA"), (rAB, "rAB"), (rB, "rB")]

# Symbolic variables to write
items = {"aA": sol[aA], "bA": sol[bA], "aB": sol[aB], "bB": sol[bB],
    "phiA": phiA, "phiB": phiB, "fA": fA, "fB": fB}

# ----------------------------------------
# 7. Generate code for coefficients, phiA, phiB, fA, fB
# ----------------------------------------

# For each item, produce implementations in each language
for name, expr in items.items():
    # C++
    try:
        c_code = write_c_function(name, expr, arg_syms)
        write_file(os.path.join(outdir, f"{name}.cpp"), c_code + "\n")
    except Exception as e:
        print("C++ generation failed for", name, ":", e)

    # Fortran
    try:
        f_code = write_fortran_function(name, expr, arg_syms)
        write_file(os.path.join(outdir, f"{name}.f90"), f_code + "\n")
    except Exception as e:
        print("Fortran generation failed for", name, ":", e)

    # Octave
    try:
        m_code = write_octave_function(name, expr, arg_syms)
        write_file(os.path.join(outdir, f"{name}.m"), m_code + "\n")
    except Exception as e:
        print("Octave generation failed for", name, ":", e)

    # Python (NumPy)
    try:
        py_code = write_python_function(name, expr, arg_syms)
        write_file(os.path.join(outdir, f"{name}.py"), py_code + "\n")
    except Exception as e:
        print("Python generation failed for", name, ":", e)

print("\nGeneration complete. Files are in:", outdir)
