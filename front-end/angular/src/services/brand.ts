import { BACK_END_URL, HEADERS } from "../common";

export class BrandService {
    // 取得所有品牌列表
    async getBrandsList(): Promise<string[]> {
        try {
            const response = await fetch(`${BACK_END_URL}/brands`, { headers: HEADERS });
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error("無法取得品牌列表:", error);
            return [];
        }
    }
}