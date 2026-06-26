# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Version-agnostic structural types (PEP 544 Protocols) for the SPDX 3 bindings.

Each SPDX 3 minor version (``v3_0_1``, ``v3_1``, …) is generated as a distinct
set of nominal types. Because SPDX 3 keeps minor versions backward compatible,
they are structurally compatible: these protocols capture the shared surface so
one function or class can work with any 3.x version under ``mypy --strict``.

Static typing only (no ``@runtime_checkable``); no runtime imports from the
bindings.
"""

from __future__ import annotations

from typing import Any, Iterable, Iterator, Optional, Protocol, Set, Tuple

__all__ = [
    "SpdxObject",
    "SpdxObjectSet",
    "SpdxModelModule",
]


class SpdxObject(Protocol):
    """Version-agnostic view of a single SPDX object (the ``SHACLObject`` base)."""

    def get_id(self) -> Optional[str]: ...
    def set_id(self, value: Optional[str]) -> None: ...
    def get_type(self) -> str: ...
    def get_compact_type(self) -> Optional[str]: ...
    def property_keys(self) -> Iterator[Tuple[Optional[str], str, Optional[str]]]: ...


class SpdxObjectSet(Protocol):
    """Version-agnostic view of a ``SHACLObjectSet`` (read / query / link surface).

    Omits the raw index attributes (``objects``, ``obj_by_id``, ``missing_ids``,
    ``context``) and the version-coupled methods (``encode``/``decode``,
    ``merge``); use a concrete version type for those.
    """

    def find_by_id(self, _id: str, default: Any = None) -> Optional[SpdxObject]: ...
    def foreach(self) -> Iterable[SpdxObject]: ...
    def foreach_type(
        self, typ: str, *, match_subclass: bool = True
    ) -> Iterable[SpdxObject]: ...
    def link(self) -> Set[str]: ...

    # Object parameters are ``Any``: no version-neutral type is a supertype of
    # every version's ``SHACLObject``.
    def add(self, obj: Any) -> Any: ...
    def remove(self, obj: Any) -> None: ...
    def update(self, *others: Iterable[Any]) -> None: ...
    def __contains__(self, item: Any) -> bool: ...


class SpdxModelModule(Protocol):
    """Version-agnostic view of a bindings module (e.g. the model returned by
    :func:`spdx_python_model.load`).

    Factories are declared as methods (covariant return) so every version's
    module satisfies the protocol; ``__getattr__`` exposes version-specific
    classes such as ``Person`` as ``Any``.
    """

    def SHACLObjectSet(self) -> SpdxObjectSet: ...
    def JSONLDDeserializer(self) -> Any: ...
    def JSONLDSerializer(self) -> Any: ...
    def __getattr__(self, name: str) -> Any: ...
