# [IFF_01] Taylor-Green flow of decaying vortices

## 1. Summary

This benchmark represents an **unsteady two-dimensional isothermal incompressible fluid flow** problem in a square domain with decaying vortices. It is particularly suitable for solvers of the **unsteady Navier-Stokes equations** with solenoidal velocity fields. The case is based on an **exact analytical solution**, enabling:
- **Code verification** of numerical schemes for the Navier-Stokes equations.
- **Numerical assessment** of the incompressibility constraint and non-linear terms.
- **Convergence analysis** on structured and unstructured meshes.

## 2. Domain and meshes

The flow exhibits periodicity through repeating counter-rotating vortices in both spatial directions. Accordingly, the computational setup considers a square domain of side length $L$, with the space–time domain defined as $\Omega=\left[0,L\right]^{2}\times\left(0,T\right]$ and boundary $\Gamma$.

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

The **unsteady two-dimensional isothermal incompressible fluid flow** problem is modelled with the **Navier-Stokes equations** equipped with the appropriate boundary conditions, and reads: seek pressure and velocity functions, $p$ and $\boldsymbol{u}$, respectively, such that

$$
\begin{array}{ll}
&\dfrac{\partial\boldsymbol{u}}{\partial t}+\left(\boldsymbol{u}\cdot\nabla\right)\boldsymbol{u}-\nu\nabla^{2}\boldsymbol{u}+\dfrac{1}{\rho}\nabla p=\boldsymbol{f},&\quad\textrm{in }\Omega,\\
&\nabla\cdot\boldsymbol{u}=0,&\quad\textrm{in }\Omega,
\end{array}
$$

where $\nu$ is the fluid constant kinetic viscosity, $\rho$ is the fluid constant density, and $\boldsymbol{f}$ is a source term function in $\Omega$.

## 4. Manufactured solution

The **exact solutions** for the pressure and velocity read

$$
p\left(x,y,t\right)=\frac{\rho u^{2}_{0}}{4}\exp\left(\frac{-16\pi^{2}\alpha^{2}\nu t}{L^{2}}\right)\left(\cos\left(4\pi\alpha\frac{x}{L}\right)+\cos\left(4\pi\alpha\frac{y}{L}\right)\right),\quad\text{in }\Omega,
$$

$$
\begin{array}{ll}
&u_{x}\left(x,y,t\right)=u_{0}\exp\left(\dfrac{-8\pi^{2}\alpha^{2}\nu t}{L^{2}}\right)\sin\left(2\pi\alpha\dfrac{x}{L}\right)\cos\left(2\pi\alpha\dfrac{y}{L}\right),&\quad\quad\text{in }\Omega,\\
&u_{y}\left(x,y,t\right)=-u_{0}\exp\left(\dfrac{-8\pi^{2}\alpha^{2}\nu t}{L^{2}}\right)\cos\left(2\pi\alpha\dfrac{x}{L}\right)\sin\left(2\pi\alpha\dfrac{y}{L}\right),&\quad\quad\text{in }\Omega,
\end{array}
$$

where $u_{0}$ is the reference velocity and $\alpha$ is the vortices frequency such that $\alpha L$ corresponds to the number of counter-rotating vortices in each direction.

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="images/pressure.pdf" width="400px"></td>
      <td align="center"><img src="images/velocity_field.pdf" width="400px"></td>
    </tr>
    <tr>
      <td align="center">Pressure.</td>
      <td align="center">Velocity field.</td>
    </tr>
     <tr>
      <td align="center"><img src="images/velocity_x.pdf" width="400px"></td>
      <td align="center"><img src="images/velocity_y.pdf" width="400px"></td>
    </tr>
    <tr>
      <td align="center">Horizontal velocity.</td>
      <td align="center">Vertical velocity.</td>
    </tr>
  </table>
</div>

The **source terms** read

$$
\begin{array}{ll}
&f^{\textrm{A}}\left(r,\theta\right)=\dfrac{n\left(a^{\textrm{A}}\ln\left(r\right)+b^{\textrm{A}}\right)\left(\alpha^{\textrm{A}}n\cos\left(n\theta\right)-r^{2}\omega^{\textrm{A}}\sin\left(n\theta\right)\right)}{r^{2}},&\quad\textrm{in }\Omega^{\textrm{A}},\\
&f^{\textrm{B}}\left(r,\theta\right)=\dfrac{n\left(a^{\textrm{B}}\ln\left(r\right)+b^{\textrm{B}}\right)\left(\alpha^{\textrm{B}}n\cos\left(n\theta\right)-r^{2}\omega^{\textrm{B}}\sin\left(n\theta\right)\right)}{r^{2}},&\quad\textrm{in }\Omega^{\textrm{B}},\\
\end{array}
$$

