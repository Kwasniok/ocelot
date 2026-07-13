import numpy as np


def get_tilt_matrix(psi):
    """
    Return the rotation matrix for a tilt of angle ``psi`` around the s-axis.

    MAD-8 Eq. 9.7.
    """
    c = np.cos(psi)
    s = np.sin(psi)
    return np.array([
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ])
