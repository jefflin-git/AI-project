from dataclasses import dataclass
from abc import ABC

@dataclass(frozen=True)
class IMedianIncome(ABC):
    neighborhood: int
    district: int

@dataclass(frozen=True)
class MedianIncome(IMedianIncome):
    neighborhood: int
    district: int