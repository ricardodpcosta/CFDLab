# [INSE_02] Flow between rotating cylinders (Taylor-Couette flow)

## 1. Summary

This benchmark represents an **stationary two-dimensional isothermal incompressible fluid flow** problem confined between two infinitely long coaxial cylinders rotating at specific constant angular velocities. Since the cylinder lengths are assumed to be infinite, the flow occurs only along the azimuthal axis and, under these conditions, the flow has known analytic solutions for the pressure and velocity. It is particularly suitable for solvers of the **stationary Navier-Stokes equations** with solenoidal velocity fields. The case is based on an **exact analytical solution** in polar coordinates, enabling:
- **Code verification** of numerical schemes for the Navier-Stokes equations.
- **Numerical assessment** of the incompressibility constraint and non-linear terms.
- **Convergence analysis** on structured and unstructured meshes.

> **NOTE:** For conciseness and readability, all functions are expressed in polar coordinates $\left(r,\theta\right)$, and vectors are represented in the unit polar basis $\lbrace\hat{\boldsymbol{r}},\hat{\boldsymbol{\theta}}\rbrace$. However, the codes generated from the symbolic expressions are implemented in Cartesian coordinates, ensuring direct applicability in numerical solvers.

## 2. Domain and meshes

The **domain**, $\Omega$, consists of an outer and inner concentric circular boundaries, $\Gamma^{\textrm{O}}$ and $\Gamma^{\textrm{I}}$, respectively, centred at the origin and with radius $r^{\textrm{O}}$ and $r^{\textrm{I}}$, respectively.

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="images/domain.png" width="300px"></td>
      <td align="center"><img src="images/quadmesh.png" width="300px"></td>
      <td align="center"><img src="images/triamesh.png" width="300px"></td>
    </tr>
    <tr>
      <td align="center">Domain and notation.</td>
      <td align="center">Structured quadrilateral mesh.</td>
      <td align="center">Unstructured triangular mesh.</td>
    </tr>
  </table>
</div>

**Structured quadrilateral** and **unstructured triangular meshes** with uniform mesh characteristic size are supplied to discretise both subdomains.

## 3. Model problem

The **stationary two-dimensional isothermal incompressible fluid flow** problem is modelled with the **Navier-Stokes equations** equipped with the appropriate boundary conditions, and reads: seek pressure and velocity functions, $p$ and $\boldsymbol{u}$, respectively, such that

$$
\begin{array}{ll}
&\left(\boldsymbol{u}\cdot\nabla\right)\boldsymbol{u}-\nu\nabla^{2}\boldsymbol{u}+\dfrac{1}{\rho}\nabla p=\boldsymbol{f},&\quad\textrm{in }\Omega,\\
&\nabla\cdot\boldsymbol{u}=0,&\quad\textrm{in }\Omega,
\end{array}
$$

where $\nu$ is the fluid constant kinetic viscosity, $\rho$ is the fluid constant density, and $\boldsymbol{f}$ is a source term function in $\Omega$.

## 4. Exact solutions

The **exact solutions** for the pressure and velocity read

$$
\begin{array}{ll}
&p\left(r,\theta\right)=\rho\left(\dfrac{a^{2}}{2}r^{2}+2ab\ln\left(r\right)-\dfrac{b^{2}}{2r^{2}}-c\right),&\quad\text{in }\Omega,\\
&u_{r}\left(r,\theta\right)=0,&\quad\text{in }\Omega,\\
&u_{\theta}\left(r,\theta\right)=ar+\dfrac{b}{r},&\quad\text{in }\Omega,
\end{array}
$$

where $c=\left.\left(c_{\textrm{O}}-c_{\textrm{I}}\right)\middle/\left(\pi\left(r_{\textrm{O}}^{2}-r_{\textrm{I}}^{2}\right)\right)\right.$ guarantees a null pressure mean-value in $\Omega$, and parameters $a$, $b$, $c_{\textrm{I}}$, and $c_{\textrm{O}}$ are are constant parameters given as

$$
\begin{array}{ll}
&a=\dfrac{\omega_{\textrm{O}}r_{\textrm{O}}^{2}-\omega_{\textrm{I}}r_{\textrm{I}}^{2}}{r_{\textrm{O}}^{2}-r_{\textrm{I}}^{2}},
\quad
&&b=\left(\omega_{\textrm{O}}-\omega_{\textrm{I}}\right)\dfrac{r_{\textrm{O}}^{2}r_{\textrm{I}}^{2}}{r_{\textrm{O}}^{2}-r_{\textrm{I}}^{2}},\\
&c_{\textrm{I}}=2\pi\left(\dfrac{a^{2}}{8}r_{\textrm{I}}^{4}+ab\left(\ln\left(r_{\textrm{I}}\right)-\dfrac{1}{2}\right)r_{\textrm{I}}^{2}-\dfrac{b^{2}}{2\ln\left(r_{\textrm{I}}\right)}\right),
\quad
&&c_{\textrm{O}}=2\pi\left(\dfrac{a^{2}}{8}r_{\textrm{O}}^{4}+ab\left(\ln\left(r_{\textrm{O}}\right)-\dfrac{1}{2}\right)r_{\textrm{O}}^{2}-\dfrac{b^{2}}{2\ln\left(r_{\textrm{O}}\right)}\right),
\end{array}
$$

