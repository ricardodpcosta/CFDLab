#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
CFDLab | HELPERS
===============================================================================

Description:
    Utility functions for code generation in multiple programming languages:
    C/C++, Fortran, Octave/Matlab, and Python.
    Includes code formatting and line-wrapping helpers to keep generated source
    code within a configurable indent and line width.

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

# import modules
import os
import re
import textwrap
import sympy

# import specific printers
try:
    from sympy.printing.c import ccode
    from sympy.printing.fortran import fcode
    from sympy.printing.octave import octave_code
    from sympy.printing.pycode import pycode
except Exception:
    raise RuntimeError("Required SymPy printers not available. Ensure sympy >= 1.6 is installed.")

#============================================
# WRITE CONSTANTS
#============================================

# write C/C++ constants
def write_cpp_constants(consts_list):
    """
    Generate C/C++ constants definition from a symbolic expression.
    """
    decl_lines = ["// Global constants"]
    for i, (varname, varexpr) in enumerate(consts_list):
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

# write Fortran constants
def write_fortran_constants(consts_list):
    """
    Generate Fortran constants definition from a symbolic expression.
    """
    decl_lines = ["! Global constants"]
    for i, (varname, varexpr) in enumerate(consts_list):
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

# write Octave/Matlab constants
def write_octave_constants(consts_list):
    """
    Generate Octave/Matlab constants definition from a symbolic expression.
    """
    decl_lines = ["% Global constants"]
    for i, (varname, varexpr) in enumerate(consts_list):
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

# write Python constants
def write_python_constants(consts_list):
    """
    Generate Python constants definition from a symbolic expression.
    """
    decl_lines = ["# Global constants"]
    for i, (varname, varexpr) in enumerate(consts_list):
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

#============================================
# WRITE GENERIC FUNCTIONS
#============================================

# write C/C++ function
def write_cpp_function(name, expr, args_list, params_list):
    """
    Generate a C/C++ function definition from a symbolic expression.
    """
    if isinstance(expr, sympy.Matrix):
        return write_cpp_vector_function(name, expr, args_list, params_list)
    else:
        return write_cpp_scalar_function(name, expr, args_list, params_list)

# write Fortran function
def write_fortran_function(name, expr, args_list, params_list):
    """
    Generate a Fortran function definition from a symbolic expression.
    """
    if isinstance(expr, sympy.Matrix):
        return write_fortran_vector_function(name, expr, args_list, params_list)
    else:
        return write_fortran_scalar_function(name, expr, args_list, params_list)

# write Octave/Matlab function
def write_octave_function(name, expr, args_list, consts_list, params_list):
    """
    Generate a Octave/Matlab function definition from a symbolic expression.
    """
    if isinstance(expr, sympy.Matrix):
        return write_octave_vector_function(name, expr, args_list, consts_list, params_list)
    else:
        return write_octave_scalar_function(name, expr, args_list, consts_list, params_list)

# write Python function
def write_python_function(name, expr, args_list, params_list):
    """
    Generate a Python function definition from a symbolic expression.
    """
    if isinstance(expr, sympy.Matrix):
        return write_python_vector_function(name, expr, args_list, params_list)
    else:
        return write_python_scalar_function(name, expr, args_list, params_list)

#============================================
# WRITE SCALAR FUNCTIONS
#============================================

# write C/C++ scalar function
def write_cpp_scalar_function(name, expr, args_list, params_list):
    """
    Generate a C/C++ function definition from a scalar symbolic expression.
    """
    argnames = ", ".join(f"double {argname}" for (argname, _) in args_list)
    decl_lines = []
    for i, (parname, parexpr) in enumerate(params_list):
        cexpr = ccode(parexpr, assign_to=None)
        cexpr = cexpr.replace("\\\n", "")
        cexpr = re.sub(r" {2,}", " ", cexpr)
        cexpr = cexpr.strip()
        cexpr = wrap_code_line(f"double {parname} = {cexpr};", width=100, indent=" "*4,continuation=" \\")
        decl_lines.extend(cexpr)
    if len(params_list) > 1:
        decl_lines[1:] = [" "*12 + line for line in decl_lines[1:]]
        decl = "\n".join(decl_lines)
    cexpr = ccode(expr, assign_to=None)
    cexpr = cexpr.replace("\\\n", "")
    cexpr = re.sub(r" {2,}", " ", cexpr)
    cexpr = cexpr.strip()
    cexpr = wrap_code_line(f"double res = {cexpr};", width=100, indent=" "*16,continuation=" \\")
    cexpr.append(" "*12 + "return res;")
    comp = "\n".join(cexpr)
    if len(params_list) > 1:
        code = textwrap.dedent(f"""
        // Function {name}
        inline double {name}({argnames}) {{
            {decl}
            {comp}
        }}
        """).strip()
    else:
        code = textwrap.dedent(f"""
        // Function {name}
        inline double {name}({argnames}) {{
            {comp}
        }}
        """).strip()
    return code

