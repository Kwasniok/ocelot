# Developer Installation Guide

## 1. Install Python 3.10+
Install Python 3.10 or higher from [python.org](https://www.python.org/downloads/). Make sure to add Python to your system PATH.

## 2. Create a virtual environment
Create a local virtual environment exclusive for your development of your ocelot fork. This is recommended to avoid conflicts with other Python packages installed on your computer. You can use the following command to create a virtual environment named `.venv`:
```bash
python3 -m venv .venv
```

## 3. Install dependencies
Activate the virtual environment and install the required dependencies:
```bash
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
pip install --upgrade pip
pip install -e ".[dev]"
```

## Notes
- From now on activate your virtual environment whenever you work on your fork (as seen in [Step 3](#3-install-dependencies)). You can deactivate it by running `deactivate` in the terminal.
- If you want to install additional dependencies, you can do so by running `pip install <package_name>` while the virtual environment is activated. But make sure to add them to the `pyproject.toml` file if they become a required dependency for your fork.