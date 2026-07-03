from ocelot.cpbd.tm_params.tm_params import TMParams


class ExactDriftParams(TMParams):
    """
    Geometry parameters for ``ExactDriftTM``.

    The exact drift map is algorithmic, so it only needs the wrapper-visible
    offsets and roll angle rather than a precomputed matrix.
    """

    def __init__(self, dx, dy, tilt):
        super().__init__()
        self.dx = dx
        self.dy = dy
        self.tilt = tilt
