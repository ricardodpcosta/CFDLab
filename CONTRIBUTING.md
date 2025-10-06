# Contributing guidelines

Thank you for your interest in contributing to the repository. All types of contributions are welcome, including:

* Addition of benchmark cases.
* Refinement of scripts.
* Enhancement of documentation.
* Resolution of issues.

The simplest route is to check the contact details in the `README.md` file and **send an email with your suggestions and proposals**. Alternatively, you can always follow the usual GitHub route described below.

---

### 1. Addition of benchmark cases

Each benchmark case should follow the existing folder structure.

Include a `README.md` with these sections:

* **Summary** – problem description.
* **Domain and meshes** – description and parameterisation (if applicable).
* **Model problem** – governing equations and parameters
* **Analytical/manufactured solution** – source terms, boundary conditions, and analytical parameters.
* **Case parameters** – user-defined parameters and suggested values.
* **Scripts and files** – description, usage (if applicable), requirements, and dependencies.
* **How to cite** – references where the benchmark case was originally published.

Organise your files in these folders:

* `codes/`
* `images/`
* `meshes/`
* `scripts/`

Follow these style guidelines:

* Use **Markdown** for documentation.
* Use descriptive and consistent **variable and function naming**.
* Keep code clean, organised, and well-commented.
* Maintain compatibility with existing scripts whenever possible.

---

### 2. Refinement of scripts/enhancement of documentation

* Submit changes via a **pull request** in GitHub.
* Explain **what** you changed and **why**.
* Keep it clear and consistent with the repository.

---

### 3. Resolution of issues

- Check the **Issues** tab to see if your problem has already been reported.
- If not, open a new issue with:
  - A clear description of the problem.
  - Steps to reproduce (if applicable).
  - Relevant error messages, screenshots, or logs.
