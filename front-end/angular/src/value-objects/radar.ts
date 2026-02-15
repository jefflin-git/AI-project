export interface IRadar {
    readonly internalCompetition: number;
    readonly externalCompetition: number;
    readonly hotSpotCount: number;
    readonly hotSpotDistance: number;
    readonly rentalCost: number;
}

export class Radar implements IRadar {
    constructor(
        public readonly internalCompetition: number,
        public readonly externalCompetition: number,
        public readonly hotSpotCount: number,
        public readonly hotSpotDistance: number,
        public readonly rentalCost: number
    ) { }
}