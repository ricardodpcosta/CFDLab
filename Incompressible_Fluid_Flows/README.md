# Incompressible Fluid Flows

## 1. Summary

The **computational modelling** of **fluid flow problems** has fundamental importance across several areas of physics and engineering, from the design of complex aerospace technologies to the weather forecast and mitigation of natural disasters. The **Navier–Stokes equations** are employed to model viscous fluid flows and consist of **momentum balance** and **mass continuity equations**, complemented with the appropriate boundary conditions.

The **fluid incompressibility** can be assumed in a wide range of applications, especially those for low Reynolds number flows, which implies that the mass continuity equation reduces to a **null divergence constraint** for the velocity field. However, the incompressibility condition poses challenging issues in obtaining physically sound and accurate numerical solutions for the Navier–Stokes equations. Indeed, the **div-grad duality** arising from the velocity–pressure coupling has been the subject of extensive research for the past decades, aiming at the development of accurate and robust **discretisation techniques** for incompressible fluid flows.

## 2. List of cases

The table below summarises the test cases provided.

| Designation | Title                                                             | Tags                         |
|:------------|:------------------------------------------------------------------|:-----------------------------|
| **INSE_01** | _Periodic flow with decaying vortices (Taylor-Green flow)_        | Navier-Stokes equations, unsteady, two-dimensional, incompressible fluid, Newtonian fluid, Dirichlet boundary conditions |
| **INSE_02** | _Flow between rotating cylinders (Taylor-Couette flow)_           | Navier-Stokes equations, stationary, two-dimensional, incompressible fluid, Newtonian fluid, Dirichlet boundary conditions, Curved boundaries |
| **INSE_03** | _Flow between circular boundaries_                                | Navier-Stokes equations, stationary, two-dimensional, incompressible fluid, Newtonian fluid, Dirichlet boundary conditions, Curved boundaries |
| **INSE_04** | _Flow between rose-shaped boundaries_                             | Navier-Stokes equations, stationary, two-dimensional, incompressible fluid, Newtonian fluid, Dirichlet boundary conditions, Curved boundaries |
