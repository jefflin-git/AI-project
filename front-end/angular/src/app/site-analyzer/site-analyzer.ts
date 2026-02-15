import { Component, OnInit, AfterViewInit, ViewChild, ElementRef, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import Chart from 'chart.js/auto';
import { GeoService } from '../../services/geo';
import { BrandService } from '../../services/brand';

@Component({
  selector: 'app-site-analyzer',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './site-analyzer.html',
  styleUrls: ['./site-analyzer.css']
})
export class SiteAnalyzerComponent implements OnInit {
  // 服務
  private geoService = new GeoService();
  private brandService = new BrandService();

  // 表單綁定變數
  selectedCity: string = '';
  selectedDistrict: string = '';
  selectedNeighborhood: string = '';
  selectedBrand: string = '';

  // 城市下拉選單
  cities: string[] = [];
  // 行政區下拉選單
  districts: string[] = [];
  // 里別下拉選單
  neighborhoods: string[] = [];
  // 品牌下拉選單
  brands: string[] = [];

  // 狀態控制
  isLoading: boolean = false;
  showResult: boolean = false;

  // 數據與圖表
  score: number = 0;
  pop: number = 0;
  income: number = 0;
  comp: number = 0;
  aiInsight: string = '';

  private charts: any = {};

  async ngOnInit() {
    await this.SetDefault();
  }

  async SetDefault() {
    await this.updateCity();
    this.selectedCity = this.cities[0];
    await this.updateDistricts();
    this.selectedDistrict = this.districts[0];
    await this.updateNeighborhoods();
    this.selectedNeighborhood = this.neighborhoods[0];
    await this.updateBrands();
    this.selectedBrand = this.brands[0];
  }

  async updateCity() {
    this.selectedCity = '';
    this.selectedDistrict = '';
    this.selectedNeighborhood = '';
    this.cities = await this.geoService.getCityList();
    console.log("cities", this.cities);
  }

  async updateDistricts() {
    this.selectedDistrict = '';
    this.selectedNeighborhood = '';
    this.districts = await this.geoService.getDistrictList(this.selectedCity);
  }

  async updateNeighborhoods() {
    this.selectedNeighborhood = '';
    this.neighborhoods = await this.geoService.getNeighborhoodList(this.selectedCity, this.selectedDistrict);
  }

  async updateBrands() {
    this.brands = await this.brandService.getBrandList();
  }

  async checkGeo() {
    const result = await this.geoService.checkValidGeo(this.selectedCity, this.selectedDistrict, this.selectedNeighborhood);
    if (result) {
      return true;
    }
    return false;
  }

  runPrediction() {
    if (!this.checkGeo()) {
      console.log(this.selectedCity, this.selectedDistrict, this.selectedNeighborhood);
      alert('請完整選擇縣市、行政區與里別');
      return;
    }
    // this.isLoading = true;

    // 模擬 API 延遲
    // setTimeout(() => {
    //   this.isLoading = false;
    //   this.showResult = true;
    //   this.generateResult();
    // }, 8);
  }

  generateResult() {
    let baseScore = (this.selectedCity === "臺北市") ? 80 : 70;
    if (this.selectedDistrict === "板橋區" || this.selectedDistrict === "大安區") baseScore += 10;

    this.score = Math.min(99.9, Math.max(40, baseScore + Math.floor(Math.random() * 20) - 5));
    this.pop = Math.floor(Math.random() * 5000) + 2000;
    this.income = Math.floor(Math.random() * 50) + 60;
    this.comp = Math.floor(Math.random() * 8);

    this.aiInsight = `該地點位於 <strong>${this.selectedDistrict} ${this.selectedNeighborhood}</strong>。AI 模型分析顯示，該區域具備 <strong>${this.income > 80 ? '高消費力' : '穩定基礎客群'}</strong> 的特徵。雖然周邊已有 ${this.comp} 家競店，但考慮到品牌 (${this.selectedBrand}) 的集客力，預估能達到 ${this.score.toFixed(1)} 的銷售指標。`;

    // 使用 setTimeout 確保 DOM 已更新再渲染圖表
    setTimeout(() => this.renderCharts(), 0);
  }

  getScoreClass() {
    if (this.score >= 90) return { badge: 'bg-success', text: '極具潛力 (Prime)', color: '#198754' };
    if (this.score >= 70) return { badge: 'bg-warning text-dark', text: '潛力良好 (Good)', color: '#ffc107' };
    return { badge: 'bg-danger', text: '需審慎評估 (Caution)', color: '#dc3545' };
  }

  renderCharts() {
    const chartConfigs = [
      { id: 'popChart', type: 'bar' as const, data: [this.pop, 4000], colors: ['#36A2EB', '#C8C8C8'] },
      { id: 'incomeChart', type: 'bar' as const, data: [this.income, 80], colors: ['#4BC0C0', '#C8C8C8'] }
    ];

    chartConfigs.forEach(conf => {
      if (this.charts[conf.id]) this.charts[conf.id].destroy();
      const ctx = document.getElementById(conf.id) as HTMLCanvasElement;
      this.charts[conf.id] = new Chart(ctx, {
        type: conf.type,
        data: {
          labels: ['該里', '行政區平均'],
          datasets: [{ data: conf.data, backgroundColor: conf.colors, barThickness: 30 }]
        },
        options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
      });
    });

    // 雷達圖
    if (this.charts['radarChart']) this.charts['radarChart'].destroy();
    const radarCtx = document.getElementById('radarChart') as HTMLCanvasElement;
    this.charts['radarChart'] = new Chart(radarCtx, {
      type: 'radar',
      data: {
        labels: ['內部競爭', '外部競爭', '熱鬧據點數', '熱點距離便利性', '租金成本'],
        datasets: [{
          label: '選址評分維度',
          data: Array.from({ length: 5 }, () => Math.random() * 10),
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgb(255, 99, 132)'
        }]
      },
      options: { scales: { r: { suggestedMin: 0, suggestedMax: 10 } } }
    });
  }
}