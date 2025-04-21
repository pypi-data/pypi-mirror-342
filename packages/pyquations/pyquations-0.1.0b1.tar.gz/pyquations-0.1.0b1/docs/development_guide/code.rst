====
Code
====

This article outlines the code standards for the `pyquations` project to ensure consistency, maintainability, and high-quality contributions. All contributors are expected to follow these guidelines when submitting code.

Code Expectations
=================

- Run the linters and formatters locally before submitting a pull request to catch issues early.
- Ensure that all new code passes MegaLinter checks without warnings or errors.
- Follow the project's strict typing requirements.

Installing Development Tools
============================

All the tools required are included in the `dev` optional dependency group. To install them, run :code:`pip install -e .[dev]`. These may be installed in your IDE, or you can run them from the command line.

Linters and Formatters
======================

The `pyquations` project uses several tools to enforce code quality and formatting. These tools are configured in the `pyproject.toml` file, which centralizes the configuration for linters, formatters, and other development tools. This means contributors do not need to configure these tools manually; they will automatically adhere to the project's standards when run.

Ruff
----
   
- Ruff is used as both a linter and a formatter for this project. It enforces PEP 8 compliance and other Python best practices.
- To run Ruff, simply execute :code:`ruff check pyquations`.

Mypy
----
   
- Mypy is used to enforce strict typing throughout the project. Contributors must ensure that all code is type-annotated and passes Mypy checks. The `pyproject.toml` file enables strict mode and additional warnings, such as `warn_unused_ignores` and `warn_unreachable`.
- To run Mypy, simply execute :code:`mypy pyquations`.

Strict Typing
=============

The `pyquations` project enforces strict typing to improve code clarity and reduce runtime errors. All functions must include type annotations, and contributors should address any typing issues flagged by Mypy. This ensures that the codebase remains robust and easy to maintain.

Pull Requests (MegaLinter)
==========================

The `pyquations` project uses MegaLinter to enforce code quality standards during pull requests. MegaLinter is configured to only check new or modified code in a pull request, ensuring that contributors are not burdened with fixing unrelated legacy issues. However, all new code must meet the project's quality standards, and no warnings are allowed for new contributions.

When a pull request is opened, MegaLinter automatically runs checks on the modified files. These checks include linting, formatting, and typing validation. If any issues are found, the pull request will fail, and contributors must resolve the issues before the code can be merged.
  