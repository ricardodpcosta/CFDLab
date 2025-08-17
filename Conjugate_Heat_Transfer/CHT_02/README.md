# [CHT_02] Rose-shape interface with the continuity condition

## 1. Summary

This benchmark represents a **steady-state two-dimensional conjugate heat transfer** problem in a concentric circular/rose-shaped domain divided into two regions with different thermal diffusivities. It is particularly suitable for solvers that support **multi-material conduction** with optional rotational convection. The case is based on **manufactured analytical solutions** in polar coordinates, enabling:
- **Code verification** of diffusion and convection numerical schemes.
- **Numerical assessment** of interface treatments (solution continuity and flux conservation).
- **Convergence analysis** on structured and unstructured meshes.

> For conciseness and readability, all functions are expressed in polar coordinates $\left(r,\theta\right)$, and vectors are represented in the unit polar basis $\lbrace\hat{\boldsymbol{r}},\hat{\boldsymbol{\theta}}\rbrace$. However, the codes generated from the symbolic expressions are implemented in Cartesian coordinates, ensuring direct applicability in numerical solvers.

## 2. Domain and meshes

The **domain**, $\Omega$, consists of an outer and inner concentric circular boundaries, $\Gamma^{\textrm{A}}$ and $\Gamma^{\textrm{B}}$, centered at the origin and with radius $r^{\textrm{A}}$ and $r^{\textrm{B}}$, respectively. An interface, $\Gamma^{\textrm{AB}}$, with variable radius $R^{\textrm{AB}}$, divides the domain into two subdomains, $\Omega^{\textrm{A}}$ and $\Omega^{\textrm{B}}$, corresponding to the outer and inner regions. The interface radius corresponds to a periodic perturbation (diffeomorphic transformation) applied to a circumference centred at the origin with radius $r^{\textrm{AB}}$, and reads

$$
R^{\textrm{AB}}\left(\theta\right)=r^{\textrm{AB}}\left(1+\beta_{1}\cos\left(\beta_{2}\theta\right)\right),
$$

where $\beta_{1}$ and $\beta_{2}$ are given constant parameters to control the perturbation magnitude and periodicity, respectively.

Vector functions $\boldsymbol{n}^{\textrm{A}}$ and $\boldsymbol{n}^{\textrm{B}}$ correspond to the outward unit normal vectors on boundaries $\Gamma^{\textrm{A}}$ and $\Gamma^{\textrm{B}}$, respectively. On the interface, $\Gamma^{\textrm{AB}}$, vector function $\boldsymbol{n}^{\textrm{AB}}$ corresponds to the unit normal vector from subdomain $\Omega^{\textrm{A}}$ to $\Omega^{\textrm{B}}$, and reads

$$
\boldsymbol{n}^{\textrm{AB}}\left(\theta\right)=\left(\sqrt{\left(R^{\textrm{AB}}\left(\theta\right)\right)^{2}+\left(\dfrac{\textrm{d}R^{\textrm{AB}}\left(\theta\right)}{\textrm{d}\theta}\right)^{2}}\right)^{-1}\left(-R^{\textrm{AB}}\left(\theta\right)\hspace{1pt}\hat{\boldsymbol{r}}+\dfrac{\textrm{d}R^{\textrm{AB}}\left(\theta\right)}{\textrm{d}\theta}\hat{\boldsymbol{\theta}}\right).
$$

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

**Structured quadrilateral** and **unstructured triangular meshes** with matching nodes on the interface are supplied to discretise both subdomains. A smooth variation of the local mesh characteristic size is implemented to accurately resolve the increasing curvature of the boundaries/interface toward the domain centre.

## 3. Model problem

The **steady-state conjugate heat transfer problem** reads: seek temperature distribution functions $\phi^{\textrm{A}}$ and $\phi^{\textrm{B}}$ such that

$$
\begin{array}{l}
&\nabla\cdot\left(\boldsymbol{u}^{\textrm{A}}\phi^{\textrm{A}}\right)-\alpha^{\textrm{A}}\nabla^{2}\phi^{\textrm{A}}=f^{\textrm{A}},&\quad\textrm{in }\Omega^{\textrm{A}},\\
&\nabla\cdot\left(\boldsymbol{u}^{\textrm{B}}\phi^{\textrm{B}}\right)-\alpha^{\textrm{B}}\nabla^{2}\phi^{\textrm{B}}=f^{\textrm{B}},&\quad\textrm{in }\Omega^{\textrm{B}},\\
\end{array}
$$

where $\alpha^{\textrm{A}}$ and $\alpha^{\textrm{B}}$ are given constant thermal diffusivities, $\boldsymbol{u}^{\textrm{A}}$ and $\boldsymbol{u}^{\textrm{B}}$ are given velocity field functions, and $f^{\textrm{A}}$ and $f^{\textrm{B}}$ are source-term functions in subdomains $\Omega^{\textrm{A}}$ and $\Omega^{\textrm{B}}$, respectively.

