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
    SymPy (version >= 1.6)

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
def write_cpp_variables(vars_list):
    """
    Generate C/C++ variables definition from a symbolic expression.
    """
    decl_lines = ["// Global variables"]
    for i, (varname, varexpr) in enumerate(vars_list):
        cexpr = str(varexpr)
        cexpr = cexpr.strip()
        cexpr = f"double {varname} = {cexpr};"
        decl_lines.append(cexpr)
    decl_lines[1:] = [" "*8 + line for line in decl_lines[1:]]
    decl = "\n".join(decl_lines)
    code = textwrap.dedent(f"""
        {decl}
    """).strip()
    return code

# Write Fortran variables
def write_fortran_variables(vars_list):
    """
    Generate Fortran variables definition from a symbolic expression.
    """
    decl_lines = ["! Global variables"]
    for i, (varname, varexpr) in enumerate(vars_list):
        fexpr = str(varexpr)
        fexpr = fexpr.strip()
        fexpr = f"real(8), parameter :: {varname} = {fexpr}"
        decl_lines.append(fexpr)
    decl_lines[1:] = [" "*8 + line for line in decl_lines[1:]]
    decl = "\n".join(decl_lines)
    code = textwrap.dedent(f"""
        {decl}
    """).strip()
    return code

# Write Octave/Matlab variables
def write_octave_variables(vars_list):
    """
    Generate Octave/Matlab variables definition from a symbolic expression.
    """
    decl_lines = ["% Global variables"]
    for i, (varname, varexpr) in enumerate(vars_list):
        mexpr = str(varexpr)
        mexpr = mexpr.strip()
        mexpr = f"global {varname} = {mexpr};"
        decl_lines.append(mexpr)
    decl_lines[1:] = [" "*8 + line for line in decl_lines[1:]]
    decl = "\n".join(decl_lines)
    code = textwrap.dedent(f"""
        {decl}
    """).strip()
    return code

# Write Python variables
def write_python_variables(vars_list):
    """
    Generate Python variables definition from a symbolic expression.
    """
    decl_lines = ["# Global variables"]
    for i, (varname, varexpr) in enumerate(vars_list):
        pexpr = str(varexpr)
        pexpr = pexpr.strip()
        pexpr = f"{varname} = {pexpr}"
        decl_lines.append(pexpr)
    decl_lines[1:] = [" "*8 + line for line in decl_lines[1:]]
    decl = "\n".join(decl_lines)
    code = textwrap.dedent(f"""
        {decl}
    """).strip()
    return code

# Write C/C++ function
def write_cpp_function(name, expr, args_list, pars_list):
    """
    Generate a C/C++ function definition from a symbolic expression.
    """
    if isinstance(expr, sympy.Matrix):
        return write_cpp_vector_function(name, expr, args_list, pars_list)
    else:
        return write_cpp_scalar_function(name, expr, args_list, pars_list)

# Write Fortran function
def write_fortran_function(name, expr, args_list, pars_list):
    """
    Generate a Fortran function definition from a symbolic expression.
    """
    if isinstance(expr, sympy.Matrix):
        return write_fortran_vector_function(name, expr, args_list, pars_list)
    else:
        return write_fortran_scalar_function(name, expr, args_list, pars_list)

# Write Octave/Matlab function
def write_octave_function(name, expr, args_list, vars_list, pars_list):
    """
    Generate a Octave/Matlab function definition from a symbolic expression.
    """
    if isinstance(expr, sympy.Matrix):
        return write_octave_vector_function(name, expr, args_list, vars_list, pars_list)
    else:
        return write_octave_scalar_function(name, expr, args_list, vars_list, pars_list)

# Write Python function
def write_python_function(name, expr, args_list, pars_list):
    """
    Generate a Python function definition from a symbolic expression.
    """
    if isinstance(expr, sympy.Matrix):
        return write_python_vector_function(name, expr, args_list, pars_list)
    else:
        return write_python_scalar_function(name, expr, args_list, pars_list)

# Write C/C++ scalar function
def write_cpp_scalar_function(name, expr, args_list, pars_list):
    """
    Generate a C/C++ function definition from a scalar symbolic expression.
    """
    argnames = ", ".join(f"double {argname}" for (argname, _) in args_list)
    decl_lines = []
    for i, (parname, parexpr) in enumerate(pars_list):
        cexpr = ccode(sympy.simplify(sympy.trigsimp(parexpr)), assign_to=None)
        cexpr = cexpr.replace("\\\\\n", "")
        cexpr = re.sub(r" {2,}", " ", cexpr)
        cexpr = cexpr.strip()
        cexpr = wrap_code_line(f"double {parname} = {cexpr};", width=100, indent=" "*4,continuation=" \\")
        decl_lines.extend(cexpr)
    decl_lines[1:] = [" "*8 + line for line in decl_lines[1:]]
    decl = "\n".join(decl_lines)
    cexpr = ccode(sympy.simplify(sympy.trigsimp(expr)), assign_to=None)
    cexpr = cexpr.replace("\\\\\n", "")
    cexpr = re.sub(r" {2,}", " ", cexpr)
    cexpr = cexpr.strip()
    cexpr = wrap_code_line(f"dobule res = {cexpr};", width=100, indent=" "*12,continuation=" \\")
    cexpr.append(" "*8 + "return res;")
    comp = "\n".join(cexpr)
    code = textwrap.dedent(f"""
    // Function {name}
    inline double {name}({argnames}) {{
        {decl}
        {comp}
    }}
    """).strip()
    return code

