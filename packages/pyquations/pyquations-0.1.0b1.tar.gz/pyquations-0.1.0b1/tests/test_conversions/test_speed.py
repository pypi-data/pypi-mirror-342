import pytest

from pyquations.conversions.speed import speed


@pytest.mark.parametrize(
    "speed_value, from_unit, to_unit, expected",
    [
        (60, "mph", "kph", 96.56064),
        (100, "kph", "mph", 62.1371),
        (10, "mps", "fps", 32.8084),
        (5, "fps", "ips", 60.0),
        (100, "kph", "mps", 27.7778),
        (50, "mph", "mph", 50),
        (0, "mph", "kph", 0),
        (10, "knots", "kph", 18.52),
        (20, "cm/s", "mps", 0.2),
        (1, "ips", "fps", 1 / 12),
    ],
)
def test_speed(speed_value, from_unit, to_unit, expected):
    assert speed(
        speed_value,
        from_unit,
        to_unit,
    ) == pytest.approx(
        expected,
        rel=1e-4,
    )


@pytest.mark.parametrize(
    "speed_value, from_unit, to_unit",
    [
        (-10, "mph", "kph"),
        (50, "mph", "invalid_unit"),
        (50, "invalid_unit", "kph"),
    ],
)
def test_speed_invalid(speed_value, from_unit, to_unit):
    with pytest.raises(ValueError):
        speed(speed_value, from_unit, to_unit)
