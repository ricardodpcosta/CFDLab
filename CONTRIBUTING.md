# Contributing guidelines

Thank you for your interest in contributing to **CFDLab**!
We welcome all types of contributions, including:

* New benchmark cases.
* Code improvements.
* Bug fixes.
* Documentation enhancements.

To keep it simple, **write us an email with your thoughts**. Alternatively, you can always follow the usual GitHub process described below.

---

### 1. Reporting issues
- Check the **Issues** tab to see if your problem has already been reported.
- If not, open a new issue with:
  - A clear description of the problem.
  - Steps to reproduce (if applicable).
  - Relevant error messages, screenshots, or logs.

---

### 2. Adding a new benchmark case

Each new benchmark case should follow the existing folder structure.

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

---

### 3. Improving existing cases

* Submit changes via a **pull request**.
* Clearly explain **what** you changed and **why**.
* Keep documentation clear, consistent, and aligned with existing cases.

---

### 4. Style guidelines

* Use **Markdown** for documentation.
* Follow consistent **variable naming** and **directory structure**.
* For code contributions:

  * Keep code clean and well-commented
  * Use descriptive function and variable names
  * Maintain compatibility with existing scripts whenever possible
