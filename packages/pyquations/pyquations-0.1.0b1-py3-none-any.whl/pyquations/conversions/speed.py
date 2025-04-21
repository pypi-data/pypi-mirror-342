def speed(speed: float, from_unit: str, to_unit: str) -> float:
    """Converts a speed value from one unit to another.

    Supported units:
        - "mph" (miles per hour)
        - "kph" (kilometers per hour)
        - "mps" (meters per second)
        - "fps" (feet per second)
        - "knots" (nautical miles per hour)
        - "cm/s" (centimeters per second)
        - "ips" (inches per second)

    Args:
        speed (float): The speed value to convert. Must be non-negative.
        from_unit (str): The unit of the input speed. Must be one of the
            supported units.
        to_unit (str): The unit to convert the speed to. Must be one of the
            supported units.

    Returns:
        float: The converted speed value.

    Raises:
        ValueError: If the speed is negative or if the units are invalid.

    Examples:
        >>> speed(60, "mph", "kph")
        96.56064

        >>> speed(100, "kph", "mps")
        27.7778

        >>> speed(30, "fps", "ips")
        360.0

        >>> speed(10, "mps", "knots")
        19.4384
    """
    if speed < 0:
        raise ValueError("Speed must be non-negative.")

    # Conversion factors
    conversion_factors = {
        ("mph", "kph"): 1.60934,
        ("kph", "mph"): 1 / 1.60934,
        ("mph", "mps"): 0.44704,
        ("mps", "mph"): 1 / 0.44704,
        ("mph", "fps"): 1.46667,
        ("fps", "mph"): 1 / 1.46667,
        ("mph", "knots"): 0.868976,
        ("knots", "mph"): 1 / 0.868976,
        ("kph", "mps"): 0.277778,
        ("mps", "kph"): 1 / 0.277778,
        ("kph", "knots"): 0.539957,
        ("knots", "kph"): 1 / 0.539957,
        ("mps", "fps"): 3.28084,
        ("fps", "mps"): 1 / 3.28084,
        ("mps", "cm/s"): 100,
        ("cm/s", "mps"): 0.01,
        ("fps", "ips"): 12,
        ("ips", "fps"): 1 / 12,
    }

    if from_unit == to_unit:
        return speed

    try:
        factor = conversion_factors[(from_unit, to_unit)]
        return speed * factor
    except KeyError:
        raise ValueError(
            f"Invalid conversion from '{from_unit}' to '{to_unit}'. "
            "Supported units are "
            f"'mph', 'kph', 'mps', 'fps', 'knots', 'cm/s', and 'ips'."
        )
