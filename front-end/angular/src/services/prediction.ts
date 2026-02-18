import { BACK_END_URL, HEADERS } from "../common";
import { IPrediction, Prediction } from "../value-objects/prediction";
import { Operation } from "../value-objects/operation";
import { TotalPopulation } from "../value-objects/population";
import { MedianIncome } from "../value-objects/income";
import { Radar } from "../value-objects/radar";

export class PredictionService {
    // 執行預測
    async runPrediction(city: string, district: string, neighborhood: string, brand: string): Promise<IPrediction> {
        try {
            const response = await fetch(`${BACK_END_URL}/run-prediction/${city}/${district}/${neighborhood}/${brand}`, { headers: HEADERS });
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            return new Prediction(
                new Operation(data.operation.score, data.operation.report),
                new TotalPopulation(data.totalPopulation.neighborhood, data.totalPopulation.district),
                new MedianIncome(data.medianIncome.neighborhood, data.medianIncome.district),
                data.competitorCount,
                data.aiInsight,
                new Radar(data.radar.labels, data.radar.values),
            );
        } catch (error) {
            console.error("無法執行預測:", error);
            return new Prediction(
                new Operation(0, ""),
                new TotalPopulation(0, 0),
                new MedianIncome(0, 0),
                0,
                "",
                new Radar(0, 0, 0, 0, 0)
            );
        }
    }
}