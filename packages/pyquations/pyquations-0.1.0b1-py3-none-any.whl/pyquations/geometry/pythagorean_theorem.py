from math import sqrt


def pythagorean_theorem(a: float, b: float) -> float:
    """Calculates the length of the hypotenuse for a right triangle.

    The area of the square whose side is the hypotenuse is equal to the sum of
    the areas of the squares on the other two sides. [1]_

    .. math::

        c^2 = a^2 + b^2

    Where:

    - :math:`a` is the length of one leg of the triangle.
    - :math:`b` is the length of the other leg of the triangle.
    - :math:`c` is the length of the hypotenuse.

    Args:
        a (float): Length of one leg of the triangle. Must be non-negative.
        b (float): Length of the other leg of the triangle. Must be
            non-negative.

    Returns:
        float: The length of the hypotenuse.

    Raises:
        ValueError: If either 'a' or 'b' is not greater than 0.

    Examples:
        >>> pythagorean_theorem(3, 4)
        5.0

        >>> pythagorean_theorem(5, 12)
        13.0

        >>> pythagorean_theorem(8, 15)
        17.0

    Resources:
        - `Math is Fun: Pythagorean Theorem <https://www.mathsisfun.com/
          pythagoras.html>`_

    References:
        .. [1] "Pythagorean Theorem", Wikipedia.
            https://en.wikipedia.org/wiki/Pythagorean_theorem
    """
    if a <= 0 or b <= 0:
        raise ValueError(
            "Lengths of the triangle's legs must be greater than zero.",
        )

    return sqrt(a**2 + b**2)
