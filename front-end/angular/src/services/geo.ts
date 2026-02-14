import { BACK_END_URL, HEADERS } from "../common";

export class GeoService {
    // 取得所有城市列表
    async getCitiesList(): Promise<string[]> {
        try {
            console.log("BACK_END_URL", BACK_END_URL);
            const response = await fetch(`${BACK_END_URL}/cities`, { headers: HEADERS });
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error("無法取得城市列表:", error);
            return [];
        }
    }

    // 取得行政區列表
    async getDistrictsList(cityName: string): Promise<string[]> {
        try {
            const response = await fetch(`${BACK_END_URL}/districts/${cityName}`, { headers: HEADERS });
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error("無法取得行政區列表:", error);
            return [];
        }
    }

    // 取得里列表
    async getNeighborhoodsList(cityName: string, districtName: string): Promise<string[]> {
        try {
            const response = await fetch(`${BACK_END_URL}/neighborhoods/${cityName}/${districtName}`, { headers: HEADERS });
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error("無法取得里列表:", error);
            return [];
        }
    }

    // 檢查地理資訊是否有效
    async is_valid_geo(cityName: string, districtName: string, neighborhoodName: string): Promise<boolean> {
        try {
            const response = await fetch(`${BACK_END_URL}/geo_check/${cityName}/${districtName}/${neighborhoodName}`, { headers: HEADERS });
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error("無法檢查地理資訊:", error);
            return false;
        }
    }
}