# write Fortran scalar function
def write_fortran_scalar_function(name, expr, args_list, params_list):
    """
    Generate a Fortran function definition from a scalar symbolic expression.
    """
    argnames = ", ".join(argname for (argname, _) in args_list)
    decl_lines = [f"real(8), intent(in) :: {argname}" for (argname, _) in args_list]
    decl_lines.append("real(8) :: res")
    decl_lines.extend([f"real(8) :: {parname}" for (parname, _) in params_list])
    for i, (parname, parexpr) in enumerate(params_list):
        fexpr = fcode(parexpr, assign_to=None, source_format="free")
        fexpr = fexpr.replace("&\n", "")
        fexpr = re.sub(r" {2,}", " ", fexpr)
        fexpr = fexpr.strip()
        fexpr = wrap_code_line(f"{parname} = {fexpr}", width=100, indent=" "*4,continuation=" &")
        decl_lines.extend(fexpr)
    if len(params_list) > 1:
        decl_lines[1:] = [" "*12 + line for line in decl_lines[1:]]
        decl = "\n".join(decl_lines)
    fexpr = fcode(expr, assign_to=None, source_format="free")
    fexpr = fexpr.replace("&\n", "")
    fexpr = re.sub(r" {2,}", " ", fexpr)
    fexpr = fexpr.strip()
    comp = "\n".join(wrap_code_line(f"res = {fexpr}", width=100, indent=" "*16,continuation=" &"))
    if len(params_list) > 1:
        code = textwrap.dedent(f"""
        ! Function {name}
        function {name}({argnames}) result(res)
            {decl}
            {comp}
        end function {name}
        """).strip()
    else:
        code = textwrap.dedent(f"""
        ! Function {name}
        function {name}({argnames}) result(res)
            {comp}
        end function {name}
        """).strip()
    return code

# write Octave/Matlab scalar function
def write_octave_scalar_function(name, expr, args_list, consts_list, params_list):
    """
    Generate an Octave/Matlab function definition from a scalar symbolic expression.
    """
    argnames = ", ".join(argname for (argname, _) in args_list)
    decl_lines = ["global " + varname + ";" for (varname, _) in consts_list]
    for i, (parname, parexpr) in enumerate(params_list):
        mexpr = octave_code(parexpr, assign_to=None)
        mexpr = mexpr.replace("...\n", "")
        mexpr = re.sub(r" {2,}", " ", mexpr)
        mexpr = mexpr.strip()
        mexpr = wrap_code_line(f"{parname} = {mexpr};", width=100, indent=" "*4,continuation=" ...")
        decl_lines.extend(mexpr)
    if len(params_list) > 1:
        decl_lines[1:] = [" "*12 + line for line in decl_lines[1:]]
        decl = "\n".join(decl_lines)
    mexpr = octave_code(expr, assign_to=None)
    mexpr = mexpr.replace("...\n", "")
    mexpr = re.sub(r" {2,}", " ", mexpr)
    mexpr = mexpr.strip()
    mexpr = wrap_code_line(f"res = {mexpr};", width=100, indent=" "*16,continuation=" ...")
    comp = "\n".join(mexpr)
    if len(params_list) > 1:
        code = textwrap.dedent(f"""
        % Function {name}
        function res = {name}({argnames})
            {decl}
            {comp}
        end
        """).strip()
    else:
        code = textwrap.dedent(f"""
        % Function {name}
        function res = {name}({argnames})
            {comp}
        end
        """).strip()
    return code

