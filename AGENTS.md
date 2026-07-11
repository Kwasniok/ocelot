# Agent Guide for Ocelot

This file is the starting point for coding agents working in this repository.
It is intentionally compact: use it to find the right modules, examples, and
tests before making changes.

## Project Context

Ocelot is a Python toolkit for accelerator and photon simulations, especially
FELs, storage rings, and transport lines. Public user documentation lives at:

- Website: https://www.ocelot-collab.com
- Documentation: https://www.ocelot-collab.com/docs/docu/intro/
- Tutorials: https://www.ocelot-collab.com/docs/tutorial/intro/

The online documentation is useful for workflow orientation, but source code,
docstrings, demos, and tests are the most reliable implementation references.
If docs and code disagree, follow the code and existing tests.

## Repository Map

- `ocelot/`: importable package.
- `ocelot/cpbd/`: charged-particle beam dynamics: lattices, elements,
  tracking, optics, matching, collective effects, wakefields, and physics
  processes.
- `ocelot/cpbd/elements/`: public accelerator element wrappers and atom
  classes. This is the main entry point for `Drift`, `Quadrupole`, `Bend`,
  `Cavity`, `Undulator`, monitors, correctors, and apertures.
- `ocelot/cpbd/transformations/`: transfer-map and tracking-method classes.
- `ocelot/cpbd/tm_params/`: typed parameter containers passed from elements to
  transformations.
- `ocelot/cpbd/beam/`: `Twiss`, `Beam`, `Particle`, `ParticleArray`, beam
  generation, and beam analysis helpers.
- `ocelot/rad/`: synchrotron/FEL radiation calculations.
- `ocelot/optics/`: photon optics and wavefront utilities.
- `ocelot/adaptors/`: import/export adapters for external tools and file
  formats.
- `ocelot/gui/`: plotting and GUI helpers. Keep GUI imports out of core
  simulation paths.
- `demos/`: runnable examples. `demos/ipython_tutorials/` mirrors the public
  tutorial workflows; `demos/ebeam/` and `demos/sr/` are good source-level
  examples.
- `unit_tests/`: regression and architecture tests. New behavior should usually
  get a focused test here.

## Accelerator Workflow Pointers

For a simple lattice or optics task, start with:

- Elements: `ocelot.cpbd.elements`
- Lattice container: `ocelot.cpbd.magnetic_lattice.MagneticLattice`
- Linear optics: `ocelot.cpbd.optics.twiss`
- Tracking: `ocelot.cpbd.track.track`
- Beam objects: `ocelot.cpbd.beam.Twiss`, `ParticleArray`, `generate_parray`
- Navigation and physics process scheduling:
  `ocelot.cpbd.navi.Navigator` and `ocelot.cpbd.physics_proc`

Minimal example shape:

```python
from ocelot.cpbd.elements import Drift, Quadrupole, Bend, Marker
from ocelot.cpbd.magnetic_lattice import MagneticLattice
from ocelot.cpbd.optics import twiss

d = Drift(l=1.0)
qf = Quadrupole(l=0.3, k1=1.0)
qd = Quadrupole(l=0.3, k1=-1.0)
b = Bend(l=0.5, angle=0.1)
cell = (Marker(eid="start"), d, qf, d, qd, d, b, Marker(eid="stop"))
lat = MagneticLattice(cell)
tws = twiss(lat)
```

For workflow examples, prefer these before inventing new patterns:

- Linear optics and lattice design: `demos/ipython_tutorials/1_introduction.ipynb`,
  `demos/ipython_tutorials/7_lattice_design.ipynb`, `demos/ebeam/dba.py`
- Tracking and Runge-Kutta examples: `demos/ipython_tutorials/2_tracking.ipynb`,
  `demos/docs/18_runge_kutta_tracking.ipynb`, `demos/ebeam/rk_vs_matrix.py`
- Space charge, wake, CSR, and laser heater workflows:
  `demos/ipython_tutorials/3_space_charge.ipynb`,
  `demos/ipython_tutorials/4_wake.ipynb`,
  `demos/ipython_tutorials/5_CSR.ipynb`,
  `demos/ipython_tutorials/8_laser_heater.ipynb`
- Synchrotron radiation and photon field simulations:
  `demos/ipython_tutorials/pfs_1_synchrotron_radiation.ipynb`,
  `demos/sr/`, `demos/optics/`

## Architecture Notes

The CPBD element implementation uses a wrapper/atom/parameter/transformation
structure:

1. Public wrapper: user-facing element class, usually in
   `ocelot/cpbd/elements/*.py`.
2. Atom: physics state and `create_*_params(...)` hooks, often named
   `*_atom.py`.
3. TMParams: data objects in `ocelot/cpbd/tm_params/`.
4. Transformation: tracking algorithm in `ocelot/cpbd/transformations/`.

When adding or changing an element, check the architecture-contract tests in
`unit_tests/cpbd/architecture_contract/`. Preserve both the active tracking
method path and the first-order optics path unless the existing contract says
otherwise.

## Import Guidance

Many tutorials use `from ocelot import *`; keep that public facade working.
For new source code and tests, prefer explicit submodule imports so dependencies
stay local to the workflow being used.

Avoid adding heavyweight imports to:

- `ocelot/__init__.py`
- `ocelot/cpbd/__init__.py`
- package `__init__.py` files that are imported by core workflows

Importing plotting, GUI, HDF5, pandas-heavy analysis, or optional acceleration
libraries at package import time makes every simulation startup slower. Prefer
function-local imports when the dependency is only needed by a specific feature.

## Testing

Useful focused commands:

```bash
pytest unit_tests/cpbd -q
pytest unit_tests/cpbd/architecture_contract -q
pytest unit_tests/ebeam_test/dba/dba_test.py -q
pytest unit_tests/sr_test -q
```

For import-related changes, measure fresh interpreter startup, not repeated
imports in one process:

```bash
python -X importtime -c "import ocelot"
python -c "import subprocess, sys, time; t=time.perf_counter(); subprocess.run([sys.executable, '-c', 'import ocelot']); print(time.perf_counter() - t)"
```

## Change Discipline

- Keep public APIs and tutorial-facing names stable unless the task explicitly
  asks for a breaking change.
- Prefer small changes with targeted tests over broad refactors.
- Check existing demos/tests for the workflow before introducing a new helper.
- Do not mix formatting-only churn with behavior changes.
