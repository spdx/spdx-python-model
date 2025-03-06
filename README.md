# spdx-python-model

Generated Python code for SPDX Spec version 3

All bindings in this repository are generated using
[shacl2code](https://github.com/JPEWdev/shacl2code) at the time the package is
built.

**NOTE:** The bindings are pretty low level, intended for more directly
manipulating SPDX files. While they are fully functions, they lack higher level
helper functions that may be useful for creating SPDX documents. If you want a
higher level approach, please see the
[SPDX Python Tools](https://github.com/spdx/tools-python) (however this repo
doesn't yet support SPDX 3)

## Installation (PyPi)

```shell
python3 -m pip install spdx-python-model
```

## Installation (Git)

If you would like to pull the bindings directly from Git instead of using a
released version from PyPi, the following command can be used:

```shell
python3 -m pip install git+https://github.com/spdx/spdx-python-model.git@main
```

Note that this will pull the latest version from the `main` branch. If you want
a specific commit, replace `main` with the git commit SHA

## Usage

Each version of the SPDX spec has a module named `v{MAJOR}_{MINOR}_{MICRO}`
that contains the bindings for that version under the `spdx_python_model` top
level. For example:

```python
import spdx_python_model

p = spdx_python_model.v3_0_1.Person()
```

Alternatively, if a shorter name is desired, a specific version can be imported
with another name:

```python
from spdx_python_model import v3_0_1 as spdx_3_0

p = spdx_3_0.Person()
```

## Testing

This repository has support for running tests against the bindings using `pytest`.
To run the tests, first setup a virtual environment and install the development
variant of the package in editable mode:

```shell
python3 -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
```

Then the tests can be run with:

```shell
pytest -vx
```

## Making a new release

To make a new release of this repository, bump the version number found in
`src/spdx_python_model/version.py`, and merge it into the repo. After this,
make a new release in GitHub with the name `v` + *VERSION*, where *VERSION*
matches the version number specified in `version.py` (e.g. `v1.0.0`).

After this, GitHub actions will do the rest to build the package and publish it
to PyPi
