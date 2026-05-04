from dataclasses import dataclass
from abc import ABC

@dataclass(frozen=True)
class ITotalPopulation(ABC):
    neighborhood: int
    district: int

@dataclass(frozen=True)
class TotalPopulation(ITotalPopulation):
    neighborhood: int
    district: int