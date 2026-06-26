# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Version-agnostic structural types (PEP 544 Protocols) for the SPDX 3 bindings.

Each SPDX 3 minor version (``v3_0_1``, ``v3_1``, …) is generated as a distinct
set of nominal types, so a function annotated with ``v3_0_1.SHACLObjectSet``
cannot accept a ``v3_1.SHACLObjectSet``. SPDX 3 guarantees backward
compatibility across minor versions, which makes the versions structurally
compatible: the protocols here capture the version-neutral surface so callers
can write a single function or class that works with any 3.x version and still
type-checks under ``mypy --strict``.

These protocols are for **static typing only** (no ``@runtime_checkable``), and
this module deliberately imports nothing from the bindings at runtime.

Intentionally **not** modeled on ``SpdxObjectSet`` (use a concrete version type
if you need them): the raw index attributes (``objects``, ``obj_by_id``,
``missing_ids``, ``context``) are invariant containers that cannot be made
version-neutral, and the version-coupled methods (``encode``/``decode``,
``merge``) take or return version-specific helper types.
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
    """Version-agnostic view of a ``SHACLObjectSet`` (read / query / link surface)."""

    # Read and query: precise, version-neutral types.
    def find_by_id(self, _id: str, default: Any = None) -> Optional[SpdxObject]: ...
    def foreach(self) -> Iterable[SpdxObject]: ...
    def foreach_type(
        self, typ: str, *, match_subclass: bool = True
    ) -> Iterable[SpdxObject]: ...
    def link(self) -> Set[str]: ...

    # Mutators: object parameters must be ``Any``. The concrete ``add`` accepts
    # only its own version's ``SHACLObject``, and no version-neutral type is a
    # supertype of every version's class, so a narrower annotation would make the
    # concrete classes fail to satisfy this protocol.
    def add(self, obj: Any) -> Any: ...
    def remove(self, obj: Any) -> None: ...
    def update(self, *others: Iterable[Any]) -> None: ...
    def __contains__(self, item: Any) -> bool: ...


class SpdxModelModule(Protocol):
    """Version-agnostic view of a bindings module (e.g. the model returned by
    :func:`spdx_python_model.load`).

    The factories are declared as methods so that covariant return matching lets
    every version's module satisfy the protocol; a ``Callable``-typed attribute
    would be matched invariantly and fail. Version-specific classes such as
    ``Person`` are reached through ``__getattr__`` and resolve to ``Any``.
    """

    def SHACLObjectSet(self) -> SpdxObjectSet: ...
    def JSONLDDeserializer(self) -> Any: ...
    def JSONLDSerializer(self) -> Any: ...
    def __getattr__(self, name: str) -> Any: ...
