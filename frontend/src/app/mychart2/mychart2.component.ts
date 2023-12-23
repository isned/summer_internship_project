import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Chart, registerables } from 'chart.js';
import 'chartjs-plugin-datalabels';

Chart.register(...registerables);

@Component({
  selector: 'app-mychart2',
  templateUrl: './mychart2.component.html',
  styleUrls: ['./mychart2.component.css']
})
export class Mychart2Component implements OnInit {
  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.fetchDataAndRenderChart();
  }

  fetchDataAndRenderChart() {
    this.http.get<any>('http://localhost:5000/get_pie_data').subscribe(
      (data) => {
        this.renderPieChart(data.labels, data.data);
      },
      (error) => {
        console.log('Erreur lors de la récupération des données :', error);
      }
    );
  }

  renderPieChart(labels: string[], data: number[]) {
    const myChart = new Chart("piechart", {
      type: 'pie',
      data: {
        labels: labels,
        datasets: [{
          label: 'Le Nombre des clients est',
          data: data,
          backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)',
            'rgba(0, 128, 0, 0.5)',
          ],
        }]
      },
      options: {}
    });
  }
}
