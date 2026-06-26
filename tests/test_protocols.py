# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
#
# Every generated version's concrete classes must satisfy the protocols under
# strict mypy, and all versions must unify under the one structural type. The set
# of generated versions varies by build (draft versions such as v3_1 are not
# always present), so the probe is built from the versions actually present.

from __future__ import annotations

from pathlib import Path

PYPROJECT = Path(__file__).resolve().parents[1] / "pyproject.toml"
DATA_DIR = Path(__file__).parent / "data"


def _available_versions() -> list[str]:
    """Module names (e.g. "v3_0_1") of every generated version binding."""
    import spdx_python_model.bindings as bindings

    pkg_dir = Path(bindings.__file__).resolve().parent
    return sorted(
        p.name
        for p in pkg_dir.iterdir()
        if p.is_dir() and p.name.startswith("v") and (p / "model.py").exists()
    )


def _build_probe(versions: list[str]) -> str:
    header = (
        "from typing import List\n"
        "from spdx_python_model import SpdxModelModule, SpdxObject, SpdxObjectSet\n"
        + "".join(f"from spdx_python_model.bindings import {v}\n" for v in versions)
        + "\n\n"
        "def count(s: SpdxObjectSet) -> int:\n"
        "    return sum(1 for _ in s.foreach())\n\n\n"
    )

    # Per version: concrete classes and module satisfy the protocols, and the
    # agnostic `count` accepts the object set.
    checks = ""
    for v in versions:
        checks += (
            f"objset_{v}: SpdxObjectSet = {v}.SHACLObjectSet()\n"
            f"person_{v}: SpdxObject = {v}.Person()\n"
            f"module_{v}: SpdxModelModule = {v}\n"
            f"count(objset_{v})\n"
            # SHACLObjectSet() is typed SpdxObjectSet; Person() resolves to Any.
            f"count(module_{v}.SHACLObjectSet())\n"
            f"module_{v}.SHACLObjectSet().add(module_{v}.Person())\n\n"
        )

    # Cross-version: every version's object set coexists in one
    # List[SpdxObjectSet], consumed by one agnostic function.
    all_sets = ", ".join(f"objset_{v}" for v in versions)
    checks += (
        f"every: List[SpdxObjectSet] = [{all_sets}]\n"
        "for _s in every:\n"
        "    count(_s)\n"
    )
    return header + checks


def test_strict_mypy_protocols_satisfied_by_all_versions(tmp_path):
    from mypy import api

    versions = _available_versions()
    assert versions, "no generated version bindings found"

    probe = tmp_path / "probe.py"
    probe.write_text(_build_probe(versions))

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

    def names(s: SpdxObjectSet) -> list:
        return [o.get_id() for o in s.foreach_type("Person")]

    assert isinstance(list(objset.foreach()), list)
    assert names(objset) is not None
    assert objset.find_by_id("does-not-exist", None) is None
