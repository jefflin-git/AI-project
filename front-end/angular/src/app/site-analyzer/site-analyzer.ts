import { Component, OnInit, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import Chart from 'chart.js/auto';

@Component({
  selector: 'app-site-analyzer',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './site-analyzer.html',
  styleUrls: ['./site-analyzer.css']
})
export class SiteAnalyzerComponent implements OnInit {
  // 模擬資料庫
  db: any = {
    "臺北市": {
      "中正區": ["板溪里", "網溪里", "頂東里", "水源里"],
      "大安區": ["古莊里", "龍泉里", "學府里"],
      "信義區": ["西村里", "正和里", "興雅里"]
    },
    "新北市": {
      "板橋區": ["深丘里", "香邱里", "西安里", "東丘里"],
      "新莊區": ["立言里", "立泰里", "中平里"],
      "八里區": ["舊城里", "訊塘里", "龍源里"]
    }
  };

  // 表單綁定變數
  selectedCity = '臺北市';
  selectedDistrict = '';
  selectedNeighborhood = '';
  selectedBrand = '便利商店';
  districts: string[] = [];
  neighborhoods: string[] = [];

  // 狀態控制
  isLoading = false;
  showResult = false;

  // 數據與圖表
  score = 0;
  pop = 0;
  income = 0;
  comp = 0;
  aiInsight = '';

  private charts: any = {};

  ngOnInit() {
    this.updateDistricts();
  }

  updateDistricts() {
    this.districts = Object.keys(this.db[this.selectedCity]);
    this.selectedDistrict = this.districts[0];
    this.updateNeighborhoods();
  }

  updateNeighborhoods() {
    this.neighborhoods = this.db[this.selectedCity][this.selectedDistrict] || [];
    this.selectedNeighborhood = this.neighborhoods[0];
  }

  runPrediction() {
    this.isLoading = true;

    // 模擬 API 延遲
    setTimeout(() => {
      this.isLoading = false;
      this.showResult = true;
      this.generateResult();
    }, 800);
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