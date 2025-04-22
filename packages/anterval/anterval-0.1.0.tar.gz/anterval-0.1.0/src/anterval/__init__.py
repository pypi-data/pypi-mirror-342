from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Final

from .core import Interval

__all__: Final[list[str]] = ["Interval"]
