import cmath
from typing import Tuple


def quadratic_formula(a: float, b: float, c: float) -> Tuple[complex, complex]:
    """Calculates the roots of a quadratic equation.

    The quadratic formula is a closed-form expression describing the solutions
    of a quadratic equation. Other ways of solving quadratic equations, such
    as completing the square, yield the same solutions. [1]_

    .. math::

        ax^2 + bx + c = 0

    Args:
        a (float): Coefficient of the quadratic term (x^2). Must not be zero.
        b (float): Coefficient of the linear term (x).
        c (float): Constant term.

    Returns:
        Tuple[complex, complex]: A tuple containing two roots of the quadratic
            equation. The roots may be real or complex numbers depending on the
            discriminant.

    Raises:
        ValueError: If 'a' is zero, as this would not represent a quadratic
            equation.

    Examples:
        >>> quadratic_formula(1, -3, 2)
        (2.0, 1.0)

        >>> quadratic_formula(1, 2, 5)
        (-1+2j, -1-2j)

    Resources:
        - `Calculator Soup: Quadratic Formula <https://www.calculatorsoup.com/
          calculators/algebra/quadratic-formula-calculator.php>`_

    References:
        .. [1] "Quadratic Formula", Wikipedia.
            https://en.wikipedia.org/wiki/Quadratic_formula
    """
    if a == 0:
        raise ValueError(
            "Coefficient 'a' must not be zero for a quadratic equation.",
        )

    discriminant: float = (b**2) - (4 * a * c)
    sol1: complex = (-b + cmath.sqrt(discriminant)) / (2 * a)
    sol2: complex = (-b - cmath.sqrt(discriminant)) / (2 * a)

    return sol1, sol2
