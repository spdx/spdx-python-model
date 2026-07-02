# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Version-agnostic structural types (PEP 544 Protocols) for the SPDX 3 bindings.

Every generated SPDX 3 minor version has its own set of nominal types; this
package exposes one Protocol per class so code can be written against any 3.x
version and still type-check under ``mypy --strict``.

**Usage:**

.. code-block:: python

    from typing import Optional
    from spdx_python_model import protocols

    def relabel(e: protocols.Element, ci: protocols.CreationInfo) -> Optional[str]:
        e.name = "renamed"      # scalar write (typed)
        e.creationInfo = ci     # object-ref write
        return e.name           # scalar read (typed)

**Class hierarchy** is preserved: ``protocols.Person`` satisfies
``protocols.Agent``; a function accepting ``protocols.Agent`` accepts
``Person``, ``Tool``, ``SoftwareAgent``, etc. from any version.

**New classes** introduced in a later minor version (e.g.
``protocols.ai_EnergyConsumption`` from SPDX 3.1) are included and accept
objects from the versions that define them.

**Object-reference property reads** return ``Any`` (e.g. ``e.creationInfo``);
scalar reads are precisely typed. See the README for patterns to recover the
type (annotate at assignment, ``cast()``, or use a concrete version).

These types are for **static typing only**; no ``@runtime_checkable``.
"""

from ._merged import *  # noqa: F401, F403
from ._merged import SHACLObjectProtocol, SHACLObjectSetProtocol
from ._merged import __all__ as _merged_all
from .core import SpdxModelModule

SpdxObject = SHACLObjectProtocol
SpdxObjectSet = SHACLObjectSetProtocol

__all__ = [
    *_merged_all,
    "SpdxModelModule",
    "SpdxObject",
    "SpdxObjectSet",
]
