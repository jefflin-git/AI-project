from dataclasses import dataclass
from abc import ABC

@dataclass(frozen=True)
class IRadar(ABC):
    labels: list[str]
    values: list[int]

@dataclass(frozen=True)
class Radar(IRadar):
    labels: list[str]
    values: list[int]