which are obtained by substituting the manufactured solutions into the governing equations in polar coordinates.


The **boundary conditions** correspond to the **cyclic solution** on the boundaries, 

$$
\begin{array}{l}
&\phi^{\textrm{A}}=\cos\left(n\theta\right),&\quad\textrm{on }\Gamma^{\textrm{A}},\\
&\phi^{\textrm{B}}=0,&\quad\textrm{on }\Gamma^{\textrm{B}}.
\end{array}
$$




## 5. Case parameters

The table below summarises the given constant parameters and the recommended values for two case configurations: a low-diffusivity ratio ($\alpha^{\textrm{A}}/\alpha^{\textrm{B}}=2$) and a high-diffusivity ratio ($\alpha^{\textrm{A}}/\alpha^{\textrm{B}}=100$).

| Symbol                    | Description                                                       | Value (low Reynolds number)   | Value (high Reynolds number)   | Units              |
|:--------------------------|:------------------------------------------------------------------|------------------------------:|-------------------------------:|:-------------------|
| $L$                       | Domain length                                                     | 1.0                           | 1.0                            | m                  |
| $T$                       | Final time                                                        | 1.0                           | 1.0                            | s                  |
| $\nu$                     | Fluid kinetic viscosity                                           | 1.0                           | 1.0                            | m<sup>2</sup>/s    |
| $\rho$                    | Fluid density                                                     | 1.0                           | 1.0                            | kg/m<sup>3</sup>   |
| $u_{0}$                   | Reference velocity                                                | 1.0                           | 100.0                          | m/s                |
| $\alpha$                  | Vorticies frequency                                               | 2                             | 2                              |                    |



## 6. Scripts and files

The table below summarises the functionality and usage of the supplied scripts. Check script headers for requirements and dependencies.

| File                        | Description                                                                     | Usage (command-line)          |
|:----------------------------|:--------------------------------------------------------------------------------|:------------------------------|
| `generate_quadmesh.msh` | Generates quadrilateral structured meshes in MSH format. Mesh refinement can be controlled through the command-line option `-setnumber N <value>` where `<value>` is a numerical argument specifying the desired refinement level (default: `1`). Outputs are saved in `meshes/`. | `gmsh -setnumber N 1 generate_quadmesh.msh` |
| `generate_triamesh.msh` | Generates triangular unstructured meshes in MSH format. Mesh refinement can be controlled through the command-line option `-setnumber N <value>` where `<value>` is a numerical argument specifying the desired refinement level (default: `1`). Outputs are saved in `meshes/`. | `gmsh -setnumber N 1 generate_triamesh.msh` |
| `generate_code.py` | Generates code for the symbolic expressions of parameters and functions in multiple programming languages: C/C++, Fortran, Octave/Matlab, and Python. Outputs are saved in `codes/`. | `python generate_code.py` |
| `helpers.py` | Utility functions for code generation in multiple programming languages: C/C++, Fortran, Octave/Matlab, and Python. Includes code formatting and line-wrapping helpers to keep generated source code within a configurable indent and line width. | |

## 7. How to cite

If you have used this test case or supplied material — in its original or modified form — in your research, please acknowledge the original work when publishing your results:

> **R. Costa**, J.M. Nóbrega, S. Clain, and G.J. Machado, _Very high-order accurate polygonal mesh finite volume scheme for conjugate heat transfer problems with curved interfaces and imperfect contacts_, **Computer Methods in Applied Mechanics and Engineering**, Vol. 357, 112560, 2019. DOI: [10.1016/j.cma.2019.07.029](https://doi.org/10.1016/j.cma.2019.07.029).

For your convenience, you may use the following BibTeX entry:

```bibtex
@article{Costa2019,
  title={Very high-order accurate polygonal mesh finite volume scheme for conjugate heat transfer problems with curved interfaces and imperfect contacts},
  author={Costa, R. and Nóbrega, J. M. and Clain, S. and Machado, G. J.},
  journal={Computer Methods in Applied Mechanics and Engineering},
  volume={357},
  pages={112560},
  year={2019},
  doi={10.1016/j.cma.2019.07.029}
}
```