# write Python scalar function
def write_python_scalar_function(name, expr, args_list, params_list):
    """
    Generate a Python function definition from a scalar symbolic expression.
    """
    argnames = ", ".join(argname for (argname, _) in args_list)
    decl_lines = []
    for i, (parname, parexpr) in enumerate(params_list):
        pexpr = pycode(parexpr)
        pexpr = pexpr.replace("\n", "")
        pexpr = re.sub(r" {2,}", " ", pexpr)
        pexpr = pexpr.strip()
        pexpr = wrap_code_line(f"{parname} = {pexpr}", width=100, indent=" "*4,continuation=" \\")
        decl_lines.extend(pexpr)
    if len(params_list) > 1:
        decl_lines[1:] = [" "*12 + line for line in decl_lines[1:]]
        decl = "\n".join(decl_lines)
    pexpr = pycode(expr)
    pexpr = pexpr.replace("\n", "")
    pexpr = re.sub(r" {2,}", " ", pexpr)
    pexpr = pexpr.strip()
    pexpr = wrap_code_line(f"res = {pexpr}", width=100, indent=" "*16,continuation=" \\")
    pexpr.append(" "*12 + "return res")
    comp = "\n".join(pexpr)
    if len(params_list) > 1:
        code = textwrap.dedent(f"""
        # Function {name}
        def {name}({argnames}):
            {decl}
            {comp}
        """).strip()
    else:
        code = textwrap.dedent(f"""
        # Function {name}
        def {name}({argnames}):
            {comp}
        """).strip()
    return code

#============================================
# WRITE VECTOR FUNCTIONS
#============================================

# write C/C++ vector function
def write_cpp_vector_function(name, expr, args_list, params_list):
    """
    Generate a C/C++ function definition from a vector symbolic expression.
    """
    argnames = ", ".join(f"double {argname}" for (argname, _) in args_list)
    argnames += ", double res[{}]".format(len(expr))
    decl_lines = []
    for i, (parname, parexpr) in enumerate(params_list):
        cexpr = ccode(parexpr, assign_to=None)
        cexpr = cexpr.replace("\\\n", "")
        cexpr = re.sub(r" {2,}", " ", cexpr)
        cexpr = cexpr.strip()
        cexpr = wrap_code_line(f"double {parname} = {cexpr};", width=100, indent=" "*4,continuation=" \\")
        decl_lines.extend(cexpr)
    if len(params_list) > 1:
        decl_lines[1:] = [" "*12 + line for line in decl_lines[1:]]
        decl = "\n".join(decl_lines)
    comp_lines = []
    for i, compexpr in enumerate(expr):
        cexpr = ccode(compexpr, assign_to=None)
        cexpr = cexpr.replace("\\\n", "")
        cexpr = re.sub(r" {2,}", " ", cexpr)
        cexpr = cexpr.strip()
        cexpr = wrap_code_line(f"res[{i}] = {cexpr};", width=100, indent=" "*4,continuation=" \\")
        comp_lines.extend(cexpr)
    comp_lines[1:] = [" "*12 + line for line in comp_lines[1:]]
    comp = "\n".join(comp_lines)
    if len(params_list) > 1:
        code = textwrap.dedent(f"""
        // Function {name}
        inline void {name}({argnames}) {{
            {decl}
            {comp}
        }}
        """).strip()
    else:
        code = textwrap.dedent(f"""
        // Function {name}
        inline void {name}({argnames}) {{
            {comp}
        }}
        """).strip()
    return code

# write Fortran vector function
def write_fortran_vector_function(name, expr, args_list, params_list):
    """
    Generate a Fortran function definition from a vector symbolic expression.
    """
    argnames = ", ".join(argname for (argname, _) in args_list)
    argnames += ", res"
    decl_lines = [f"real(8), intent(in) :: {argname}" for (argname, _) in args_list]
    decl_lines.append("real(8), intent(out) :: res({})".format(len(expr)))
    decl_lines.extend([f"real(8) :: {parname}" for (parname, _) in params_list])
    for i, (parname, parexpr) in enumerate(params_list):
        fexpr = fcode(parexpr, assign_to=None, source_format="free")
        fexpr = fexpr.replace("&\n", "")
        fexpr = re.sub(r" {2,}", " ", fexpr)
        fexpr = fexpr.strip()
        fexpr = wrap_code_line(f"{parname} = {fexpr}", width=100, indent=" "*4,continuation=" &")
        decl_lines.extend(fexpr)
    if len(params_list) > 1:
        decl_lines[1:] = [" "*12 + line for line in decl_lines[1:]]
        decl = "\n".join(decl_lines)
    comp_lines = []
    for i, compexpr in enumerate(expr):
        fexpr = fcode(compexpr, assign_to=None, source_format="free")
        fexpr = fexpr.replace("&\n", "")
        fexpr = re.sub(r" {2,}", " ", fexpr)
        fexpr = fexpr.strip()
        fexpr = wrap_code_line(f"res({i+1}) = {fexpr}", width=100, indent=" "*4,continuation=" &")
        comp_lines.extend(fexpr)
    comp_lines[1:] = [" "*12 + line for line in comp_lines[1:]]
    comp = "\n".join(comp_lines)
    if len(params_list) > 1:
        code = textwrap.dedent(f"""
        ! Subroutine {name}
        subroutine {name}({argnames})
            {decl}
            {comp}
        end subroutine {name}
        """).strip()
    else:
        code = textwrap.dedent(f"""
        ! Subroutine {name}
        subroutine {name}({argnames})
            {comp}
        end subroutine {name}
        """).strip()
    return code

