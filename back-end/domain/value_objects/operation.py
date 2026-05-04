from dataclasses import dataclass
from abc import ABC

@dataclass(frozen=True)
class IOperation(ABC):
    score: float
    report: str

@dataclass(frozen=True)
class Operation(IOperation):
    score: float
    report: str