import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

@Component({
  selector: 'app-linechart',
  templateUrl: './linechart.component.html',
  styleUrls: ['./linechart.component.css']
})
export class LinechartComponent implements OnInit {
  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.fetchDataAndRenderChart();
  }

  fetchDataAndRenderChart() {
    this.http.get<any>('http://localhost:5000/get_country_churn_rate_data').subscribe(
      (data) => {
        this.renderLineChart(data);
      },
      (error) => {
        console.log('Erreur lors de la récupération des données :', error);
      }
    );
  }

  renderLineChart(data: any[]) {
    const countries = data.map(entry => entry.country);
    const churnRates = data.map(entry => entry.churn_rate);

    const myChart = new Chart('linechart', {
      type: 'line',
      data: {
        labels: countries,
        datasets: [
          {
            label: 'Taux de désabonnement moyen par pays',
            data: churnRates,
            borderColor: 'rgb(75, 192, 192)',
            borderWidth: 1,
            fill: false,
            tension: 0.1
          },
        ],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }
}