# write Octave/Matlab vector function
def write_octave_vector_function(name, expr, args_list, consts_list, params_list):
    """
    Generate a Octave/Matlab function definition from a vector symbolic expression.
    """
    argnames = ", ".join(argname for (argname, _) in args_list)
    decl_lines = ["global " + varname + ";" for (varname, _) in consts_list]
    for i, (parname, parexpr) in enumerate(params_list):
        mexpr = octave_code(parexpr, assign_to=None)
        mexpr = mexpr.replace("...\n", "")
        mexpr = re.sub(r" {2,}", " ", mexpr)
        mexpr = mexpr.strip()
        mexpr = wrap_code_line(f"{parname} = {mexpr};", width=100, indent=" "*4,continuation=" ...")
        decl_lines.extend(mexpr)
    if len(params_list) > 1:
        decl_lines[1:] = [" "*12 + line for line in decl_lines[1:]]
        decl = "\n".join(decl_lines)
    comp_lines = [f"res = zeros({len(expr)},1);"]
    for i, compexpr in enumerate(expr):
        mexpr = octave_code(compexpr, assign_to=None)
        mexpr = mexpr.replace("...\n", "")
        mexpr = re.sub(r" {2,}", " ", mexpr)
        mexpr = mexpr.strip()
        mexpr = wrap_code_line(f"res({i+1}) = {mexpr};", width=100, indent=" "*4,continuation=" ...")
        comp_lines.extend(mexpr)
    comp_lines[1:] = [" "*12 + line for line in comp_lines[1:]]
    comp = "\n".join(comp_lines)
    if len(params_list) > 1:
        code = textwrap.dedent(f"""
        % Function {name}
        function res = {name}({argnames})
            {decl}
            {comp}
        end
        """).strip()
    else:
        code = textwrap.dedent(f"""
        % Function {name}
        function res = {name}({argnames})
            {comp}
        end
        """).strip()
    return code

# write Python vector function
def write_python_vector_function(name, expr, args_list, params_list):
    """
    Generate a Python function definition from a vector symbolic expression.
    """
    argnames = ", ".join(argname for (argname, _) in args_list)
    decl_lines = []
    for i, (parname, parexpr) in enumerate(params_list):
        pexpr = pycode(parexpr)
        pexpr = pexpr.replace("\n", "")
        pexpr = re.sub(r" {2,}", " ", pexpr)
        pexpr = pexpr.strip()
        pexpr = wrap_code_line(f"{parname} = {pexpr}", width=100, indent=" "*4,continuation=" \\")
        decl_lines.extend(pexpr)
    decl_lines[1:] = [" "*12 + line for line in decl_lines[1:]]
    decl = "\n".join(decl_lines)
    comp_lines = [f"res = [0.0]*{len(expr)}"]
    for i, compexpr in enumerate(expr):
        pexpr = pycode(compexpr)
        pexpr = pexpr.replace("\n", "")
        pexpr = re.sub(r" {2,}", " ", pexpr)
        pexpr = pexpr.strip()
        pexpr = wrap_code_line(f"res[{i}] = {pexpr}", width=100, indent=" "*4,continuation=" \\")
        comp_lines.extend(pexpr)
    comp_lines.append("return res")
    comp_lines[1:] = [" "*12 + line for line in comp_lines[1:]]
    comp = "\n".join(comp_lines)
    if len(params_list) > 1:
        code = textwrap.dedent(f"""
        # Function {name}
        def {name}({argnames}):
            {decl}
            {comp}
        """).strip()
    else:
        code = textwrap.dedent(f"""
        # Function {name}
        def {name}({argnames}):
            {comp}
        """).strip()
    return code

