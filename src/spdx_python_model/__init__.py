# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
#
"""SPDX 3 model."""

import importlib
import json
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING, Any, List, Tuple

from .bindings import _CONTEXT_TABLE
from .version import VERSION

if TYPE_CHECKING:
    # Generated re-exports to give type checkers version types.
    # No imported during runtime.
    from .bindings._reexport import *  # noqa: F403

__all__ = ["VERSION", "LoadError", "load", "load_data"]

# Version submodule names accepted by __getattr__ for top-level import.
_VERSION_MODULES = frozenset(_CONTEXT_TABLE.values())


class LoadError(Exception):
    """Raised when a SPDX document cannot be loaded."""


def __getattr__(name: str) -> ModuleType:
    """Lazily import a version's bindings on first top-level access (PEP 562)."""
    if name in _VERSION_MODULES:
        return importlib.import_module(f"{__name__}.bindings.{name}")
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> List[str]:
    return sorted(set(globals()) | _VERSION_MODULES)


def load_data(data: Any) -> Tuple[ModuleType, Any]:
    """
    Automatically load a SPDX 3 JSON document with the correct model based on
    its context

    :param data: The decoded JSON data as a Python dict

    :returns: A tuple that contains the model and the decoded SHACLObjectSet

    :raises LoadError: If the data is missing a context or if the context is
        not recognized
    :raises TypeError: If the data is not a dictionary
    """

    if not isinstance(data, dict):
        raise TypeError("Data must be a dictionary")

    context = data.get("@context")
    if not context:
        raise LoadError("No @context in data")

    context_url = None

    if isinstance(context, str):
        context_url = context
    elif isinstance(context, list):
        for item in context:
            if isinstance(item, str):
                context_url = item
                break

    if not context_url:
        raise LoadError("No valid @context URL string found in data")

    module_name = _CONTEXT_TABLE.get(context_url)
    if module_name is None:
        raise LoadError(f"Unknown context URL '{context_url}'")

    model = importlib.import_module(f"{__name__}.bindings.{module_name}")

    d = model.JSONLDDeserializer()
    objset = model.SHACLObjectSet()

    d.deserialize_data(data, objset)

    return model, objset


def load(path: Path) -> Tuple[ModuleType, Any]:
    """
    Automatically load a SPDX 3 JSON document with the correct model based on
    its context

    :param path: The path to the SPDX 3 JSON file

    :returns: A tuple that contains the model and the decoded SHACLObjectSet

    :raises LoadError: If the data is missing a context or if the context is
        not recognized
    :raises TypeError: If the data is not a dictionary
    """
    with path.open("r") as f:
        data = json.load(f)

    return load_data(data)