# Write Fortran scalar function
def write_fortran_scalar_function(name, expr, args_list, pars_list):
    """
    Generate a Fortran function definition from a scalar symbolic expression.
    """
    argnames = ", ".join(argname for (argname, _) in args_list)
    decl_lines = [f"real(8), intent(in) :: {argname}" for (argname, _) in args_list]
    decl_lines.append("real(8) :: res")
    decl_lines.extend([f"real(8) :: {parname}" for (parname, _) in pars_list])
    for i, (parname, parexpr) in enumerate(pars_list):
        fexpr = fcode(sympy.simplify(sympy.trigsimp(parexpr)), assign_to=None, source_format="free")
        fexpr = fexpr.replace("&\n", "")
        fexpr = re.sub(r" {2,}", " ", fexpr)
        fexpr = fexpr.strip()
        fexpr = wrap_code_line(f"{parname} = {fexpr}", width=100, indent=" "*4,continuation=" &")
        decl_lines.extend(fexpr)
    decl_lines[1:] = [" "*8 + line for line in decl_lines[1:]]
    decl = "\n".join(decl_lines)
    fexpr = fcode(sympy.simplify(sympy.trigsimp(expr)), assign_to=None, source_format="free")
    fexpr = fexpr.replace("&\n", "")
    fexpr = re.sub(r" {2,}", " ", fexpr)
    fexpr = fexpr.strip()
    comp = "\n".join(wrap_code_line(f"res = {fexpr}", width=100, indent=" "*12,continuation=" &"))
    code = textwrap.dedent(f"""
    ! Function {name}
    function {name}({argnames}) result(res)
        {decl}
        {comp}
    end function {name}
    """).strip()
    return code

# Write Matlab scalar function
def write_octave_scalar_function(name, expr, args_list, vars_list, pars_list):
    """
    Generate an Octave/Matlab function definition from a scalar symbolic expression.
    """
    argnames = ", ".join(argname for (argname, _) in args_list)
    decl_lines = ["global " + varname + ";" for (varname, _) in vars_list]
    for i, (parname, parexpr) in enumerate(pars_list):
        mexpr = octave_code(sympy.simplify(sympy.trigsimp(parexpr)), assign_to=None)
        mexpr = mexpr.replace("...\n", "")
        mexpr = re.sub(r" {2,}", " ", mexpr)
        mexpr = mexpr.strip()
        mexpr = wrap_code_line(f"{parname} = {mexpr};", width=100, indent=" "*4,continuation=" ...")
        decl_lines.extend(mexpr)
    decl_lines[1:] = [" "*8 + line for line in decl_lines[1:]]
    decl = "\n".join(decl_lines)
    mexpr = octave_code(sympy.simplify(sympy.trigsimp(expr)), assign_to=None)
    mexpr = mexpr.replace("...\n", "")
    mexpr = re.sub(r" {2,}", " ", mexpr)
    mexpr = mexpr.strip()
    mexpr = wrap_code_line(f"res = {mexpr};", width=100, indent=" "*12,continuation=" ...")
    comp = "\n".join(mexpr)
    code = textwrap.dedent(f"""
    % Function {name}
    function res = {name}({argnames})
        {decl}
        {comp}
    end
    """).strip()
    return code

# Write Python scalar function
def write_python_scalar_function(name, expr, args_list, pars_list):
    """
    Generate a Python function definition from a scalar symbolic expression.
    """
    argnames = ", ".join(argname for (argname, _) in args_list)
    decl_lines = []
    for i, (parname, parexpr) in enumerate(pars_list):
        pexpr = pycode(sympy.simplify(sympy.trigsimp(parexpr)))
        pexpr = pexpr.replace("\n", "")
        pexpr = re.sub(r" {2,}", " ", pexpr)
        pexpr = pexpr.strip()
        pexpr = wrap_code_line(f"{parname} = {pexpr}", width=100, indent=" "*4,continuation="")
        decl_lines.extend(pexpr)
    decl_lines[1:] = [" "*8 + line for line in decl_lines[1:]]
    decl = "\n".join(decl_lines)
    pexpr = pycode(sympy.simplify(sympy.trigsimp(expr)))
    pexpr = pexpr.replace("\n", "")
    pexpr = re.sub(r" {2,}", " ", pexpr)
    pexpr = pexpr.strip()
    pexpr = wrap_code_line(f"res = {pexpr}", width=100, indent=" "*12,continuation="")
    pexpr.append(" "*8 + "return res")
    comp = "\n".join(pexpr)
    code = textwrap.dedent(f"""
    # Function {name}
    def {name}({argnames}):
        {decl}
        {comp}
    """).strip()
    return code

