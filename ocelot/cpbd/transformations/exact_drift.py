import functools

import numpy as np

from ocelot.common.globals import m_e_GeV
from ocelot.cpbd.elements.element import Element
from ocelot.cpbd.tm_utils import transform_vec_ent, transform_vec_ext
from ocelot.cpbd.transformations.transformation import Transformation, TMTypes


@functools.lru_cache(maxsize=1024)
def _energy_parameters(energy: float):
    gamma = energy / m_e_GeV
    if gamma <= 1.0:
        raise ValueError("ExactDriftTM requires energy greater than the electron rest energy, or energy=0 for 4D drift.")
    gamma2 = gamma * gamma
    beta = np.sqrt(1.0 - 1.0 / gamma2)
    ibeta = 1.0 / beta
    igammabeta2 = 1.0 / (gamma2 - 1.0)
    return ibeta, igammabeta2


class ExactDriftTM(Transformation):
    """
    Exact field-free drift tracking for Ocelot coordinates.

    The map uses the full longitudinal momentum in a drift instead of the
    linear or second-order path-length approximation. It tracks arrays with
    Ocelot coordinates ``(x, px/p0, y, py/p0, tau, dE/(p0*c))``. For
    ``energy=0`` it falls back to the usual 4D linear drift.

    Original exact-drift implementation and MAD-X comparison tests by
    Nikita Kuklev, 2020.
    """

    @classmethod
    def from_element(cls, element: Element, tm_type: TMTypes = TMTypes.MAIN, delta_l=None, **params):
        return cls.create(main_tm_params_func=element.create_exact_drift_main_params,
                          delta_e_func=element.create_delta_e,
                          tm_type=tm_type, length=element.l, delta_length=delta_l)

    def map_function(self, X, energy: float):
        params = self.get_params(energy)
        length = self.delta_length if self.delta_length is not None else self.length

        if params.dx != 0.0 or params.dy != 0.0 or params.tilt != 0.0:
            X = transform_vec_ent(X, params.dx, params.dy, params.tilt)
        self._drift(X, energy, length)
        if params.dx != 0.0 or params.dy != 0.0 or params.tilt != 0.0:
            X = transform_vec_ext(X, params.dx, params.dy, params.tilt)
        return X

    @staticmethod
    def _drift(X, energy: float, length: float):
        if energy == 0.0:
            X[0] += X[1] * length
            X[2] += X[3] * length
            return

        ibeta, igammabeta2 = _energy_parameters(float(energy))
        ibeta_de = ibeta + X[5]
        longitudinal_momentum2 = ibeta_de * ibeta_de - X[1] * X[1] - X[3] * X[3] - igammabeta2
        if np.any(longitudinal_momentum2 <= 0.0):
            raise ValueError("ExactDriftTM received particle coordinates with non-real longitudinal momentum.")

        inv_pz = 1.0 / np.sqrt(longitudinal_momentum2)
        X[0] += X[1] * length * inv_pz
        X[2] += X[3] * length * inv_pz
        X[4] -= length * (ibeta - ibeta_de * inv_pz)
