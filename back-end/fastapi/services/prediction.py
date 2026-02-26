from repositories.prediction import IPredictionRepository
from value_objects.prediction import IPrediction, Prediction
from value_objects.population import TotalPopulation
from value_objects.income import MedianIncome
from value_objects.radar import Radar
from value_objects.operation import Operation

class PredictionService:
    def __init__(self, prediction_repository: IPredictionRepository):
        self.prediction_repository = prediction_repository
    
    def run_prediction(self, city: str, district: str, neighborhood: str, brand_type: int) -> IPrediction:
        try:
            score, id = self.prediction_repository.get_operation_score_from_model(city, district, neighborhood, brand_type)
            report = self.prediction_repository.get_operation_report(score, brand_type)
        
            return Prediction(
                operation=Operation(
                    score=score,
                    report=report
                ),
                total_population=TotalPopulation(
                    neighborhood=self.prediction_repository.get_neighborhood_total_population(city, district, neighborhood),
                    district=self.prediction_repository.get_district_total_population(city, district),
                ),
                median_income=MedianIncome(
                    neighborhood=self.prediction_repository.get_neighborhood_median_income(city, district, neighborhood),
                    district=self.prediction_repository.get_district_median_income(city, district),
                ),
                competitor_count=self.prediction_repository.get_competitor_count(city, district, neighborhood, brand_type),
                ai_insight=self.prediction_repository.get_ai_insight_from_table(id),
                radar=self.prediction_repository.get_radar(id=id, selected_idx=[1,2,3,4,6,9]),
                is_success=True
            )
        except Exception as e:
            print(e)
            return Prediction(
                operation=Operation(
                    score=0,
                    report=""
                ),
                total_population=TotalPopulation(
                    neighborhood=0,
                    district=0,
                ),
                median_income=MedianIncome(
                    neighborhood=0,
                    district=0,
                ),
                competitor_count=0,
                ai_insight=[],
                radar=Radar(
                    labels=[],
                    values=[],
                ),
                is_success=False
            )