where $\omega_{\textrm{O}}$ and $\omega_{\textrm{I}}$ are constant parameters to control the angular velocity on the outer and inner boundaries, respectively.

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="images/pressure.png" width="400px"></td>
      <td align="center"><img src="images/velocity_field.png" width="400px"></td>
    </tr>
    <tr>
      <td align="center">Pressure.</td>
      <td align="center">Velocity field.</td>
    </tr>
     <tr>
      <td align="center"><img src="images/velocity_x.png" width="400px"></td>
      <td align="center"><img src="images/velocity_y.png" width="400px"></td>
    </tr>
    <tr>
      <td align="center">Horizontal velocity.</td>
      <td align="center">Vertical velocity.</td>
    </tr>
  </table>
</div>

The **source term** vanishes for this exact solution, that is

$$
\begin{array}{ll}
&f_{r}\left(x,y\right)=0,&\quad\text{in }\Omega,\\
&f_{\theta}\left(x,y\right)=0,&\quad\text{in }\Omega.
\end{array}
$$

The **boundary conditions** prescribed for both the velocity correspond to the **Dirichlet boundary condition** on the outer and inner boundaries, considering the prescribed angular velocities, that is

$$
\begin{array}{ll}
&u_{r}\left(r,\theta\right)=0,&\quad\text{on }\Gamma^{\textrm{O}},\\
&u_{\theta}\left(r,\theta\right)=\omega^{\textrm{O}},&\quad\text{on }\Gamma^{\textrm{O}},\\
&u_{r}\left(r,\theta\right)=0,&\quad\text{on }\Gamma^{\textrm{I}},\\
&u_{\theta}\left(r,\theta\right)=\omega^{\textrm{I}},&\quad\text{on }\Gamma^{\textrm{I}}.\\
\end{array}
$$

## 5. Case parameters

The table below summarises the given constant parameters and the recommended values for two case configurations: a low Reynolds number ($Re=1$) and a high Reynolds number ($Re=100$).

| Symbol                    | Description                                                       | Value (low Reynolds number)   | Value (high Reynolds number)   | Units              |
|:--------------------------|:------------------------------------------------------------------|------------------------------:|-------------------------------:|:-------------------|
| $r^{\textrm{O}}$          | Radius of outer boundary, $\Gamma^{\textrm{O}}$                   | 1.0                           | 1.0                            | m                  |
| $r^{\textrm{I}}$          | Radius of inner boundary, $\Gamma^{\textrm{I}}$                   | 0.5                           | 0.5                            | m                  |
| $\nu$                     | Fluid kinetic viscosity                                           | 1.0                           | 1.0                            | m<sup>2</sup>/s    |
| $\rho$                    | Fluid density                                                     | 1.0                           | 1.0                            | kg/m<sup>3</sup>   |
| $\omega^{\textrm{O}}$     | Angular velocity of outer boundary, $\Gamma^{\textrm{O}}$         | 1.0                           | 100.0                          | rad/s              |
| $\omega^{\textrm{I}}$     | Angular velocity of inner boundary, $\Gamma^{\textrm{i}}$         | -2.0                          | -200.0                         | rad/s              |

## 6. Scripts and files

The table below summarises the functionality and usage of the supplied scripts. Check script headers for requirements and dependencies.

| File                        | Description                                                                     | Usage (command-line)          |
|:----------------------------|:--------------------------------------------------------------------------------|:------------------------------|
| `generate_quadmesh.msh` | Generates quadrilateral structured meshes in MSH format. Mesh refinement can be controlled through the command-line option `-setnumber N <value>` where `<value>` is a numerical argument specifying the desired refinement level (default: `1`). Outputs are saved in `meshes/`. | `gmsh -setnumber N 1 generate_quadmesh.msh` |
| `generate_triamesh.msh` | Generates triangular unstructured meshes in MSH format. Mesh refinement can be controlled through the command-line option `-setnumber N <value>` where `<value>` is a numerical argument specifying the desired refinement level (default: `1`). Outputs are saved in `meshes/`. | `gmsh -setnumber N 1 generate_triamesh.msh` |
| `generate_code.py` | Generates code for the symbolic expressions of parameters and functions in multiple programming languages: C/C++, Fortran, Octave/Matlab, and Python. Outputs are saved in `codes/`. | `python generate_code.py` |
| `helpers.py` | Utility functions for code generation in multiple programming languages: C/C++, Fortran, Octave/Matlab, and Python. Includes code formatting and line-wrapping helpers to keep generated source code within a configurable indent and line width. | |

## 7. How to cite

If you have used this benchmark or supplied material — in its original or modified form, in part or in whole — in your research, please acknowledge the original work when publishing your results:

> **R. Costa**, S. Clain, G.J. Machado, and J.M. Nóbrega, _Very high-order accurate finite volume method for the steady-state incompressible Navier-Stokes equations with polygonal meshes on arbitrary curved boundaries_, **Computer Methods in Applied Mechanics and Engineering**, Vol. 396, 115064, 2022. DOI: [10.1016/j.cma.2022.115064](https://doi.org/10.1016/j.cma.2022.115064).

For your convenience, you may use the following BibTeX entry:

```bibtex
@article{Costa2022,
  title={Very high-order accurate finite volume method for the steady-state incompressible Navier-Stokes equations with polygonal meshes on arbitrary curved boundaries},
  author={Costa, R. and Clain, S. and Machado, G. J. and Nóbrega, J. M.},
  journal={Computer Methods in Applied Mechanics and Engineering},
  volume={396},
  pages={115064},
  year={2022},
  doi={10.1016/j.cma.2022.115064}
}
```
