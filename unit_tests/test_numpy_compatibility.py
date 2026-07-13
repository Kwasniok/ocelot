import numpy as np


def test_math_helpers_use_supported_numpy_dtypes():
    from ocelot.common.math_op import bin_scale, conj_sym

    result = conj_sym([1, 2 + 3j, 3, 4])

    np.testing.assert_array_equal(result, [1, 2 + 3j, 3, 2 - 3j])
    np.testing.assert_array_equal(bin_scale(np.arange(10.0), 2), [1, 3, 5, 7, 9])


def test_response_matrix_set_membership_without_in1d(monkeypatch):
    from ocelot.cpbd.response_matrix import ResponseMatrix, ResponseMatrixJSON

    monkeypatch.delattr(np, "in1d", raising=False)

    response = ResponseMatrixJSON()
    response.cor_names = ["c1", "c2", "c3"]
    response.bpm_names = ["b1", "b2"]
    response.matrix = np.arange(12.0).reshape(4, 3)

    selected = response.extract(["c1", "c3"], ["b2"])
    np.testing.assert_array_equal(selected, [[3, 5], [9, 11]])

    replacement = np.full((2, 2), -1.0)
    response.inject(["c1", "c3"], ["b2"], replacement)
    np.testing.assert_array_equal(response.extract(["c1", "c3"], ["b2"]), replacement)
    response.compare(response)

    dataframe_response = ResponseMatrix()
    dataframe_response.cor_names = response.cor_names
    dataframe_response.bpm_names = response.bpm_names
    dataframe_response.matrix = response.matrix
    dataframe_response.compare(dataframe_response)


def test_fel_ptap_at_zero_returns_nan():
    from ocelot.rad.fel import FelParameters

    parameters = FelParameters()
    parameters.P_sn = np.array([1.0, 2.0])

    assert np.isnan(parameters.Ptap(z=0)).all()


def test_optics_signals_use_complex_dtype():
    from ocelot.optics.utils import Signal, Signal3D

    assert np.issubdtype(Signal().f.dtype, np.complexfloating)
    assert np.issubdtype(Signal3D().f.dtype, np.complexfloating)


def test_cut_lattice_accepts_fractional_cell_count():
    from ocelot.adaptors.genesis import cut_lattice
    from ocelot.cpbd.elements import Drift
    from ocelot.cpbd.magnetic_lattice import MagneticLattice

    lattice = MagneticLattice(tuple(Drift(l=1.0, eid=f"d{i}") for i in range(4)))

    trimmed = cut_lattice(lattice, 1.2, elem_in_cell=1)

    assert [element.id for element in trimmed.sequence] == ["d2", "d3"]
