import importlib

import numpy as np

from ocelot.common.globals import m_e_GeV, q_e
from ocelot.cpbd.beam import ParticleArray
from ocelot.rad.screen import Screen


radiation_module = importlib.import_module("ocelot.rad.radiation_py")


class CustomParticleArray(ParticleArray):
    pass


def test_coherent_radiation_accepts_particle_array_subclass_and_adds_segments_once(
    monkeypatch,
):
    p_array = CustomParticleArray(n=1)
    p_array.E = 1.0
    p_array.q_array[0] = q_e

    screen = Screen()
    screen.x = 0.0
    screen.y = 0.0
    screen.z = 100.0
    screen.size_x = 0.0
    screen.size_y = 0.0
    screen.nx = 1
    screen.ny = 1
    screen.start_energy = 1.0
    screen.end_energy = 1.0
    screen.num_energy = 1

    first_segment = np.zeros((9, 1))
    second_segment = np.zeros((9, 1))
    first_segment[0, 0] = 10.0
    second_segment[0, 0] = 1.0

    def fake_track4rad_beam(*args, **kwargs):
        return (
            [first_segment, second_segment],
            [2.0 * m_e_GeV, 3.0 * m_e_GeV],
        )

    phases_at_segment_start = []

    def fake_radiation_py(gamma, traj, segment_screen):
        phases_at_segment_start.append(segment_screen.arPhase.copy())
        segment_screen.arReEx += traj[0]
        segment_screen.arPhase += 0.25

    monkeypatch.setattr(
        radiation_module,
        "track4rad_beam",
        fake_track4rad_beam,
    )
    monkeypatch.setattr(radiation_module, "radiation_py", fake_radiation_py)
    monkeypatch.setattr(
        radiation_module,
        "_trajectory_start_mm",
        lambda trajectory: (0.0, 0.0, 0.0),
    )

    result = radiation_module.coherent_radiation(
        lat=object(),
        screen=screen,
        p_array=p_array,
        verbose=False,
    )

    # Desired segment-wise weighted sum:
    # gamma_1 * field_1 + gamma_2 * field_2 = 2 * 10 + 3 * 1.
    # The previous cumulative implementation produced
    # 2 * 10 + 3 * (10 + 1) = 53.
    np.testing.assert_allclose(result.arReEx, [23.0])
    np.testing.assert_allclose(phases_at_segment_start[0], [0.0])
    np.testing.assert_allclose(phases_at_segment_start[1], [0.25])
