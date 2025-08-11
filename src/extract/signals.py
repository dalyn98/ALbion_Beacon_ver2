"""Signal extraction (stub)."""
from dataclasses import dataclass
from typing import List, Any

@dataclass
class ZoneEnter:
    zone_id: str

@dataclass
class PartySizeUpdate:
    party_n: int

def emit(rec: Any) -> List[object]:
    return []  # stub
