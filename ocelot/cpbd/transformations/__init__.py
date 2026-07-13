from importlib import import_module

__all__ = ['CavityTM', 'TransferMap', 'ExactDriftTM', 'KickTM', 'MultipoleTM',
           'PulseTM', 'RungeKuttaGlobalTM', 'RungeKuttaOcelotTM', 'RungeKuttaTM',
           'RungeKuttaTrTM', 'SecondTM', 'TWCavityTM', 'UndulatorTestTM',
           'TMTypes']

_LAZY_EXPORTS = {
    'CavityTM': ('ocelot.cpbd.transformations.cavity', 'CavityTM'),
    'TransferMap': ('ocelot.cpbd.transformations.transfer_map', 'TransferMap'),
    'ExactDriftTM': ('ocelot.cpbd.transformations.exact_drift', 'ExactDriftTM'),
    'KickTM': ('ocelot.cpbd.transformations.kick', 'KickTM'),
    'MultipoleTM': ('ocelot.cpbd.transformations.multipole', 'MultipoleTM'),
    'PulseTM': ('ocelot.cpbd.transformations.pulse', 'PulseTM'),
    'RungeKuttaGlobalTM': ('ocelot.cpbd.transformations.runge_kutta', 'RungeKuttaGlobalTM'),
    'RungeKuttaOcelotTM': ('ocelot.cpbd.transformations.runge_kutta', 'RungeKuttaOcelotTM'),
    'RungeKuttaTM': ('ocelot.cpbd.transformations.runge_kutta', 'RungeKuttaTM'),
    'RungeKuttaTrTM': ('ocelot.cpbd.transformations.runge_kutta_tr', 'RungeKuttaTrTM'),
    'SecondTM': ('ocelot.cpbd.transformations.second_order', 'SecondTM'),
    'TWCavityTM': ('ocelot.cpbd.transformations.tw_cavity', 'TWCavityTM'),
    'UndulatorTestTM': ('ocelot.cpbd.transformations.undulator_test', 'UndulatorTestTM'),
    'TMTypes': ('ocelot.cpbd.transformations.transformation', 'TMTypes'),
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
