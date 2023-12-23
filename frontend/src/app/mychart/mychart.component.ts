import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

@Component({
  selector: 'app-mychart',
  templateUrl: './mychart.component.html',
  styleUrls: ['./mychart.component.css']
})
export class MychartComponent implements OnInit {
  constructor(private http: HttpClient) {}
  
  ngOnInit(): void {
    this.fetchDataAndRenderChart();
  }
   
  fetchDataAndRenderChart() {
    this.http.get<any>('http://localhost:5000/get_bar_data').subscribe(
      (data) => {
        this.renderBarChart(data.labels, data.data);
      },
      (error) => {
        console.log('Erreur lors de la récupération des données :', error);
      }
    );
  }

  renderBarChart(labels: string[], data: number[]) {
    const myChart = new Chart('barchart', {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Pourcentage est',
            data: data,
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(255, 159, 64, 0.2)',
            ],
            borderColor: [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)',
            ],
            borderWidth: 1,
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
