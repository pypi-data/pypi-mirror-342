import pytest

from pyquations.algebra.quadratic_formula import quadratic_formula


@pytest.mark.parametrize(
    "a, b, c, expected",
    [
        (1, -3, 2, ((2 + 0j), (1 + 0j))),
        (1, 2, 1, ((-1 + 0j), (-1 + 0j))),
        (1, 2, 5, ((-1 + 2j), (-1 - 2j))),
        (0, 2, 1, None),
        (1e6, -3e6, 2e6, ((2 + 0j), (1 + 0j))),
    ],
)
def test_quadratic_formula(a, b, c, expected):
    if expected is None:
        with pytest.raises(ValueError):
            quadratic_formula(a, b, c)
    else:
        result = quadratic_formula(a, b, c)
        assert result == pytest.approx(expected)
