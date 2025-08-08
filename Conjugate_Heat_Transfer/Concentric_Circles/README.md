# Circular interface with continuity interface conditions (CHT_01)

---

## Overview

An annular domain $\Omega$ is considered consisting of an exterior and interior physical boundaries, $\Gamma^{\textrm{D},\textrm{A}}$ and $\Gamma^{\textrm{D},\textrm{B}}$, respectively, corresponding to circumferences centered at point $\left(0,0\right)$ and with radius $r_{\textrm{E}}=1$ and $r_{\textrm{I}}=0.5$, respectively (see Fig.XX(a)). Physical subdomains $\Omega^{\textrm{A}}$ and $\Omega^{\textrm{B}}$ correspond to the exterior and interior regions separated with physical interface $\Gamma^{\textrm{C}}$ that corresponds to a circumference centered at point $\left(0,0\right)$ and with radius $r_{\textrm{M}}=0.75$.

The analytic solutions assigned to this test case in polar coordinates $\left(r,\theta\right)$, with $r^{2}=x^{2}+y^{2}$ and $\theta=\arctan\left(y/x\right)$, are given as
$$
\phi^{S}\left(r,\theta\right)=\left(a^{S}\ln\left(r\right)+b^{S}\right)\cos\left(n^{S}\theta\right),\quad\textrm{in }\Omega^{S},
$$

where $n^{S}\in\mathbb{R}$ are given parameters and $a^{S},b^{S}\in\mathbb{R}$ are parameters to determine.
Notice that, although the analytic solutions are given in polar coordinates, the problem is numerically solved in Cartesian coordinates.
Dirichlet boundary conditions are prescribed on both physical boundaries, where for exterior physical boundary $\Gamma^{\textrm{D},\textrm{A}}$ the associated boundary condition function is periodic and given as $g^{\textrm{D},\textrm{A}}\left(r=r_{\textrm{E}},\theta\right)=\cos\left(n^{\textrm{A}}\theta\right)$, while for interior physical boundary $\Gamma^{\textrm{D},\textrm{B}}$ the associated boundary condition function is constant and given as $g^{\textrm{D},\textrm{B}}\left(r=r_{\textrm{I}},\theta\right)=0$.
On the physical interface, the continuity interface conditions are prescribed and parameters $a^{\textrm{A}}$, $a^{\textrm{B}}$, $b^{\textrm{A}}$, and $b^{\textrm{B}}$ in the analytic solutions are determined such that the Dirichlet boundary conditions and the continuity interface conditions are simultaneously satisfied.
Constant thermal conductivities $\kappa^{\textrm{A}}$ and $\kappa^{\textrm{B}}$ are assigned and parameters are determined as $a^{\textrm{A}}=-c\kappa^{\textrm{B}}$, $a^{\textrm{B}}=-c\kappa^{\textrm{A}}$, $b^{\textrm{A}}=c\left(\kappa^{\textrm{A}}\ln\left(r_{\textrm{I}}/r_{\textrm{M}}\right)+\kappa^{\textrm{B}}\ln\left(r_{\textrm{M}}\right)\right)$, and $b^{\textrm{B}}=c\kappa^{\textrm{A}}\ln\left(r_{\textrm{I}}\right)$, where constant $c$ is given as $c=\left.1\middle/\left(\kappa^{\textrm{A}}\ln\left(r_{\textrm{I}}/r_{\textrm{M}}\right)+\kappa^{\textrm{B}}\ln\left(r_{\textrm{M}}/r_{\textrm{E}}\right)\right)\right.$.
On the other side, circular velocities are assigned to both physical subdomains and are given in polar coordinates as

$$
\boldsymbol{u}^{S}\left(r,\theta\right)=\omega^{S}r\hat{\boldsymbol{\theta}},\quad\textrm{in }\Omega^{S},
$$

with given parameters $\omega^{S}\in\mathbb{R}$.
Vectors $\hat{\boldsymbol{r}}$ and $\hat{\boldsymbol{\theta}}$ are the orthogonal unit vectors in the directions of increasing $r$ and $\theta$, respectively.
Notice that, with the above velocities, no convection occurs through the physical boundaries and interface.

The associated source term functions are obtained after substituting analytic solutions given in Eq.~\eqref{eq:numerical_benchmark_c1_manufactured} into Eqs.~\eqref{eq:mathematical_formulation_convdiff_3} and~\eqref{eq:mathematical_formulation_convdiff_4}, respectively, and are given in polar coordinates as

$$
f^{S}\left(r,\theta\right)=\left(\kappa^{S}\left(n^{S}\right)^{2}\cos\left(n^{S}\theta\right)\left(a^{S}\ln\left(r\right)+b^{S}\right)\right)/r^{2}-n^{S}\omega^{S}\sin\left(n^{S}\theta\right)\left(a^{S}\ln\left(r\right)+b^{S}\right),\quad\textrm{in }\Omega^{S}.
$$