# Write C/C++ vector function
def write_cpp_vector_function(name, expr, args_list, pars_list):
    """
    Generate a C/C++ function definition from a vector symbolic expression.
    """
    argnames = ", ".join(f"double {argname}" for (argname, _) in args_list)
    argnames += ", double res[{}]".format(len(expr))
    decl_lines = []
    for i, (parname, parexpr) in enumerate(pars_list):
        cexpr = ccode(sympy.simplify(sympy.trigsimp(parexpr)), assign_to=None)
        cexpr = cexpr.replace("\\\\\n", "")
        cexpr = re.sub(r" {2,}", " ", cexpr)
        cexpr = cexpr.strip()
        cexpr = wrap_code_line(f"double {parname} = {cexpr};", width=100, indent=" "*4,continuation=" \\")
        decl_lines.extend(cexpr)
    decl_lines[1:] = [" "*8 + line for line in decl_lines[1:]]
    decl = "\n".join(decl_lines)
    comp_lines = []
    for i, compexpr in enumerate(expr):
        cexpr = ccode(sympy.simplify(sympy.trigsimp(compexpr)), assign_to=None)
        cexpr = cexpr.replace("\\\\\n", "")
        cexpr = re.sub(r" {2,}", " ", cexpr)
        cexpr = cexpr.strip()
        cexpr = wrap_code_line(f"res[{i}] = {cexpr}", width=100, indent=" "*4,continuation=" \\")
        cexpr = "\n".join(cexpr)
        comp_lines.append(cexpr)
    comp_lines[1:] = [" "*8 + line for line in comp_lines[1:]]
    comp = "\n".join(comp_lines)
    code = textwrap.dedent(f"""
    // Function {name}
    inline void {name}({argnames}) {{
        {decl}
        {comp}
    }}
    """).strip()
    return code

# Write Fortran vector function
def write_fortran_vector_function(name, expr, args_list, pars_list):
    """
    Generate a Fortran function definition from a vector symbolic expression.
    """
    argnames = ", ".join(argname for (argname, _) in args_list)
    argnames += ", res"
    decl_lines = [f"real(8), intent(in) :: {argname}" for (argname, _) in args_list]
    decl_lines.append("real(8), intent(out) :: res({})".format(len(expr)))
    decl_lines.extend([f"real(8) :: {parname}" for (parname, _) in pars_list])
    for i, (parname, parexpr) in enumerate(pars_list):
        fexpr = fcode(sympy.simplify(sympy.trigsimp(parexpr)), assign_to=None, source_format="free")
        fexpr = fexpr.replace("&\n", "")
        fexpr = re.sub(r" {2,}", " ", fexpr)
        fexpr = fexpr.strip()
        fexpr = wrap_code_line(f"{parname} = {fexpr}", width=100, indent=" "*4,continuation=" &")
        decl_lines.extend(fexpr)
    decl_lines[1:] = [" "*8 + line for line in decl_lines[1:]]
    decl = "\n".join(decl_lines)
    comp_lines = []
    for i, compexpr in enumerate(expr):
        fexpr = fcode(sympy.simplify(sympy.trigsimp(compexpr)), assign_to=None, source_format="free")
        fexpr = fexpr.replace("&\n", "")
        fexpr = re.sub(r" {2,}", " ", fexpr)
        fexpr = fexpr.strip()
        fexpr = wrap_code_line(f"res({i+1}) = {fexpr}", width=100, indent=" "*4,continuation=" &")
        fexpr = "\n".join(fexpr)
        comp_lines.append(fexpr)
    comp_lines[1:] = [" "*8 + line for line in comp_lines[1:]]
    comp = "\n".join(comp_lines)
    code = textwrap.dedent(f"""
    ! Subroutine {name}
    subroutine {name}({argnames})
        {decl}
        {comp}
    end subroutine {name}
    """).strip()
    return code

