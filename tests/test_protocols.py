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

# Each version's instances of these classes must satisfy SpdxObject.
_CLASSES = [
    "Person",
    "Element",
    "ElementCollection",
    "SpdxDocument",
    "CreationInfo",
    "Relationship",
    "RelationshipType",
    "IndividualElement",
    "software_Package",
    "software_Sbom",
    "simplelicensing_AnyLicenseInfo",
    "expandedlicensing_IndividualLicensingInfo",
    "expandedlicensing_License",
]

# Named-individual IRI constants (str) that must exist, as (owning class, name).
_NAMED_INDIVIDUALS = [
    ("IndividualElement", "NoneElement"),
    ("IndividualElement", "NoAssertionElement"),
    ("expandedlicensing_IndividualLicensingInfo", "NoAssertionLicense"),
    ("expandedlicensing_IndividualLicensingInfo", "NoneLicense"),
]


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

    checks = ""
    for v in versions:
        checks += (
            # Assignment to protocol type forces the static conformance check.
            f"module_{v}: SpdxModelModule = {v}\n"
            f"objset_{v}: SpdxObjectSet = {v}.SHACLObjectSet()\n"
            f"count(objset_{v})\n"
            f"count(module_{v}.SHACLObjectSet())\n"
            f"module_{v}.SHACLObjectSet().add(module_{v}.Person())\n"
        )
        for i, cls in enumerate(_CLASSES):
            checks += f"c{i}_{v}: SpdxObject = {v}.{cls}()\n"
        for i, (cls, name) in enumerate(_NAMED_INDIVIDUALS):
            checks += f"n{i}_{v}: str = {v}.{cls}.{name}\n"
        checks += "\n"

    # All versions' object sets coexist in one List[SpdxObjectSet].
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
