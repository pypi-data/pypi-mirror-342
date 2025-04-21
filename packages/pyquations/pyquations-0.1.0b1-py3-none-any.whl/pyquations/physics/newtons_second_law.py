def newtons_second_law(
    *,
    mass: float,
    acceleration: float,
    force: float,
) -> float:
    """Solve for one variable in Newton's second law of motion given the other
    two.

    The acceleration of an object depends on the mass of the object and the
    amount of force applied. [1]_

    .. math::

        F = m \\cdot a

    Where:

    - :math:`F` is the force in newtons (N).
    - :math:`m` is the mass in kilograms (kg).
    - :math:`a` is the acceleration in meters per second squared (m/s²).

    Newton's second law of motion pertains to the behavior of objects for
    which all existing forces are not balanced. The second law states that the
    acceleration of an object is dependent upon two variables - the net force
    acting upon the object and the mass of the object. The acceleration of an
    object depends directly upon the net force acting upon the object, and
    inversely upon the mass of the object. As the force acting upon an object
    is increased, the acceleration of the object is increased. As the mass of
    an object is increased, the acceleration of the object is decreased. [2]_

    .. note::
        Provide 2 of the 3 parameters. The method will solve for the third.

    Args:
        mass (float): The mass of the object in kilograms. Must be
            non-negative.
        acceleration (float): The acceleration of the object in meters per
            second squared.
        force (float): The force exerted on the object in newtons. Must be
            non-negative.

    Returns:
        float: The force exerted on the object in newtons (N).

    Raises:
        ValueError: If there aren't exactly 2 parameters provided.
        ValueError: If mass is provided and is not greater than zero.
        ValueError: If acceleration is provided and is not greater than zero.
        ValueError: If force is provided and is negative.

    Examples:
        Solve for Force

        >>> newtons_second_law(mass=10, acceleration=2)
        20.0

        Solve for Mass

        >>> newtons_second_law(force=20, acceleration=2)
        10.0

        Solve for Acceleration

        >>> newtons_second_law(force=20, mass=10)
        2.0

    References:
        .. [1] "Newton's Second Law: Force", NASA.
            https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/newtons-laws-of-motion/#newtons-second-law-force
        .. [2] "Newton's Second Law of Motion", The Physics Classroom.
            https://www.physicsclassroom.com/class/newtlaws/lesson-3/newton-s-second-law
    """
    # Validate that exactly two parameters are provided
    provided: list = [mass, acceleration, force]
    if provided.count(None) != 1:
        raise ValueError("Exactly two parameters must be provided.")

    # Validate the provided parameters
    if mass is not None and mass <= 0:
        raise ValueError("Mass must be greater than zero.")
    if acceleration is not None and acceleration <= 0:
        raise ValueError("Acceleration must be greater than zero.")
    if force is not None and force < 0:
        raise ValueError("Force must be non-negative.")

    # Perform the calculations
    if mass is None:
        return force / acceleration
    if acceleration is None:
        return force / mass
    return mass * acceleration
