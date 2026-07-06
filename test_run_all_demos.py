from pathlib import Path
import subprocess
import sys
import os
import traceback
from typing import List, Tuple

root = Path(os.getcwd()).resolve()
demos = root / "demos"

counters = {
    "notebook_success": 0,
    "notebook_fail": 0,
    "script_success": 0,
    "script_fail": 0,
}
failures : List[Tuple[str, str]] = []


def run_cmd(cmd: List[str], file: str, cwd=None):
    try:
        subprocess.run(
            cmd,
            cwd=cwd,
            env=os.environ
            | {
                "MPLBACKEND": "Agg"
            },  # prevent matplotlib from trying to open a window and blocking the execution of the script until manual intervention
            # supress output to avoid cluttering the console:
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"FAILED: Error encountered while executing {file}:")
        traceback.print_exception(type(e), e, e.__traceback__)
        msg = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        failures.append((file, msg))


def run_all_notebooks():
    for notebook in demos.rglob("*.ipynb"):
        print(f"Running `{notebook}` ...")
        run_cmd(
            [
                sys.executable,
                "-m",
                "jupyter",
                "nbconvert",
                "--to",
                "notebook",
                "--execute",
                "--inplace",
                notebook.name,
            ],
            file=notebook.name,
            cwd=notebook.parent,
        )


def run_all_scripts():
    for script in demos.rglob("*.py"):

        print(f"Running `{script}` ...")
        run_cmd(
            [
                sys.executable,
                script.name,
            ],
            file=script.name,
            cwd=script.parent,
        )


if __name__ == "__main__":
    run_all_notebooks()
    run_all_scripts()

    print("\n\nexecution summary:")
    for file, error in failures:
        print(f"\n\nError encountered while executing {file}:\n{error}")

    print("\n\nsummary:")
    print(f"notebooks executed successfully: {counters['notebook_success']}")
    print(f"notebooks failed: {counters['notebook_fail']}")
    print(f"scripts executed successfully: {counters['script_success']}")
    print(f"scripts failed: {counters['script_fail']}")

    exit((counters["notebook_fail"] + counters["script_fail"]) > 0)
