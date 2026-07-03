from ocelot.cpbd.elements.magnet import Magnet
from ocelot.cpbd.tm_params.exact_drift_params import ExactDriftParams


class DriftAtom(Magnet):
    """
    drift - free space
    l - length of drift in [m]
    """

    def __init__(self, l=0., eid=None, **kwargs):
        super().__init__(eid, **kwargs)
        self.l = l

    def create_exact_drift_main_params(self, energy: float, delta_length: float = None) -> ExactDriftParams:
        return ExactDriftParams(dx=self.dx, dy=self.dy, tilt=self.tilt)

    def __str__(self):
        s = 'Drift('
        s += 'l=%7.5f, ' % self.l if self.l != 0. else ""
        s += 'eid="' + str(self.id) + '")' if self.id is not None else ")"
        return s
