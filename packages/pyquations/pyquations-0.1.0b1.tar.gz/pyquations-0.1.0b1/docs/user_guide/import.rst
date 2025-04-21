==============
Import Options
==============

Pyquations provides flexible options for imports. Choose the method that best suits your needs.

Option 1: Import Everything
===========================
Import the entire package to access all equations.

.. code-block:: python

   import pyquations

   # Call a function directly
   pyquations.quadratic_formula(1, 2, 3)

   # Or access it via the algebra package
   pyquations.algebra.quadratic_formula(1, 2, 3)

Option 2: Import a Specific Package
===================================
If you only need a specific package, you can import it directly.

.. code-block:: python

   import pyquations.algebra as algebra

   algebra.quadratic_formula(1, 2, 3)

Option 3: Import Specific Module
================================
If you only need specific equations, you can import them directly.

.. code-block:: python

   from pyquations import quadratic_formula

   quadratic_formula(1, 2, 3)

.. code-block:: python

   from pyquations.algebra import quadratic_formula

   quadratic_formula(1, 2, 3)