## 4. Manufactured solution

The **manufactured solutions** read

$$
\begin{array}{l}
&\phi^{\textrm{A}}\left(r,\theta\right)=a^{\textrm{A}}\ln\left(D\left(r,\theta\right)\right)+b^{\textrm{A}},&\quad\textrm{in }\Omega^{\textrm{A}},\\
&\phi^{\textrm{B}}\left(r,\theta\right)=a^{\textrm{B}}\ln\left(D\left(r,\theta\right)\right)+b^{\textrm{B}},&\quad\textrm{in }\Omega^{\textrm{B}},
\end{array}
$$

where $a^{\textrm{A}}$, $a^{\textrm{B}}$, $b^{\textrm{A}}$, and $b^{\textrm{B}}$ are constant parameters to enforce boundary and interface conditions and $D\left(\theta\right)$ is a mapping function to a domain with a circular interface, and read

$$
D\left(r,\theta\right)=d_{1}\left(\theta\right)+d_{2}\left(\theta\right)r+d_{3}\left(\theta\right)r^{2},
$$

where $d_{1}$, $d_{2}$, and $d_{3}$ are constant parameters to enforce that $D\left(r^{\textrm{A}},\theta\right)=r^{\textrm{A}}$, $D\left(r^{\textrm{B}},\theta\right)=r^{\textrm{B}}$, and $D\left(R^{\textrm{AB}}\left(\theta\right),\theta\right)=r^{\textrm{AB}}$, and read

$$
d_{1}\left(\theta\right)=-cr^{\textrm{A}}r^{\textrm{B}}\beta_{1}\cos\left(\beta_{2}\theta\right),\qquad
d_{2}\left(\theta\right)=1+c\left(r^{\textrm{A}}+r^{\textrm{B}}\right)r^{\textrm{AB}}\beta_{1}\cos\left(\beta_{2}\theta\right),\qquad
d_{3}\left(\theta\right)=-c\beta_{1}\cos\left(\beta_{2}\theta\right),
$$
$$
c=\left(r^{\textrm{AB}}\left(1+\beta_{1}\cos\left(\beta_{2}\theta\right)\right)-r^{\textrm{A}}\right)^{-1}\left(r^{\textrm{AB}}\left(1+\beta_{1}\cos\left(\beta_{2}\theta\right)\right)-r^{\textrm{B}}\right)^{-1}.
$$

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="images/solution_1.png" width="400px"></td>
      <td align="center"><img src="images/solution_2.png" width="400px"></td>
    </tr>
    <tr>
      <td align="center">Manufactured solution in the low-diffusivity ratio case.</td>
      <td align="center">Manufactured solution in the high-diffusivity ratio case.</td>
    </tr>
  </table>
</div>

The **velocity fields** are tangential to the boundaries and interface, such that no mass transfer occurs through the boundaries and interface, and read

$$
\begin{array}{ll}
&\boldsymbol{u}^{\textrm{A}}\left(r,\theta\right)=\omega^{\textrm{A}}r\left(\left(\dfrac{r-r^{\textrm{A}}}{R^{\textrm{AB}}\left(\theta\right)-r^{\textrm{A}}}\right)\dfrac{\textrm{d}R^{\textrm{AB}}\left(\theta\right)}{\textrm{d}\theta}\hat{\boldsymbol{r}}+\hat{\boldsymbol{\theta}}\right),&\quad\textrm{in }\Omega^{\textrm{A}},\\
&\boldsymbol{u}^{\textrm{B}}\left(r,\theta\right)=\omega^{\textrm{B}}r\left(\left(\dfrac{r-r^{\textrm{B}}}{R^{\textrm{AB}}\left(\theta\right)-r^{\textrm{B}}}\right)\dfrac{\textrm{d}R^{\textrm{AB}}\left(\theta\right)}{\textrm{d}\theta}\hat{\boldsymbol{r}}+\hat{\boldsymbol{\theta}}\right),&\quad\textrm{in }\Omega^{\textrm{B}},\\
\end{array}
$$

where $\omega^{\textrm{A}}$ and $\omega^{\textrm{B}}$ are given constant parameters to control the angular velocity.

The **source-terms** read

$$
\begin{array}{ll}
&f^{\textrm{A}}\left(r,\theta\right)=\dfrac{n\left(a^{\textrm{A}}\ln\left(r\right)+b^{\textrm{A}}\right)\left(\alpha^{\textrm{A}}n\cos\left(n\theta\right)-r^{2}\omega^{\textrm{A}}\sin\left(n\theta\right)\right)}{r^{2}}&\quad\textrm{in }\Omega^{\textrm{A}},\\
&f^{\textrm{B}}\left(r,\theta\right)=\dfrac{n\left(a^{\textrm{B}}\ln\left(r\right)+b^{\textrm{B}}\right)\left(\alpha^{\textrm{B}}n\cos\left(n\theta\right)-r^{2}\omega^{\textrm{B}}\sin\left(n\theta\right)\right)}{r^{2}}&\quad\textrm{in }\Omega^{\textrm{B}},\\
\end{array}
$$

