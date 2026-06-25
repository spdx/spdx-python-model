# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
#
# Strict mypy must resolve the generated version bindings via both the
# top-level (spdx_python_model.vX) and package (spdx_python_model.bindings.vX)
# import paths. This guards the generated bindings/__init__.pyi stub.

from pathlib import Path

PYPROJECT = Path(__file__).resolve().parents[1] / "pyproject.toml"

PROBE = """\
from spdx_python_model import v3_0_1
from spdx_python_model.bindings import v3_0_1 as b

p: v3_0_1.Person = v3_0_1.Person()
q: b.Person = b.Person()
"""


def test_strict_mypy_resolves_version_types(tmp_path):
    from mypy import api

    probe = tmp_path / "probe.py"
    probe.write_text(PROBE)

    # --strict is passed explicitly so the check stays strict even if the
    # pyproject.toml config changes; the config still supplies python_version.
    stdout, stderr, status = api.run(
        ["--config-file", str(PYPROJECT), "--strict", str(probe)]
    )
    assert status == 0, stdout + stderr
