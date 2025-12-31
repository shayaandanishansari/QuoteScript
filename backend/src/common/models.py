
from dataclasses import dataclass
from typing import Dict, Optional, List


@dataclass
class FilterNode:
    kind: str          # 'quote' / 'author' / 'theme'
    value: str         # unquoted string content
    tag: Optional[str] # canonical tag: 'exact' / 'forgiving' / 'loose'


@dataclass
class SelectionNode:
    # TOP M and/or RANDOM N
    top: Optional[int] = None
    random: Optional[int] = None


@dataclass
class ProgramNode:
    filters: Dict[str, FilterNode]
    selection: SelectionNode


# IR shapes

@dataclass
class FilterIR:
    field: str   # 'quote', 'author', 'theme'
    value: str
    tag: str     # 'exact' / 'forgiving' / 'loose'


@dataclass
class SelectionIR:
    top: Optional[int]
    random: Optional[int]


@dataclass
class IR:
    filters: List[FilterIR]
    selection: SelectionIR
