# Contributing

Thank you for your interest in contributing to the repository. This document provides guidelines to ensure that contributions are consistent, maintainable, and aligned with the project's goals. All types of contributions are welcome, including:

* **Addition of benchmarks**: Propose and implement benchmark cases aligned with the project scope.
* **Refinement of code**: Refactor or optimise existing code while preserving functionality.
* **Enhancement of documentation**: Enhance or correct project documentation, including README, docstrings, and examples.
* **Resolution of issues**: Identify, report, and resolve issues in existing modules and scripts.

The simplest route is to check the contact details in the `README.md` file and **reaching out via email with your ideas or suggestions**. Alternatively, you may follow the standard GitHub contribution procedure outlined below.

1. **Fork the repository** and create a new branch for your feature or fix.
   ```bash
   git checkout -b my_branch
   ```
2. **Implement your changes** following the contributing guidelines.
3. **Test your code** to ensure it runs correctly and does not break existing functionality.
4. **Commit and push** your branch to your forked repository.
5. **Submit a pull request (PR)** to the `main` branch of the repository.

---

## Addition of benchmarks

Each benchmark case should follow the existing folder structure, where you should organise your files:

* `codes/` – Generated code in multiple programming languages.
* `meshes/` – Pre-generated meshes for the benchmark case.
* `scripts/` – Utilities for code generation, mesh generation, etc.
* `images/` – Images illustrating the benchmark.

Include a `README.md` with these sections:

* **Summary** – problem description.
* **Domain and meshes** – description and parameterisation (if applicable).
* **Model problem** – governing equations and parameters
* **Analytical/manufactured solution** – source terms, boundary conditions, and analytical parameters.
* **Case parameters** – user-defined parameters and suggested values.
* **Scripts and files** – description, usage (if applicable), requirements, and dependencies.
* **How to cite** – references where the benchmark case was originally published.


---

## Refinement of code/enhancement of documentation

Follow these coding style guidelines:

* Use **Markdown** syntax for all documentation files.
* Write **clean, readable, and consistent** Python code.
* Follow the **snake_case** convention for variable and function names.
* Include clear and concise **docstrings** in all scripts, classes, and functions.
* Keep the codebase **well-structured, organised, and thoroughly commented**.
* Adhere to the official **Python style guidelines** defined in [PEP 8](https://peps.python.org/pep-0008/).
* Ensure **backward compatibility** with existing modules whenever feasible.
* Introduce **external dependencies** only when strictly necessary.

---

## Resolution of issues

If you encounter an issue or wish to request a feature:

- Check the **Issues** tab to see if your problem has already been reported.
- If not, open a new issue and provide:
  - A clear title and description of the problem.
  - Steps to reproduce the issue, if applicable.
  - Relevant error messages, screenshots, and logs.
  - Suggest possible solutions or improvements.
