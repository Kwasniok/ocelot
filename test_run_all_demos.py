from __future__ import annotations

import argparse
import importlib.util
import os
import shlex
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parent
DEMOS = ROOT / "demos"
MAX_OUTPUT_CHARS = 12_000
NOTEBOOK_DEPENDENCIES = ("nbconvert", "ipykernel")


@dataclass
class Failure:
    kind: str
    path: Path
    command: Sequence[str]
    returncode: int | None
    stdout: str
    stderr: str
    reason: str


def make_env() -> dict[str, str]:
    env = os.environ.copy()
    env["MPLBACKEND"] = "Agg"

    pythonpath = [str(ROOT)]
    if env.get("PYTHONPATH"):
        pythonpath.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(pythonpath)
    return env


def relpath(path: Path) -> str:
    return str(path.relative_to(ROOT))


def output_tail(output: str, limit: int = MAX_OUTPUT_CHARS) -> str:
    if len(output) <= limit:
        return output
    return f"... output truncated to last {limit} characters ...\n{output[-limit:]}"


def matching_files(paths: Iterable[Path], match: str | None) -> list[Path]:
    selected = sorted(paths)
    if match is None:
        return selected
    return [path for path in selected if match in relpath(path)]


def missing_notebook_dependencies() -> list[str]:
    return [
        module
        for module in NOTEBOOK_DEPENDENCIES
        if importlib.util.find_spec(module) is None
    ]


def record_notebook_setup_failure(
    counters: dict[str, int],
    failures: list[Failure],
    *,
    notebook_count: int,
    missing: Sequence[str],
) -> None:
    counters["notebook_fail"] += notebook_count
    failures.append(
        Failure(
            kind="notebook setup",
            path=DEMOS,
            command=[sys.executable, "-m", "nbconvert", "--help"],
            returncode=None,
            stdout="",
            stderr=(
                "Missing notebook execution dependencies in this Python environment: "
                f"{', '.join(missing)}.\n"
                "Install them with `python -m pip install nbconvert ipykernel` "
                "or the equivalent conda command."
            ),
            reason="notebook dependencies are not installed",
        )
    )
    print(
        "FAILED: notebook execution dependencies are missing: "
        f"{', '.join(missing)}",
        flush=True,
    )


def run_cmd(
    command: Sequence[str],
    path: Path,
    kind: str,
    counters: dict[str, int],
    failures: list[Failure],
    *,
    cwd: Path,
    timeout: float | None,
) -> None:
    print(f"Running `{relpath(path)}` ...", flush=True)

    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            env=make_env(),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        counters[f"{kind}_fail"] += 1
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        failures.append(
            Failure(
                kind=kind,
                path=path,
                command=command,
                returncode=None,
                stdout=stdout if isinstance(stdout, str) else stdout.decode(errors="replace"),
                stderr=stderr if isinstance(stderr, str) else stderr.decode(errors="replace"),
                reason=f"timed out after {timeout} seconds",
            )
        )
        print(f"FAILED: `{relpath(path)}` timed out after {timeout} seconds", flush=True)
        return

    if result.returncode == 0:
        counters[f"{kind}_success"] += 1
        return

    counters[f"{kind}_fail"] += 1
    failures.append(
        Failure(
            kind=kind,
            path=path,
            command=command,
            returncode=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
            reason=f"exited with return code {result.returncode}",
        )
    )
    print(f"FAILED: `{relpath(path)}` exited with return code {result.returncode}", flush=True)


def run_all_notebooks(
    counters: dict[str, int],
    failures: list[Failure],
    *,
    notebooks: Sequence[Path],
    output_dir: Path,
    timeout: float | None,
) -> None:
    for notebook in notebooks:
        notebook_output_dir = output_dir / notebook.parent.relative_to(DEMOS)
        notebook_output_dir.mkdir(parents=True, exist_ok=True)
        run_cmd(
            [
                sys.executable,
                "-m",
                "nbconvert",
                "--to",
                "notebook",
                "--execute",
                "--output-dir",
                str(notebook_output_dir),
                "--output",
                notebook.name,
                notebook.name,
            ],
            path=notebook,
            kind="notebook",
            counters=counters,
            failures=failures,
            cwd=notebook.parent,
            timeout=timeout,
        )


def run_all_scripts(
    counters: dict[str, int],
    failures: list[Failure],
    *,
    match: str | None,
    timeout: float | None,
) -> None:
    scripts = (path for path in DEMOS.rglob("*.py") if path.name != "__init__.py")
    for script in matching_files(scripts, match):
        run_cmd(
            [sys.executable, script.name],
            path=script,
            kind="script",
            counters=counters,
            failures=failures,
            cwd=script.parent,
            timeout=timeout,
        )


def format_failure(failure: Failure) -> str:
    parts = [
        f"{failure.kind}: {relpath(failure.path)}",
        f"reason: {failure.reason}",
        f"command: {shlex.join(failure.command)}",
    ]
    if failure.stdout:
        parts.append(f"stdout:\n{output_tail(failure.stdout).rstrip()}")
    if failure.stderr:
        parts.append(f"stderr:\n{output_tail(failure.stderr).rstrip()}")
    return "\n".join(parts)


def print_summary(counters: dict[str, int], failures: list[Failure]) -> None:
    print("\n\nexecution summary:")
    for failure in failures:
        print(f"\n\n{format_failure(failure)}")

    print("\n\nsummary:")
    print(f"notebooks executed successfully: {counters['notebook_success']}")
    print(f"notebooks failed: {counters['notebook_fail']}")
    print(f"scripts executed successfully: {counters['script_success']}")
    print(f"scripts failed: {counters['script_fail']}")


def run_all(kind: str = "all", match: str | None = None, timeout: float | None = None) -> tuple[dict[str, int], list[Failure]]:
    counters = {
        "notebook_success": 0,
        "notebook_fail": 0,
        "script_success": 0,
        "script_fail": 0,
    }
    failures: list[Failure] = []

    selected_notebooks = matching_files(DEMOS.rglob("*.ipynb"), match)
    missing = missing_notebook_dependencies() if kind in {"all", "notebooks"} else []

    with tempfile.TemporaryDirectory(prefix="ocelot-demo-notebooks-") as tmpdir:
        output_dir = Path(tmpdir)
        if kind in {"all", "notebooks"}:
            if selected_notebooks and missing:
                record_notebook_setup_failure(
                    counters,
                    failures,
                    notebook_count=len(selected_notebooks),
                    missing=missing,
                )
            else:
                run_all_notebooks(
                    counters,
                    failures,
                    notebooks=selected_notebooks,
                    output_dir=output_dir,
                    timeout=timeout,
                )
        if kind in {"all", "scripts"}:
            run_all_scripts(counters, failures, match=match, timeout=timeout)

    return counters, failures


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute Ocelot demo notebooks and scripts.")
    parser.add_argument(
        "--kind",
        choices=("all", "notebooks", "scripts"),
        default="all",
        help="select which demo files to execute",
    )
    parser.add_argument(
        "--match",
        help="only run demo paths containing this substring, for example `demos/ebeam/dba.py`",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        help="optional per-demo timeout in seconds",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    counters, failures = run_all(kind=args.kind, match=args.match, timeout=args.timeout)
    print_summary(counters, failures)
    return int(bool(failures))


def test_run_all_demos() -> None:
    counters, failures = run_all()
    print_summary(counters, failures)
    assert not failures, "\n\n".join(format_failure(failure) for failure in failures)


if __name__ == "__main__":
    raise SystemExit(main())
