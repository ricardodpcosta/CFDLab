# Contributing Guidelines

Thank you for your interest in contributing to **CFD-BenchLab**!  
We welcome all contributions, including new benchmark cases, code improvements, bug fixes, and documentation enhancements.

---

## 📌 How to Contribute

### 1. Reporting Issues
- Check the **Issues** tab to see if your problem has already been reported.
- If not, open a new issue with:
  - A clear description of the problem.
  - Steps to reproduce (if applicable).
  - Relevant error messages, screenshots, or logs.

### 2. Adding a New Test Case
Each new test case should follow the existing folder structure:

**Requirements:**
- A `README.md` with:
  - Problem description
  - Analytical solution (if available)
  - Governing equations and parameters
  - Mesh information
  - Usage instructions
  - References
- All relevant meshes, scripts, and codes.
- If possible, provide a manufactured or exact analytical solution.

### 3. Improving Existing Cases
- Submit changes via a pull request (PR).
- Explain clearly **what** you changed and **why**.
- Keep documentation clear and consistent with existing cases.

### 4. Style Guidelines
- Use **Markdown** for documentation.
- Follow consistent variable naming and directory structure.
- For code:
  - Keep it clean and well-commented.
  - Use descriptive function and variable names.
  - Maintain compatibility with existing scripts when possible.

---

## 🚀 Submitting a Pull Request
1. **Fork** the repository.
2. Create a new branch for your contribution:
   ```bash
   git checkout -b feature/new-case


   📜 License and Acknowledgement

   By contributing, you agree that your work will be licensed under the MIT License.
   If your contribution is based on published work, please provide a reference in the case’s README file.

   🙌 Acknowledgements

   We greatly appreciate contributions from the community.
   Your feedback and participation help make CFD-BenchLab a valuable resource for the CFD community.


   
