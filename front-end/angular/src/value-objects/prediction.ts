import { IOperation } from "./operation";
import { ITotalPopulation } from "./population";
import { IMedianIncome } from "./income";
import { IRadar } from "./radar";

export interface IPrediction {
    readonly operation: IOperation;
    readonly totalPopulation: ITotalPopulation;
    readonly medianIncome: IMedianIncome;
    readonly competitorCount: number;
    readonly aiInsight: string;
    readonly radar: IRadar;
    readonly isSuccess: boolean;
}

export class Prediction implements IPrediction {
    constructor(
        public readonly operation: IOperation,
        public readonly totalPopulation: ITotalPopulation,
        public readonly medianIncome: IMedianIncome,
        public readonly competitorCount: number,
        public readonly aiInsight: string,
        public readonly radar: IRadar,
        public readonly isSuccess: boolean
    ) { }
}