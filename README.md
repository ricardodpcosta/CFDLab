# CFD-BenchLab

**A curated collection of benchmarking test cases with analytical solutions for the design, testing, comparison, and verification of numerical schemes.**

---

## Overview

CFD-BenchLab is a repository dedicated to providing rigorous test cases for verification and benchmarking of numerical schemes in computational fluid dynamics (CFD). Each case includes analytical solutions, source terms, boundary conditions, and meshes. Scripts and tools are also provided when necessary to facilitate the reproducibility of results and the manipulation of the test cases.

This open laboratory aims to be a valuable resource for researchers, engineers, and students developing, testing, and comparing numerical schemes for fluid flow simulations.

---

## Objectives

- Collect benchmarking cases with known or manufactured analytical solutions.
- Enable quantitative verification through convergence and stability analysis.
- Provide an organised environment for comparative testing and benchmarking.
- Promote reproducibility and transparency in numerical schemes design.
- Offer educational material for teaching and training in numerical methods.

---

## Repository Structure

```
CFD-BenchLab/
│
├── category/ # Model category
│ ├── case/ # Test case
│ │ ├── analytical/ # Analytical formulas
│ │ ├── scripts/ # Scripts and tools
│ │ ├── meshes/ # Mesh files
│ │ ├── docs/ # Relevant documentation
│ │ └── README.md # Case description
│ └── ...
│
├── LICENSE.md
├── CONTRIBUTING.md
└── README.md
```

---

## How to Use

1. Select the test case relevant to your research based on the model category.
2. Read the provided case description and review the associated documentation.
3. Use the provided analytical formulas and meshes to run simulations with your code.
4. Revise the scripts to manipulate the test case and generate the analytical formulas.
5. Contribute new cases or improvements by following the guidelines in `CONTRIBUTING.md`.

---

## Contribution

Contributions are warmly welcome! If you would like to add new test cases, improve scripts, or fix issues, please see the `CONTRIBUTING.md` file for instructions on how to get involved.

---

## License

This project is licensed under the MIT License — see the `LICENSE` file for details.

---

## Contact

Ricardo Costa  
[https://ricardodpcosta.github.io/](https://ricardodpcosta.github.io/)  
ricardodpcosta@example.com

---

Thank you for visiting CFD-BenchLab!  
We hope this repository helps advance the state of the art in numerical validation for CFD.

