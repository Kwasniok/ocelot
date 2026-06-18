import numpy as np
import pytest

from ocelot.rad.spline_py import cspline_coef, moment, moment_numba


def test_spline_moments_define_interval_coefficients():
    x = np.linspace(0.0, 2.5, 33)
    y = np.sin(1.3 * x) + 0.05 * x**2

    moments = moment(x, y)
    a, b, c, d, z = cspline_coef(x, y)
    step = np.diff(x)

    np.testing.assert_allclose(
        a,
        np.diff(moments) / (6.0 * step),
        rtol=0.0,
        atol=0.0,
    )
    np.testing.assert_allclose(
        b,
        moments[:-1] / 2.0,
        rtol=0.0,
        atol=0.0,
    )
    np.testing.assert_allclose(
        c,
        np.diff(y) / step
        - moments[1:] * step / 6.0
        - moments[:-1] * step / 3.0,
        rtol=0.0,
        atol=0.0,
    )
    np.testing.assert_array_equal(d, y[:-1])
    np.testing.assert_array_equal(z, x[:-1])


@pytest.mark.skipif(moment_numba is None, reason="Numba is unavailable")
def test_numba_spline_moments_match_python_implementation():
    x = np.linspace(-1.0, 3.0, 257)
    y = 0.03 * np.cos(2.1 * x) - 0.02 * x

    np.testing.assert_array_equal(moment_numba(x, y), moment(x, y))
