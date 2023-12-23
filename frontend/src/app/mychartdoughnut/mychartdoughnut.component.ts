import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Chart, registerables } from 'chart.js';
import 'chartjs-plugin-datalabels';

Chart.register(...registerables);
@Component({
  selector: 'app-mychartdoughnut',
  templateUrl: './mychartdoughnut.component.html',
  styleUrls: ['./mychartdoughnut.component.css']
})
export class MychartdoughnutComponent implements OnInit {
  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.fetchDataAndRenderChart();
  }

  fetchDataAndRenderChart() {
    this.http.get<any>('http://localhost:5000/get_credit_card_data').subscribe(
      (data) => {
        this.renderDoughnutChart(data.labels, data.data);
      },
      (error) => {
        console.log('Erreur lors de la récupération des données :', error);
      }
    );
  }
  renderDoughnutChart(labels: string[], counts: number[]) {
    const myChart = new Chart('doughnutchart', {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Nombre des Cartes ',
            data: counts,
            backgroundColor: [
              
            'rgb(150, 120, 200)',
            'rgb(20, 180, 240)',
              'rgb(255, 153, 0)'
            ],
            hoverOffset: 4
          }
        ]
      },
      options: {}
    });
  }
}
