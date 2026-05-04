from dataclasses import dataclass
from abc import ABC
from domain.value_objects.population import ITotalPopulation
from domain.value_objects.income import IMedianIncome
from domain.value_objects.radar import IRadar
from domain.value_objects.operation import IOperation

@dataclass(frozen=True)
class IPrediction(ABC):
    operation: IOperation
    total_population: ITotalPopulation
    median_income: IMedianIncome
    competitor_count: int
    ai_insight: str
    radar: IRadar
    is_success: bool

@dataclass(frozen=True)
class Prediction(IPrediction):
    operation: IOperation
    total_population: ITotalPopulation
    median_income: IMedianIncome
    competitor_count: int
    ai_insight: str
    radar: IRadar
    is_success: bool