#============================================
# WRAP CODE LINE
#============================================

# wrap code line
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

#============================================
# WRITE FILE
#============================================

# write contens to file
def write_file(path, contents):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(contents)
    print("Wrote", path)

#============================================
# WRITE FILES
#============================================

# generate implementations in C/C++
def write_cpp_file(outdir, name, consts_list, funcs_list):
    contents = ["// Auto-generated by generate_code.py", "#ifndef " + name.upper() + "_H",
                "#define " + name.upper() + "_H", "#include <cmath>"]
    contents.append(write_cpp_constants(consts_list))
    for (func_name, func_expr, func_args_list, func_params_list) in funcs_list:
        try:
            code = write_cpp_function(func_name, func_expr, func_args_list, func_params_list)
            contents.append(code)
        except Exception as e:
            print("C/C++ generation failed for", name, ":", e)
    contents.append("#endif")
    contents = "\n\n".join(contents) + "\n"
    write_file(os.path.join(outdir, name + ".h"), contents)

# generate implementations in Fortran
def write_fortran_file(outdir, name, consts_list, funcs_list):
    contents = ["! Auto-generated by generate_code.py", "module " + name.upper(), "implicit none"]
    contents.append(write_fortran_constants(consts_list))
    contents.append("contains")
    for (func_name, func_expr, func_args_list, func_params_list) in funcs_list:
        try:
            code = write_fortran_function(func_name, func_expr, func_args_list, func_params_list)
            contents.append(code)
        except Exception as e:
            print("Fortran generation failed for", name, ":", e)
    contents.append("end module " + name)
    contents = "\n\n".join(contents) + "\n"
    write_file(os.path.join(outdir, name+".f"), contents)

# generate implementations in Octave/Matlab
def write_octave_file(outdir, name, consts_list, funcs_list):
    contents = ["% Auto-generated by generate_code.py"]
    contents.append(write_octave_constants(consts_list))
    for (func_name, func_expr, func_args_list, func_params_list) in funcs_list:
        try:
            code = write_octave_function(func_name, func_expr, func_args_list, consts_list, func_params_list)
            contents.append(code)
        except Exception as e:
            print("Octave/Matlab generation failed for", name, ":", e)
    contents = "\n\n".join(contents) + "\n"
    write_file(os.path.join(outdir, name + ".m"), contents)

# generate implementations in Python
def write_python_file(outdir, name, consts_list, funcs_list):
    contents = ["# Auto-generated by generate_code.py", "import math"]
    contents.append(write_python_constants(consts_list))
    for (func_name, func_expr, func_args_list, func_params_list) in funcs_list:
        try:
            code = write_python_function(func_name, func_expr, func_args_list, func_params_list)
            contents.append(code)
        except Exception as e:
            print("Python generation failed for", name, ":", e)
    contents = "\n\n".join(contents) + "\n"
    write_file(os.path.join(outdir, name + ".py"), contents)

#============================================
# WRITE TESTS
#============================================

# write C/C++ test file
def write_cpp_test(outdir, name):
    code = textwrap.dedent(f"""
    // Test file\n
    // Compile with "gcc test.cpp -o test"
    // Run with ".\\test"\n
    #include <stdio.h>
    #include "{name}.h"\n
    int main() {{\n
        // Insert code\n
        return 0;
    }}
    """).lstrip()
    write_file(os.path.join(outdir, "test.cpp"), code)

# write Fortran test file
def write_fortran_test(outdir, name):
    code = textwrap.dedent(f"""
    ! Test file\n
    ! Compile with "gfortran -cpp test.f -o test"
    ! Run with ".\\test"\n
    #include "{name}.f"\n
    program test\n
        use {name.upper()}\n
        ! Insert code\n
    end program test
    """).lstrip()
    write_file(os.path.join(outdir, "test.f"), code)

# write Octave/Matlab test file
def write_octave_test(outdir, name):
    code = textwrap.dedent(f"""
    % Test file\n
    % Run with "octave {name}.m"\n
    {name}\n
    % Insert code
    """).lstrip()
    write_file(os.path.join(outdir, "test.m"), code)

# write Python test file
def write_python_test(outdir, name):
    code = textwrap.dedent(f"""
    # Test file\n
    # Run with "python {name}.py"\n
    import {name}\n
    # Insert code
    """).lstrip()
    write_file(os.path.join(outdir, "test.py"), code)

# end of file
