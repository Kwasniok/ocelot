from importlib import import_module

__all__ = [
    "CavityParams", "ExactDriftParams", "FirstOrderParams", "KickParams",
    "MultipoleParams", "RungeKuttaParams", "SecondOrderParams",
    "UndulatorTestParams",
]

_LAZY_EXPORTS = {
    "CavityParams": ("ocelot.cpbd.tm_params.cavity_params", "CavityParams"),
    "ExactDriftParams": ("ocelot.cpbd.tm_params.exact_drift_params", "ExactDriftParams"),
    "FirstOrderParams": ("ocelot.cpbd.tm_params.first_order_params", "FirstOrderParams"),
    "KickParams": ("ocelot.cpbd.tm_params.kick_params", "KickParams"),
    "MultipoleParams": ("ocelot.cpbd.tm_params.multipole_params", "MultipoleParams"),
    "RungeKuttaParams": ("ocelot.cpbd.tm_params.runge_kutta_params", "RungeKuttaParams"),
    "SecondOrderParams": ("ocelot.cpbd.tm_params.second_order_params", "SecondOrderParams"),
    "UndulatorTestParams": ("ocelot.cpbd.tm_params.undulator_test_params", "UndulatorTestParams"),
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