which are obtained after substituting the manufactured solutions into the governing equations in polar coordinates.

The **boundary conditions** correspond to the **constant solution** on the outer boundary and the **homogeneous solution** on the inner boundary, that is

$$
\begin{array}{l}
&\phi^{\textrm{A}}=1,&\quad\textrm{on }\Gamma^{\textrm{A}},\\
&\phi^{\textrm{B}}=0,&\quad\textrm{on }\Gamma^{\textrm{B}}.
\end{array}
$$

The **interface conditions** correspond to the **solution continuity** and the **conservation of diffusive fluxes** on the interface, that is

$$
\begin{array}{l}
&\phi^{\textrm{A}}=\phi^{\textrm{B}},&\quad\textrm{on }\Gamma^{\textrm{AB}},\\
&-\alpha^{\textrm{A}}\nabla\phi^{\textrm{A}}\cdot\boldsymbol{n}^{\textrm{A}}=-\alpha^{\textrm{B}}\nabla\phi^{\textrm{B}}\cdot\boldsymbol{n}^{\textrm{AB}},&\quad\textrm{on }\Gamma^{\textrm{AB}}.
\end{array}
$$

Parameters $a^{\textrm{A}}$, $a^{\textrm{B}}$, $b^{\textrm{A}}$, and $b^{\textrm{B}}$ in the analytical solutions are determined such that boundary and interface conditions are simultaneously satisfied, and read

$$
a^{\textrm{A}}=c\alpha^{\textrm{B}},\qquad
a^{\textrm{B}}=c\alpha^{\textrm{A}},\qquad
b^{\textrm{A}}=c\left(\alpha^{\textrm{A}}\ln\left(\dfrac{r^{\textrm{AB}}}{r^{\textrm{B}}}\right)-\alpha^{\textrm{B}}\ln\left(r^{\textrm{AB}}\right)\right),\qquad
b^{\textrm{B}}=-c\alpha^{\textrm{A}}\ln\left(r^{\textrm{B}}\right),\qquad
c=\left(\alpha^{\textrm{A}}\ln\left(\dfrac{r^{\textrm{AB}}}{r^{\textrm{B}}}\right)+\alpha^{\textrm{B}}\ln\left(\dfrac{r^{\textrm{A}}}{r^{\textrm{AB}}}\right)\right)^{-1}.
$$

## 5. Case parameters

The table below summarises the given constant parameters and the recommended values for two case configurations: a low-diffusivity ratio ($\alpha^{\textrm{A}}/\alpha^{\textrm{B}}=2$) and a high-diffusivity ratio ($\alpha^{\textrm{A}}/\alpha^{\textrm{B}}=100$).

| Symbol                    | Description                                                       | Value (low-diffusivity ratio) | Value (high-diffusivity ratio) | Units              |
|:--------------------------|:------------------------------------------------------------------|------------------------------:|-------------------------------:|:-------------------|
| $r^{\textrm{A}}$          | Radius of outer boundary, $\Gamma^{\textrm{A}}$                   | 1.0                           | 1.0                            | m                  |
| $r^{\textrm{AB}}$         | Radius of interface, $\Gamma^{\textrm{AB}}$                       | 0.75                          | 0.75                           | m                  |
| $r^{\textrm{B}}$          | Radius of inner boundary, $\Gamma^{\textrm{B}}$                   | 0.5                           | 0.5                            | m                  |
| $\beta_{1}$               | Magnitude of interface perturbation, $\Gamma^{\textrm{AB}}$       | 0.04                          | 0.04                           |                    |
| $\beta_{2}$               | Periodicity of interface perturbation, $\Gamma^{\textrm{AB}}$     | 8.0                           | 8.0                            |                    |
| $\alpha^{\textrm{A}}$     | Thermal diffusivity in outer subdomain, $\Omega^{\textrm{A}}$     | 2.0                           | 100.0                          | m<sup>2</sup>/s    |
| $\alpha^{\textrm{B}}$     | Thermal diffusivity in inner subdomain, $\Omega^{\textrm{B}}$     | 1.0                           | 1.0                            | m<sup>2</sup>/s    |
| $\omega^{\textrm{A}}$     | Angular velocity in outer subdomain, $\Omega^{\textrm{A}}$        | 1.0                           | 1.0                            | rad/s              |
| $\omega^{\textrm{B}}$     | Angular velocity in inner subdomain, $\Omega^{\textrm{B}}$        | -1.0                          | -1.0                           | rad/s              |

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
