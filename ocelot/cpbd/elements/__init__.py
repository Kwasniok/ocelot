from importlib import import_module

__all__ = ['UnknownElement', 'Aperture', 'Bend', 'Cavity', 'Drift', 'Element',
           'Hcor', 'Marker', 'Matrix', 'Monitor', 'Multipole', 'Octupole', 'Pulse',
           'Quadrupole', 'RBend', 'SBend', 'Sextupole', 'Solenoid', 'TDCavity',
           'TWCavity', 'Undulator', 'Vcor', 'XYQuadrupole']

_LAZY_EXPORTS = {
    'UnknownElement': ('ocelot.cpbd.elements.unknown_element', 'UnknownElement'),
    'Aperture': ('ocelot.cpbd.elements.aperture', 'Aperture'),
    'Bend': ('ocelot.cpbd.elements.bend', 'Bend'),
    'Cavity': ('ocelot.cpbd.elements.cavity', 'Cavity'),
    'Drift': ('ocelot.cpbd.elements.drift', 'Drift'),
    'Element': ('ocelot.cpbd.elements.element', 'Element'),
    'Hcor': ('ocelot.cpbd.elements.hcor', 'Hcor'),
    'Marker': ('ocelot.cpbd.elements.marker', 'Marker'),
    'Matrix': ('ocelot.cpbd.elements.matrix', 'Matrix'),
    'Monitor': ('ocelot.cpbd.elements.monitor', 'Monitor'),
    'Multipole': ('ocelot.cpbd.elements.multipole', 'Multipole'),
    'Octupole': ('ocelot.cpbd.elements.octupole', 'Octupole'),
    'Pulse': ('ocelot.cpbd.elements.pulse', 'Pulse'),
    'Quadrupole': ('ocelot.cpbd.elements.quadrupole', 'Quadrupole'),
    'RBend': ('ocelot.cpbd.elements.rbend', 'RBend'),
    'SBend': ('ocelot.cpbd.elements.sbend', 'SBend'),
    'Sextupole': ('ocelot.cpbd.elements.sextupole', 'Sextupole'),
    'Solenoid': ('ocelot.cpbd.elements.solenoid', 'Solenoid'),
    'TDCavity': ('ocelot.cpbd.elements.tdcavity', 'TDCavity'),
    'TWCavity': ('ocelot.cpbd.elements.twcavity', 'TWCavity'),
    'Undulator': ('ocelot.cpbd.elements.undulator', 'Undulator'),
    'Vcor': ('ocelot.cpbd.elements.vcor', 'Vcor'),
    'XYQuadrupole': ('ocelot.cpbd.elements.xyquadruple', 'XYQuadrupole'),
}


def __getattr__(name):
    try:
        module_name, attr_name = _LAZY_EXPORTS[name]
    except KeyError as exc:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc

    value = getattr(import_module(module_name), attr_name)
    globals()[name] = value
    return value


def __dir__():
    return sorted(set(globals()) | set(__all__))
