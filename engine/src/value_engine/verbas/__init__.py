"""Verbas. Na v1, apenas indenização substitutiva do PASEP (PROMPT_VALUE.md §4).

A arquitetura fica preparada para outras verbas (interface `Verba`), mas ATS,
insalubridade e URV NÃO são implementados na v1 (§14).
"""

from __future__ import annotations

from .base import Verba
from .pasep import VerbaPasep

__all__ = ["Verba", "VerbaPasep"]
