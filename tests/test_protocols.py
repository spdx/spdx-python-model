# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
#
# The version-agnostic protocols must be satisfied by the concrete classes of
# every generated version, under strict mypy. This guards against generator
# drift silently breaking the shared interface, and verifies the runtime
# behavior matches the static surface.

from pathlib import Path

import pytest

PYPROJECT = Path(__file__).resolve().parents[1] / "pyproject.toml"
DATA_DIR = Path(__file__).parent / "data"

# A probe that forces mypy to check that both versions' concrete classes satisfy
# the protocols, and that a single version-agnostic function works with each.
PROBE = """\
from spdx_python_model import SpdxModelModule, SpdxObject, SpdxObjectSet
from spdx_python_model.bindings import v3_0_1, v3_1


def count(s: SpdxObjectSet) -> int:
    return sum(1 for _ in s.foreach())


def first_id(s: SpdxObjectSet) -> object:
    for o in s.foreach():
        return o.get_id()
    return None


# Concrete object sets satisfy SpdxObjectSet (assignment forces the check).
a: SpdxObjectSet = v3_0_1.SHACLObjectSet()
b: SpdxObjectSet = v3_1.SHACLObjectSet()

# Concrete objects satisfy SpdxObject.
p: SpdxObject = v3_0_1.Person()
q: SpdxObject = v3_1.Person()

# The version submodules satisfy SpdxModelModule.
m0: SpdxModelModule = v3_0_1
m1: SpdxModelModule = v3_1

# A single version-agnostic function accepts either version.
count(a)
count(b)

# SpdxModelModule.SHACLObjectSet() is typed as SpdxObjectSet; Person() is Any.
s = m0.SHACLObjectSet()
count(s)
person = m1.Person()
s.add(person)
"""


def test_strict_mypy_protocols_satisfied_by_all_versions(tmp_path):
    from mypy import api

    probe = tmp_path / "probe.py"
    probe.write_text(PROBE)

    stdout, stderr, status = api.run(
        ["--config-file", str(PYPROJECT), "--strict", str(probe)]
    )
    assert status == 0, stdout + stderr


def test_loaded_objset_is_usable_through_protocol():
    import spdx_python_model
    from spdx_python_model import SpdxObjectSet

    _model, objset = spdx_python_model.load(
        DATA_DIR / "3.0.1" / "example.spdx3.json"
    )

    # Exercise the protocol surface through a version-agnostic annotation.
    def names(s: SpdxObjectSet) -> list:
        return [o.get_id() for o in s.foreach_type("Person")]

    assert isinstance(list(objset.foreach()), list)
    assert names(objset) is not None
    # find_by_id returns either an object or the default.
    assert objset.find_by_id("does-not-exist", None) is None
