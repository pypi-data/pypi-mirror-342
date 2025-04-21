=============
Documentation
=============

This article outlines the documentation standards for the `pyquations` project. All contributors are expected to follow these guidelines to ensure the project maintains clear, consistent, and comprehensive documentation.

Documentation Expectations
==========================

All contributions to the `pyquations` project must include proper documentation. This includes:

- Adding or updating docstrings for all new or modified functions.
- Ensuring that the documentation is clear, concise, and follows the Google-style format.
- Providing examples and references where applicable.

Installing Documentation Dependencies
=====================================

The `pyquations` project uses Sphinx to generate documentation. The required tools are included in the `docs` optional dependency group. To install the documentation dependencies, run:

.. code-block:: bash

    pip install -e .[docs]

This will install all the necessary tools to build and maintain the documentation.

Writing Docstrings
==================

All functions in the `pyquations` project must include Google-style docstrings. These docstrings provide detailed information about the function's purpose, parameters, return values, errors raised, and usage examples. Following this standard ensures that the documentation is consistent and easy to understand.

Each function's docstring should include the following sections when applicable:

1. **Description**: A brief overview of what the function does.
2. **Args**: A list of all parameters, including their types, default values (if any), and a short description of their purpose.
3. **Returns**:  A description of the return value, including its type.
4. **Raises**: A list of exceptions the function may raise, along with the conditions under which they are raised.
5. **Examples**: One or more usage examples demonstrating how to call the function.
6. **References**: Links or citations to external resources or related documentation.

Template Docstring
------------------

.. code-block:: python

    def example_function(param1: int, param2: str = "default") -> bool:
        """Brief description of the function.

        Brief description of the equations with sources if used. [1]_

        .. math::

            Equation here

        Where:

        - variable1: Description of variable1.
        - variable2: Description of variable2.
  
        Additional details and sited sources (optional).

        Args:
            param1 (int): Description of param1.
            param2 (str, optional): Description of param2. Defaults to "default".

        Returns:
            bool: Description of the return value.

        Raises:
            ValueError: Description of the error condition.

        Examples:
            >>> example_function(1, "test")
            True

        Resources:
            - Link to helpful resources or documentation.

        References:
            .. [1] Article Title, Source.
                Link to article.
        """
        pass

Building the Documentation Locally
==================================

To build the documentation locally, use the `docs/build_docs.py` script. This script generates the HTML documentation using Sphinx.

Run the following command to build the documentation:

.. code-block:: bash

    python docs/build_docs.py

Once the build is complete, open the generated HTML files in the `docs/_build/html` folder. This will allow you to preview the documentation and ensure that it renders correctly.

Pull Requests
=============

The documentation is automatically built and validated on pull requests. If any warnings or errors are detected during the build process, the pull request will be blocked until they are resolved. This ensures that all contributions meet the project's documentation standards before being merged.