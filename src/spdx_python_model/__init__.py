# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Python bindings for the SPDX 3 data model.
"""

import importlib
import json
import warnings
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING, Any, List, Tuple, cast

from .bindings import _CONTEXT_TABLE, _DRAFT_VERSIONS
from .version import VERSION
from .version import VERSION as __version__

if TYPE_CHECKING:
    from .bindings import *  # noqa: F403
    from .protocols import SpdxModelModule, SpdxObject, SpdxObjectSet

__all__ = [
    "bindings",  # generated # noqa: F405
    "LoadError",
    "SPDXDraftWarning",
    "SpdxModelModule",
    "SpdxObject",
    "SpdxObjectSet",
    "VERSION",
    "__version__",
    "load",
    "load_data",
    "protocols",  # lazy submodule via __getattr__ # noqa: F405
]

_VERSION_MODULES = frozenset(_CONTEXT_TABLE.values())


class LoadError(Exception):
    """Raised when a SPDX document cannot be loaded."""


class SPDXDraftWarning(FutureWarning):
    """Warns that a loaded SPDX version is still in development (draft).

    To suppress::

        import warnings
        from spdx_python_model import SPDXDraftWarning
        warnings.filterwarnings("ignore", category=SPDXDraftWarning)
    """


def _warn_if_draft(module_name: str) -> None:
    if module_name in _DRAFT_VERSIONS:
        warnings.warn(
            f"SPDX bindings '{module_name}' track an in-development draft and "
            "may change without notice.",
            SPDXDraftWarning,
            stacklevel=3,
        )


def __getattr__(name: str) -> Any:
    """Lazily import a version's bindings or the protocols package (PEP 562)."""
    if name in _VERSION_MODULES:
        _warn_if_draft(name)
        return importlib.import_module(f"{__name__}.bindings.{name}")
    if name == "protocols":
        return importlib.import_module(f"{__name__}.protocols")
    if name in ("SpdxObject", "SpdxObjectSet", "SpdxModelModule"):
        protocols = importlib.import_module(f"{__name__}.protocols")
        return getattr(protocols, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> List[str]:
    return sorted(set(globals()) | _VERSION_MODULES)


def load_data(data: Any) -> Tuple[ModuleType, "SpdxObjectSet"]:
    """
    Automatically load a SPDX 3 JSON document with the correct model based on
    its context

    :param data: The decoded JSON data as a Python dict

    :returns: A tuple of ``(model, objset)`` where ``objset`` is typed as
        :class:`~spdx_python_model.protocols.SpdxObjectSet` and ``model`` is
        the concrete version submodule (``ModuleType``).

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

    _warn_if_draft(module_name)
    model = importlib.import_module(f"{__name__}.bindings.{module_name}")

    d = model.JSONLDDeserializer()
    objset = model.SHACLObjectSet()

    d.deserialize_data(data, objset)

    return model, cast("SpdxObjectSet", objset)


def load(path: Path) -> Tuple[ModuleType, "SpdxObjectSet"]:
    """
    Automatically load a SPDX 3 JSON document with the correct model based on
    its context

    :param path: The path to the SPDX 3 JSON file

    :returns: A tuple of ``(model, objset)`` where ``objset`` is typed as
        :class:`~spdx_python_model.protocols.SpdxObjectSet` and ``model`` is
        the concrete version submodule (``ModuleType``).

    :raises LoadError: If the data is missing a context or if the context is
        not recognized
    :raises TypeError: If the data is not a dictionary
    """
    with path.open("r") as f:
        data = json.load(f)

    return load_data(data)
