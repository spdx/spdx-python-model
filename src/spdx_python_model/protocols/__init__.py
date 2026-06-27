# SPDX-FileType: SOURCE
# SPDX-License-Identifier: Apache-2.0
"""
Version-agnostic structural types (PEP 544 Protocols) for the SPDX 3 bindings.

- Core protocols (:mod:`.core`, hand-written): ``SpdxObject``, ``SpdxObjectSet``,
  ``SpdxModelModule`` — the version-neutral machinery surface.
- Domain protocols (:mod:`._domain`, generated at build time from the baseline
  version's stub): one per SPDX class, e.g. ``protocols.Element``,
  ``protocols.CreationInfo``.

See the package README for guidance on when to annotate with a protocol versus a
concrete version type.
"""

from . import _domain
from ._domain import *  # noqa: F401, F403
from .core import SpdxModelModule, SpdxObject, SpdxObjectSet

__all__ = [
    "SpdxModelModule",
    "SpdxObject",
    "SpdxObjectSet",
    *_domain.__all__,
]
