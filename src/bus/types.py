"""Event bus/types (stub)."""
from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

T = TypeVar("T")
E = TypeVar("E")

@dataclass
class Result(Generic[T, E]):
    ok: bool
    value: Optional[T] = None
    error: Optional[E] = None
