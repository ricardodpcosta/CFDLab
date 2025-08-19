# CFDLab

___A curated collection of benchmarking test cases with analytical solutions for the design, testing, and verification of numerical codes in computational fluid dynamics and thermodynamics.___

---

## Overview

CFDLab is a repository dedicated to providing rigorous, well-documented test cases for verification and benchmarking of numerical schemes in computational fluid dynamics (CFD). Each case includes analytical solutions, source terms, boundary conditions, and meshes. Scripts and tools are also supplied to facilitate the reproducibility and the manipulation of the test cases.

_This open laboratory aims to be a valuable resource for researchers, engineers, and students developing, testing, and verifying numerical codes for heat transfer and fluid flow simulations._

---

## Objectives

- **Collect** benchmarking cases with known or manufactured analytical solutions.
- **Enable** quantitative verification through convergence and stability analysis.
- **Provide** an organised framework for comparative testing and benchmarking.
- **Promote** reproducibility and transparency in numerical schemes design.
- **Support** education and training in numerical methods for fluid flow and heat transfer.

---

## Repository Structure

```
CFD-BenchLab/
│
├── category/           # Model categories (e.g., conjugate heat transfer, incompressible flows, etc.)
│ ├── case/             # Specific benchmark case
│ │ ├── codes/          # Generated code in multiple programming languages
│ │ ├── meshes/         # Pre-generated meshes for the case
│ │ ├── scripts/        # Utilities for code generation, mesh generation, etc.
│ │ └── README.md       # Case description
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

Contributions are warmly welcome! Whether by adding new benchmark cases, improving scripts, enhancing documentation, or fixing issues.
Please refer to the CONTRIBUTING.md file for detailed guidelines on how to get involved.

---

## License

This project is licensed under the MIT License with Author Credit and Citation Requirement — see the `LICENSE.md` file for details.

---

## Contact

📧 [Ricardo Costa](mailto:rcosta\@dep.uminho.pt)  
🌐 [https://ricardodpcosta.github.io/](https://ricardodpcosta.github.io/)  

---

## Acknowledgement

If you have used any test case or supplied material from this repository — in its original or modified form — in your research, please acknowledge the original work referenced in the case description when publishing your results. Your acknowledgement not only gives credit to the authors but also motivates us to continue improving and expanding this resource.

Lastly, we thank all contributors and users who helped improve and expand CFD-TestSuite. Your feedback, suggestions, and participation are essential in making it a valuable resource for the CFD community.
