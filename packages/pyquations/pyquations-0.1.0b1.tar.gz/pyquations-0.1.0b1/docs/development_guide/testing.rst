=======
Testing
=======

This article outlines the testing standards for the `pyquations` project. All contributors are expected to follow these guidelines to ensure the project maintains high-quality, reliable, and well-tested code.

Expectations for Testing
========================

All code must be accompanied by tests that meet the following expectations:

- **100% Test Coverage**: Every line of code must be covered by tests. The project enforces this requirement using `pytest-cov` with a coverage threshold of 100%. Pull requests that reduce test coverage will not be accepted.
- **Multiple Test Cases**: Write multiple test cases to cover a variety of scenarios, including edge cases and invalid inputs. Ensure that your tests validate both expected behavior and error handling.

Installing Test Dependencies
============================

The `pyquations` project uses `pytest` as the testing framework, along with `pytest-cov` for measuring test coverage. These tools are included in the `test` optional dependency group. To install the test dependencies, run:

.. code-block:: bash

    pip install -e .[test]

Running Tests Locally
=====================

To run the tests locally, use the following command:

.. code-block:: bash

    pytest

This will execute all the tests in the project and display the results.

Pull Requests
=============

The test suite runs automatically on pull requests. It utilizes a Python matrix to execute the tests and ensure compatibility with supported Python versions. If any tests fail, the pull request will be blocked until the issues are resolved.
