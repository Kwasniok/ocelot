import numpy as np
import pytest

from ocelot.cpbd.beam import Particle
from ocelot.cpbd.elements import Drift
from ocelot.cpbd.transformations.exact_drift import ExactDriftTM
from ocelot.cpbd.transformations.transfer_map import TransferMap


def _track_once(particle):
    drift = Drift(l=2.0, tm=ExactDriftTM)
    drift.tms[0].apply(particle)


@pytest.mark.parametrize(
    ("particle", "after_one", "after_two"),
    [
        (
            Particle(),
            (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
            (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        ),
        (
            Particle(p=-0.001, E=0.1),
            (0.0, 0.0, 0.0, 0.0, 5.230379184e-08, -0.001, 0.1),
            (0.0, 0.0, 0.0, 0.0, 1.046075837e-07, -0.001, 0.1),
        ),
        (
            Particle(x=-0.3, px=0.1, y=0.7, py=-0.25, p=0.0, E=0.1),
            (-0.09233034734, 0.1, 0.1808258683, -0.25, 0.07669752797, 0.0, 0.1),
            (0.1153393053, 0.1, -0.3383482633, -0.25, 0.1533950559, 0.0, 0.1),
        ),
        (
            Particle(x=0.1, px=-0.15, y=-0.2, py=-0.07, tau=0.01, p=0.03, E=0.1),
            (-0.195097717, -0.15, -0.3377122679, -0.07, 0.0363372301, 0.03, 0.1),
            (-0.490195434, -0.15, -0.4754245359, -0.07, 0.06267446021, 0.03, 0.1),
        ),
    ],
)
def test_exact_drift_tracks_madx_reference_values_with_ocelot_tau_sign(particle, after_one, after_two):
    _track_once(particle)
    actual_one = (particle.x, particle.px, particle.y, particle.py, particle.tau, particle.p, particle.E)
    np.testing.assert_allclose(actual_one, after_one, rtol=0.0, atol=1e-10)

    _track_once(particle)
    actual_two = (particle.x, particle.px, particle.y, particle.py, particle.tau, particle.p, particle.E)
    np.testing.assert_allclose(actual_two, after_two, rtol=0.0, atol=1e-10)


def test_exact_drift_keeps_transfer_map_for_linear_optics():
    drift = Drift(l=2.0, tm=ExactDriftTM)
    reference = Drift(l=2.0)

    assert isinstance(drift.tms[0], ExactDriftTM)
    assert isinstance(drift.first_order_tms[0], TransferMap)
    np.testing.assert_allclose(drift.R(energy=0.1)[0], reference.R(energy=0.1)[0])


def test_exact_drift_rejects_non_real_longitudinal_momentum():
    particle = Particle(px=2.0, E=0.1)
    drift = Drift(l=2.0, tm=ExactDriftTM)

    with pytest.raises(ValueError, match="non-real longitudinal momentum"):
        drift.tms[0].apply(particle)
