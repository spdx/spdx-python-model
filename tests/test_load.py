# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0

import importlib
import re
from pathlib import Path

import pytest

DATA_DIR = Path(__file__).parent / "data"


@pytest.mark.parametrize(
    "datapath,version",
    [
        pytest.param(
            DATA_DIR / "3.0.1" / "example.spdx3.json",
            "3.0.1",
            id="3.0.1",
        ),
    ],
)
def test_load(datapath, version):
    import spdx_python_model

    modname = "v" + re.sub(r"[^a-zA-Z0-9_]", "_", version)

    model, objset = spdx_python_model.load(datapath)

    assert isinstance(objset, model.SHACLObjectSet)
    assert model is getattr(spdx_python_model, modname)
