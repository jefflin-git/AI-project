import { ITotalPopulation } from "./population";
import { IMedianIncome } from "./income";
import { IRadar } from "./radar";

export interface IPrediction {
    readonly operationScore: number;
    readonly totalPopulation: ITotalPopulation;
    readonly medianIncome: IMedianIncome;
    readonly competitorCount: number;
    readonly aiInsight: string;
    readonly radar: IRadar;
}

export class Prediction implements IPrediction {
    constructor(
        public readonly operationScore: number,
        public readonly totalPopulation: ITotalPopulation,
        public readonly medianIncome: IMedianIncome,
        public readonly competitorCount: number,
        public readonly aiInsight: string,
        public readonly radar: IRadar
    ) { }
}