from importlib import import_module

__all__ = [
    # Core containers.
    "Twiss", "Beam", "BeamArray", "twiss_iterable_to_df",
    "ParticleArray", "Particle",

    # Beam generation and conversion.
    "generate_parray", "generate_beam", "BeamFormFactor",
    "recalculate_ref_particle", "twiss_parray_slice", "parray2beam",
    "cov_matrix_from_twiss", "cov_matrix_to_parray", "optics_from_moments",
    "moments_from_parray", "gauss_from_twiss", "waterbag_from_twiss",
    "ellipse_from_twiss",

    # Beam analysis.
    "get_envelope", "get_current", "s_to_cur", "signal_to_spectrum",
    "slice_analysis", "slice_analysis_py", "slice_analysis_transverse", "SliceParameters",
    "global_slice_analysis_extended", "global_slice_analysis",
    "bunching_spectrum", "bunching_at_klist_2", "bunching_at_klist_py",
    "bunching_at_klist_np", "spectrum_to_z", "compute_bunching",
    "zero_pad_signal", "s2cur_auxil_py", "s2cur_auxil",

    # Beam utilities.
    "simple_filter", "interp1", "sortcols", "convmode_py", "convmode",
    "moments", "m_from_twiss", "beam_matching",

    # Common dependency alias kept for legacy star-import workflows.
    "np",
]

_LAZY_EXPORTS = {
    # Module aliases used by explicit imports such as
    # ``from ocelot.cpbd.beam import core``.
    "analysis": ("ocelot.cpbd.beam.analysis", None),
    "beam": ("ocelot.cpbd.beam.beam", None),
    "beam_utils": ("ocelot.cpbd.beam.beam_utils", None),
    "core": ("ocelot.cpbd.beam.core", None),
    "generator": ("ocelot.cpbd.beam.generator", None),
    "noise": ("ocelot.cpbd.beam.noise", None),
    "particle": ("ocelot.cpbd.beam.particle", None),

    "np": ("numpy", None),

    # Core containers.
    "Twiss": ("ocelot.cpbd.beam.core", "Twiss"),
    "Beam": ("ocelot.cpbd.beam.core", "Beam"),
    "BeamArray": ("ocelot.cpbd.beam.core", "BeamArray"),
    "twiss_iterable_to_df": ("ocelot.cpbd.beam.core", "twiss_iterable_to_df"),
    "ParticleArray": ("ocelot.cpbd.beam.particle", "ParticleArray"),
    "Particle": ("ocelot.cpbd.beam.particle", "Particle"),

    # Beam generation and conversion.
    "generate_parray": ("ocelot.cpbd.beam.generator", "generate_parray"),
    "generate_beam": ("ocelot.cpbd.beam.generator", "generate_beam"),
    "BeamFormFactor": ("ocelot.cpbd.beam.beam", "BeamFormFactor"),
    "recalculate_ref_particle": ("ocelot.cpbd.beam.beam", "recalculate_ref_particle"),
    "twiss_parray_slice": ("ocelot.cpbd.beam.beam", "twiss_parray_slice"),
    "parray2beam": ("ocelot.cpbd.beam.beam", "parray2beam"),
    "cov_matrix_from_twiss": ("ocelot.cpbd.beam.beam", "cov_matrix_from_twiss"),
    "cov_matrix_to_parray": ("ocelot.cpbd.beam.beam", "cov_matrix_to_parray"),
    "optics_from_moments": ("ocelot.cpbd.beam.beam", "optics_from_moments"),
    "moments_from_parray": ("ocelot.cpbd.beam.beam", "moments_from_parray"),
    "gauss_from_twiss": ("ocelot.cpbd.beam.beam", "gauss_from_twiss"),
    "waterbag_from_twiss": ("ocelot.cpbd.beam.beam", "waterbag_from_twiss"),
    "ellipse_from_twiss": ("ocelot.cpbd.beam.beam", "ellipse_from_twiss"),

    # Beam analysis.
    "get_envelope": ("ocelot.cpbd.beam.analysis", "get_envelope"),
    "get_current": ("ocelot.cpbd.beam.analysis", "get_current"),
    "s_to_cur": ("ocelot.cpbd.beam.analysis", "s_to_cur"),
    "signal_to_spectrum": ("ocelot.cpbd.beam.analysis", "signal_to_spectrum"),
    "slice_analysis": ("ocelot.cpbd.beam.analysis", "slice_analysis"),
    "slice_analysis_py": ("ocelot.cpbd.beam.analysis", "slice_analysis_py"),
    "slice_analysis_transverse": ("ocelot.cpbd.beam.analysis", "slice_analysis_transverse"),
    "SliceParameters": ("ocelot.cpbd.beam.analysis", "SliceParameters"),
    "global_slice_analysis_extended": ("ocelot.cpbd.beam.analysis", "global_slice_analysis_extended"),
    "global_slice_analysis": ("ocelot.cpbd.beam.analysis", "global_slice_analysis"),
    "bunching_spectrum": ("ocelot.cpbd.beam.analysis", "bunching_spectrum"),
    "bunching_at_klist_2": ("ocelot.cpbd.beam.analysis", "bunching_at_klist_2"),
    "bunching_at_klist_py": ("ocelot.cpbd.beam.analysis", "bunching_at_klist_py"),
    "bunching_at_klist_np": ("ocelot.cpbd.beam.analysis", "bunching_at_klist_np"),
    "spectrum_to_z": ("ocelot.cpbd.beam.analysis", "spectrum_to_z"),
    "compute_bunching": ("ocelot.cpbd.beam.analysis", "compute_bunching"),
    "zero_pad_signal": ("ocelot.cpbd.beam.analysis", "zero_pad_signal"),
    "s2cur_auxil_py": ("ocelot.cpbd.beam.analysis", "s2cur_auxil_py"),
    "s2cur_auxil": ("ocelot.cpbd.beam.analysis", "s2cur_auxil"),

    # Beam utilities.
    "simple_filter": ("ocelot.cpbd.beam.beam_utils", "simple_filter"),
    "interp1": ("ocelot.cpbd.beam.beam_utils", "interp1"),
    "sortcols": ("ocelot.cpbd.beam.beam_utils", "sortcols"),
    "convmode_py": ("ocelot.cpbd.beam.beam_utils", "convmode_py"),
    "convmode": ("ocelot.cpbd.beam.beam_utils", "convmode"),
    "moments": ("ocelot.cpbd.beam.beam_utils", "moments"),
    "m_from_twiss": ("ocelot.cpbd.beam.beam_utils", "m_from_twiss"),
    "beam_matching": ("ocelot.cpbd.beam.beam_utils", "beam_matching"),
}


def __getattr__(name):
    try:
        module_name, attr_name = _LAZY_EXPORTS[name]
    except KeyError as exc:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc

    module = import_module(module_name)
    value = module if attr_name is None else getattr(module, attr_name)
    globals()[name] = value
    return value


def __dir__():
    return sorted(set(globals()) | set(__all__) | set(_LAZY_EXPORTS))
