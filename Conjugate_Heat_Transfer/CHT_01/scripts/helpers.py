#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
CFD-BenchLab | Helpers
===============================================================================

Description:
    Utility functions for code generation in multiple programming languages:
    C/C++, Fortran, Octave/Matlab, and Python.
    Includes code formatting and line-wrapping helpers to keep generated source
    code within a configurable indent and line width.
    This module is intended to be imported by the main code generation script
    (generate_code.py).

Author:
    Ricardo Costa (rcosta@dep.uminho.pt)

License:
    MIT License (see LICENSE file for details)

Repository:
    https://github.com/ricardodpcosta/CFD-TestSuite

Dependencies:
    Python (version >= 3.9)
    Sympy (version >= 1.6)

Usage:
    import helpers
===============================================================================
"""

# Import modules
import re
import textwrap
import sympy

# Import specific printers
try:
    from sympy.printing.c import ccode
    from sympy.printing.fortran import fcode
    from sympy.printing.octave import octave_code
    from sympy.printing.pycode import pycode
except Exception:
    raise RuntimeError("Required SymPy printers not available. Ensure sympy >= 1.6 is installed.")

# Write contens to file
def write_file(path, contents):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(contents)
    print("Wrote", path)

# Write C/C++ variables
def write_cpp_variables(vars):
    """
    Generate C/C++ variables definition from a symbolic expression.
    """
    decl_lines = []
    for i, (varname, varexpr) in enumerate(vars):
        cexpr = str(varexpr)
        cexpr = cexpr.strip()
        cexpr = f"double {varname} = {cexpr};"
        decl_lines.append(cexpr)
    decl = "\n".join((line if i == 0 else "        " + line) for i, line in enumerate(decl_lines))
    code = textwrap.dedent(f"""
        {decl}
    """).strip()
    return code

# Write fortran variables
def write_fortran_variables(vars):
    """
    Generate Fortran variables definition from a symbolic expression.
    """
    decl_lines = []
    for i, (varname, varexpr) in enumerate(vars):
        cexpr = str(varexpr)
        cexpr = cexpr.strip()
        cexpr = f"real(8), parameter :: {varname} = {cexpr}"
        decl_lines.append(cexpr)
    decl = "\n".join((line if i == 0 else "        " + line) for i, line in enumerate(decl_lines))
    code = textwrap.dedent(f"""
        {decl}
    """).strip()
    return code

# Write Octave/Matlab variables
def write_octave_variables(vars):
    """
    Generate Octave/Matlab variables definition from a symbolic expression.
    """
    decl_lines = []
    for i, (varname, varexpr) in enumerate(vars):
        cexpr = str(varexpr)
        cexpr = cexpr.strip()
        cexpr = f"{varname} = {cexpr};"
        decl_lines.append(cexpr)
    decl = "\n".join((line if i == 0 else "        " + line) for i, line in enumerate(decl_lines))
    code = textwrap.dedent(f"""
        {decl}
    """).strip()
    return code

# Write Python variables
def write_python_variables(vars):
    """
    Generate Python variables definition from a symbolic expression.
    """
    decl_lines = []
    for i, (varname, varexpr) in enumerate(vars):
        cexpr = str(varexpr)
        cexpr = cexpr.strip()
        cexpr = f"{varname} = {cexpr}"
        decl_lines.append(cexpr)
    decl = "\n".join((line if i == 0 else "        " + line) for i, line in enumerate(decl_lines))
    code = textwrap.dedent(f"""
        {decl}
    """).strip()
    return code

# Write C/C++ function
def write_cpp_function(name, expr, args, pars):
    """
    Generate a C/C++ function definition from a symbolic expression.
    """
    arglist = ", ".join(f"double {argname}" for (argname, _) in args)
    decl_lines = []
    for i, (parname, parexpr) in enumerate(pars):
        cexpr = ccode(sympy.simplify(sympy.trigsimp(parexpr)), assign_to=None)
        cexpr = cexpr.replace("\\\\\n", "")
        cexpr = re.sub(r" {2,}", " ", cexpr)
        cexpr = cexpr.strip()
        cexpr = wrap_code_line(f"double {parname} = {cexpr};", width=72, indent="    ",continuation=" \\")
        decl_lines.extend(cexpr)
    decl = "\n".join((line if i == 0 else "        " + line) for i, line in enumerate(decl_lines))
    cexpr = ccode(sympy.simplify(sympy.trigsimp(expr)), assign_to=None)
    cexpr = cexpr.replace("\\\\\n", "")
    cexpr = re.sub(r" {2,}", " ", cexpr)
    cexpr = cexpr.strip()
    cexpr = "\n".join(wrap_code_line(f"return {cexpr}", width=72, indent="    ",continuation=" \\"))
    code = textwrap.dedent(f"""
    double {name}({arglist}) {{
        {decl}
        {cexpr};
    }}
    """).strip()
    return code

# Write Fortran function
def write_fortran_function(name, expr, args, pars):
    """
    Generate a Fortran function definition from a symbolic expression.
    """
    argnames = ", ".join(argname for (argname, _) in args)
    decl_lines = [f"real(8), intent(in) :: {argname}" for (argname, _) in args]
    for i, (parname, parexpr) in enumerate(pars):
        fexpr = fcode(sympy.simplify(sympy.trigsimp(parexpr)), assign_to=None, source_format='free')
        fexpr = fexpr.replace("&\n", "")
        fexpr = re.sub(r" {2,}", " ", fexpr)
        fexpr = fexpr.strip()
        fexpr = wrap_code_line(f"real(8) :: {parname} = {fexpr}", width=72, indent="    ",continuation=" &")
        decl_lines.extend(fexpr)
    decl = "\n".join((line if i == 0 else "        " + line) for i, line in enumerate(decl_lines))
    fexpr = fcode(sympy.simplify(sympy.trigsimp(expr)), assign_to=None, source_format='free')
    fexpr = fexpr.replace("&\n", "")
    fexpr = re.sub(r" {2,}", " ", fexpr)
    fexpr = fexpr.strip()
    fexpr = "\n".join(wrap_code_line(f"res = {fexpr}", width=72, indent="            ",continuation=" &"))
    code = textwrap.dedent(f"""
    function {name}({argnames}) result(res)
        {decl}
        real(8) :: res
        {fexpr}
    end function {name}
    """).strip()
    return code

# Write Matlab function
def write_octave_function(name, expr, args, pars):
    """
    Generate an Octave/Matlab function definition from a symbolic expression.
    """
    arglist = ", ".join(argname for (argname, _) in args)
    decl_lines = []
    for i, (parname, parexpr) in enumerate(pars):
        mexpr = octave_code(sympy.simplify(sympy.trigsimp(parexpr)), assign_to=None)
        mexpr = mexpr.replace("...\n", "")
        mexpr = re.sub(r" {2,}", " ", mexpr)
        mexpr = mexpr.strip()
        mexpr = wrap_code_line(f"{parname} = {mexpr};", width=72, indent="    ",continuation=" ...")
        decl_lines.extend(mexpr)
    decl = "\n".join((line if i == 0 else "        " + line) for i, line in enumerate(decl_lines))
    mexpr = octave_code(sympy.simplify(sympy.trigsimp(expr)), assign_to=None)
    mexpr = mexpr.replace("...\n", "")
    mexpr = re.sub(r" {2,}", " ", mexpr)
    mexpr = mexpr.strip()
    mexpr = "\n".join(wrap_code_line(f"res = {mexpr}", width=72, indent="            ",continuation=" ..."))
    code = textwrap.dedent(f"""
    function res = {name}({arglist})
        {decl}
        {mexpr};
    end
    """).strip()
    return code

# Write Python function
def write_python_function(name, expr, args, pars):
    """
    Generate a Python function definition from a symbolic expression.
    """
    arglist = ", ".join(argname for (argname, _) in args)
    decl_lines = []
    for i, (parname, parexpr) in enumerate(pars):
        pexpr = pycode(sympy.simplify(sympy.trigsimp(parexpr)))
        pexpr = pexpr.replace("\\\\\n", "")
        pexpr = re.sub(r" {2,}", " ", pexpr)
        pexpr = pexpr.strip()
        pexpr = wrap_code_line(f"{parname} = {pexpr}", width=72, indent="    ",continuation="")
        decl_lines.extend(pexpr)
    decl = "\n".join((line if i == 0 else "        " + line) for i, line in enumerate(decl_lines))
    pexpr = pycode(sympy.simplify(sympy.trigsimp(expr)))
    pexpr = pexpr.replace("\\\\\n", "")
    pexpr = re.sub(r" {2,}", " ", pexpr)
    pexpr = pexpr.strip()
    pexpr = "\n".join(wrap_code_line(f"return {pexpr}", width=72, indent="            ",continuation=""))
    code = textwrap.dedent(f"""
    def {name}({arglist}):
        {decl}
        {pexpr}
    """).strip()
    return code

# Wrap code line
def wrap_code_line(line, width=72, indent="", continuation="\\"):
    """
    Wrap a code line to a given width, breaking at operators (+, -, *, /) or spaces.
    Adds trailing characters for line continuation with the given continuation string.
    Indents continuation lines with the given indent string.
    """
    if len(line) <= width:
        return [line]
    parts = []
    while len(line) > width:
        break_pos = max(line.rfind(op, 0, width) for op in ['+', '-', '*', '/'])
        if break_pos == -1:
            break_pos = line.rfind(' ', 0, width)
        if break_pos == -1:
            break_pos = width
        parts.append(line[:break_pos].rstrip() + continuation)
        line = indent + line[break_pos:].lstrip()
    parts.append(line)
    return parts
