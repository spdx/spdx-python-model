# spdx-python-model

[![PyPI - Version](https://img.shields.io/pypi/v/spdx-python-model)](https://pypi.org/project/spdx-python-model/)
![Apache-2.0 license](https://img.shields.io/github/license/spdx/spdx-python-model)

`spdx-python-model` is a Python library for working with the SPDX 3 data model.

Read the [API documentation](https://spdx.github.io/spdx-python-model/).

All bindings in this repository are auto-generated from the RDF and SHACL
definitions of the [SPDX specification version 3][spdx-spec] using
[shacl2code](https://github.com/JPEWdev/shacl2code) during the package build
process.

**NOTE:** The bindings are pretty low level, intended for more directly
manipulating SPDX files. While they are fully functions, they lack higher level
helper functions that may be useful for creating SPDX documents. If you want a
higher level approach, please see the
[SPDX Python Tools](https://github.com/spdx/tools-python) (however, it
doesn't yet support SPDX 3).

[spdx-spec]: https://spdx.org/specifications

## Installation

### Install from PyPI

```shell
python3 -m pip install spdx-python-model
```

### Install from Git

If you would like to pull the bindings directly from Git instead of using a
released version from PyPI, the following command can be used:

```shell
python3 -m pip install git+https://github.com/spdx/spdx-python-model.git@main
```

Note that this will pull the latest version from the `main` branch. If you want
a specific commit, replace `main` with the git commit SHA.

### Install/build using local SPDX model files

Using local SPDX model files is ideal for testing pre-release versions
or when official URLs are not yet live.

It is also required for build systems that prohibit network access during
packaging, such as Debian or Yocto.

To build using local model files:

1) Clone the repository:

    ```shell
    git clone https://github.com/spdx/spdx-python-model.git
    cd spdx-python-model
    ```

2) Download model files:

    Run the following commands to download the necessary files
    for a specific SPDX version and keep it in a local directory:

    ```shell
    mkdir -p ~/spdx_models/v3.0.1
    cd ~/spdx_models/v3.0.1
    wget https://spdx.org/rdf/3.0.1/spdx-context.jsonld
    wget https://spdx.org/rdf/3.0.1/spdx-json-serialize-annotations.ttl
    wget https://spdx.org/rdf/3.0.1/spdx-model.ttl
    ```

    Or use your own model files.

    The local directory must be organized by SPDX version,
    with specific file names.

    ```text
    <SHACL2CODE_SPDX_DIR>/
    └── v[VERSION]/
        ├── spdx-context.jsonld
        ├── spdx-json-serialize-annotations.ttl
        └── spdx-model.ttl
    ```

3) Set the model directory:

    Point `SHACL2CODE_SPDX_DIR` environment variable to that local directory.

    ```shell
    export SHACL2CODE_SPDX_DIR=~/spdx_models
    ```

4) Install/build:

    ```shell
    python3 -m pip install .
    ```

    or

    ```shell
    python3 -m build
    ```

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

You can also have the bindings automatically detect the correct version to use
using the `load()` API:

```python
import spdx_python_model

path = Path("/path/to/file.spdx3.json")

model, objset = spdx_python_model.load(path)

p = model.Person()
```

Check out this short [Python notebook tutorial][tutorial]
to get started with spdx-python-model.

[tutorial]: https://spdx.github.io/spdx-python-model/tutorial/using-spdx3.html

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
to PyPI.
