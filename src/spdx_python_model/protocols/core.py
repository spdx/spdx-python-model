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

    # Names mirror the generated factory/class names exactly (PascalCase),
    # not method-naming convention, so the Protocol structurally matches them.
    # pylint: disable=invalid-name,missing-function-docstring
    def SHACLObjectSet(self) -> SHACLObjectSetProtocol: ...
    def JSONLDDeserializer(self) -> Any: ...
    def JSONLDSerializer(self) -> Any: ...
    # pylint: enable=invalid-name,missing-function-docstring
    def __getattr__(self, name: str) -> Any: ...