# Write Octave/Matlab vector function
def write_octave_vector_function(name, expr, args_list, vars_list, pars_list):
    """
    Generate a Octave/Matlab function definition from a vector symbolic expression.
    """
    argnames = ", ".join(argname for (argname, _) in args_list)
    decl_lines = ["global " + varname + ";" for (varname, _) in vars_list]
    for i, (parname, parexpr) in enumerate(pars_list):
        mexpr = octave_code(sympy.simplify(sympy.trigsimp(parexpr)), assign_to=None)
        mexpr = mexpr.replace("...\n", "")
        mexpr = re.sub(r" {2,}", " ", mexpr)
        mexpr = mexpr.strip()
        mexpr = wrap_code_line(f"{parname} = {mexpr};", width=100, indent=" "*4,continuation=" ...")
        decl_lines.extend(mexpr)
    decl_lines[1:] = [" "*8 + line for line in decl_lines[1:]]
    decl = "\n".join(decl_lines)
    comp_lines = []
    for i, compexpr in enumerate(expr):
        mexpr = octave_code(sympy.simplify(sympy.trigsimp(compexpr)), assign_to=None)
        mexpr = mexpr.replace("...\n", "")
        mexpr = re.sub(r" {2,}", " ", mexpr)
        mexpr = mexpr.strip()
        mexpr = wrap_code_line(f"res({i+1}) = {mexpr};", width=100, indent=" "*4,continuation=" ...")
        mexpr = "\n".join(mexpr)
        comp_lines.append(mexpr)
    comp_lines[1:] = [" "*8 + line for line in comp_lines[1:]]
    comp = "\n".join(comp_lines)
    code = textwrap.dedent(f"""
    % Function {name}
    function res = {name}({argnames})
        {decl}
        {comp}
    end
    """).strip()
    return code

# Write Python vector function
def write_python_vector_function(name, expr, args_list, pars_list):
    """
    Generate a Python function definition from a vector symbolic expression.
    """
    argnames = ", ".join(argname for (argname, _) in args_list)
    decl_lines = []
    for i, (parname, parexpr) in enumerate(pars_list):
        pexpr = pycode(sympy.simplify(sympy.trigsimp(parexpr)))
        pexpr = pexpr.replace("\n", "")
        pexpr = re.sub(r" {2,}", " ", pexpr)
        pexpr = pexpr.strip()
        pexpr = wrap_code_line(f"{parname} = {pexpr}", width=100, indent=" "*4,continuation="")
        decl_lines.extend(pexpr)
    decl_lines[1:] = [" "*8 + line for line in decl_lines[1:]]
    decl = "\n".join(decl_lines)
    comp_lines = [f"res = [0.0]*{len(expr)}"]
    for i, compexpr in enumerate(expr):
        pexpr = pycode(sympy.simplify(sympy.trigsimp(compexpr)))
        pexpr = pexpr.replace("\n", "")
        pexpr = re.sub(r" {2,}", " ", pexpr)
        pexpr = pexpr.strip()
        pexpr = wrap_code_line(f"res[{i}] = {pexpr}", width=100, indent=" "*4,continuation="")
        pexpr = "\n".join(pexpr)
        comp_lines.append(pexpr)
    comp_lines.append("return res")
    comp_lines[1:] = [" "*8 + line for line in comp_lines[1:]]
    comp = "\n".join(comp_lines)
    code = textwrap.dedent(f"""
    # Function {name}
    def {name}({argnames}):
        {decl}
        {comp}
    """).strip()
    return code

# Wrap code line
def wrap_code_line(line, width=100, indent="", continuation="\\"):
    """
    Wrap a code line to a given width, breaking at operators (+, -, *, /) or spaces.
    Adds trailing characters for line continuation with the given continuation string.
    Indents continuation lines with the given indent string.
    """
    if len(line) <= width:
        return [line]
    parts = []
    while len(line) > width:
        break_pos = max(line.rfind(op, 0, width) for op in ["+", "-", "*", "/"])
        if break_pos == -1:
            break_pos = line.rfind(" ", 0, width)
        if break_pos == -1:
            break_pos = width
        parts.append(line[:break_pos].rstrip() + continuation)
        line = indent + line[break_pos:].lstrip()
    parts.append(line)
    return parts

# Write C/C++ test file
def write_cpp_test(name):
    code = textwrap.dedent(f"""
    // Test file\n
    #include <iostream>
    #include "{name}.h"\n
    int main() {{\n
        // Insert code\n
        return 0;
    }}
    """).lstrip()
    return code

# Write Fortran test file
def write_fortran_test(name):
    code = textwrap.dedent(f"""
    ! Test file\n
    program test\n
        use {name}\n
        ! Insert code\n
    end program test
    """).lstrip()
    return code

# Write Octave/Matlab test file
def write_octave_test(name):
    code = textwrap.dedent(f"""
    % Test file\n
    {name}\n
    % Insert code
    """).lstrip()
    return code

# Write Python test file
def write_python_test(name):
    code = textwrap.dedent(f"""
    # Test file\n
    import {name}\n
    # Insert code
    """).lstrip()
    return code
