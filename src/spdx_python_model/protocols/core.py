# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""Protocol types describing spdx-python-model's packaging (not the SHACL model)."""

from __future__ import annotations

from typing import Any, Protocol

from ._merged import SHACLObjectSetProtocol

__all__ = ["SpdxModelModule"]


class SpdxModelModule(Protocol):
    """Version-agnostic view of a bindings module (e.g. the ``model`` returned
    by :func:`spdx_python_model.load`).

    Factories are declared as methods (covariant return) so every version's
    module satisfies the protocol; ``__getattr__`` exposes version-specific
    classes such as ``Person`` as ``Any``.
    """

    def SHACLObjectSet(self) -> SHACLObjectSetProtocol: ...
    def JSONLDDeserializer(self) -> Any: ...
    def JSONLDSerializer(self) -> Any: ...
    def __getattr__(self, name: str) -> Any: ...
