===============
Release Process
===============

The `pyquations` project uses an automated release process. All releases are made from the `main` branch, and the GitHub release notes are automatically populated based on the titles of pull requests included in the release. Once a release is created, the CI workflow publishes the package to PyPI using the tag version making it available for installation. Additionally, the CI workflow rebuilds and updates the documentation site to reflect the latest changes, ensuring that users have access to up-to-date information about the project.