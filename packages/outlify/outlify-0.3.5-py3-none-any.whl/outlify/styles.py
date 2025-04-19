from enum import Enum
from typing import NamedTuple


class Align(Enum):
    left = 'left'
    center = 'center'
    right = 'right'


class BorderStyle(NamedTuple):
    lt: str
    rt: str
    lb: str
    rb: str
    headers: str
    sides: str
