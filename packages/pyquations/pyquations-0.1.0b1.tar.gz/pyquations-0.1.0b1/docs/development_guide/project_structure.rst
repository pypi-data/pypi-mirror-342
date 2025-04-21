=================
Project Structure
=================

The `pyquations` project is designed to be intuitive and modular, making it easy to navigate, extend, and use. This document outlines the structure of the project and provides guidelines for adding new packages and modules.

Organization
============

The project is organized by topic, with each topic represented as a package (e.g., `algebra`, `physics`, `geometry`). Each equation is implemented in its own module (a single `.py` file) within the appropriate package. This structure ensures that the codebase remains clean and that equations are easy to locate and maintain.

Adding a New Equation
=====================

When adding a new equation, create a new module (a `.py` file) in the appropriate package based on the topic. For example, if the equation belongs to algebra, it should be added to the `algebra` package. This modular approach keeps the project organized and makes it easier to extend.

Adding a New Package
====================

When adding a new package, create a new directory with the package name. Inside this directory, create an `__init__.py` file to make it a package. From there, add the necessary modules (equations) as `.py` files.

Organizing Imports
===================

To make the project user-friendly, all new equations must be imported in the appropriate `__init__.py` files:

1. **Module-Level Import**: Add the equation to the `__init__.py` file of the package where the module resides. This allows users to import the equation from the package directly.
2. **Top-Level Import**: Add the equation to the main `pyquations/__init__.py` file. This allows users to import the equation directly from the `pyquations` package.
3. **For New Packages**: Ensure that the package is also imported in the main `pyquations/__init__.py` file. This way, users can access the new package and its equations directly from the top level.

.. tip::
    Utilize the `__all__` list in the `__init__.py` files.

By following this structure, users can import equations in multiple ways, depending on their needs, while maintaining a clean and consistent project organization.