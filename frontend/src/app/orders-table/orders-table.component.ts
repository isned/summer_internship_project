import { MatTableDataSource } from '@angular/material/table';
import { Router } from '@angular/router';
import { Component, ViewChild, OnInit } from '@angular/core';
import { MatTable } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { HttpClient } from '@angular/common/http';
import { MatDialog } from '@angular/material/dialog';
import { OrdersTableDataSource, OrdersTableItem } from './orders-table-datasource';
import { EditClientComponent } from '../edit-client/edit-client.component';

@Component({
  selector: 'app-orders-table',
  templateUrl: './orders-table.component.html',
  styleUrls: ['./orders-table.component.css']
})
export class OrdersTableComponent implements OnInit {
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;
  @ViewChild(MatTable) table!: MatTable<OrdersTableItem>;
  displayedColumns = ['id', 'credit_score', 'country', 'gender', 'age', 'tenure', 'balance',  'credit_card', 'active_member', 'estimated_salary', 'churn','actions'];
  dataSource!: MatTableDataSource<any>; // Initialize dataSource here // Declare dataSource once

  constructor(private http: HttpClient, private dialog: MatDialog, private router: Router) {}

  ngOnInit(): void {
    this.dataSource = new MatTableDataSource();
    this.dataSource.paginator = this.paginator;

    // Call the get_customers API and update the data source
    this.http.get<any>('http://localhost:5000/get_customers').subscribe(
      (data) => {
        this.dataSource.data = data;
        this.dataSource.sort = this.sort;
        this.table.dataSource = this.dataSource;
      },
      (error) => {
        console.log('Error retrieving data:', error);
      }
    );
  }

  deleteCustomer(customerId: number) {
    this.http.delete(`http://localhost:5000/delete_customer/${customerId}`).subscribe(
      (response) => {
        console.log(response);
        this.refreshTableDataAfterDeletion(customerId);
      },
      (error) => {
        console.error('Error deleting customer:', error);
      }
    );
  }

  refreshTableDataAfterDeletion(deletedCustomerId: number) {
    // Mettez à jour la source de données de la table après la suppression
    this.dataSource.data = this.dataSource.data.filter(item => item.id !== deletedCustomerId);
  }

  editCustomer(customerId: number) {
    const dialogRef = this.dialog.open(EditClientComponent, {
      width: '400px',
      height: '600px',
      data: {
        customerId,
        updatedData: { ...this.dataSource.data.find(item => item.id === customerId) }
      }
    });
  
    dialogRef.afterClosed().subscribe(result => {
      if (result === 'edited') {
        // Handle refresh or other actions after editing
        
        
      }
    });
  }
 /* editCustomer(customerId: number) {
    const dialogRef = this.dialog.open(EditClientComponent, {
      width: '400px',
      height: '600px',
      data: {
        customerId,
        updatedData: { ...this.dataSource.data.find(item => item.id === customerId) }
      }
    });
  
    dialogRef.afterClosed().subscribe(result => {
      if (result === 'edited') {
        // Mettre à jour les données après l'édition
        const updatedItemIndex = this.dataSource.data.findIndex(item => item.id === customerId);
        if (updatedItemIndex !== -1) {
          // Mettre à jour les données dans le tableau de données
          this.dataSource.data[updatedItemIndex] = dialogRef.componentInstance.updatedData;
          console.log('Données mises à jour dans le tableau :', this.dataSource.data[updatedItemIndex]);
        }
      }
    });
    
  }*/
  /*editCustomer(customerId: number) {
    const dialogRef = this.dialog.open(EditClientComponent, {
      width: '400px',
      height: '600px',
      data: {
        customerId,
        updatedData: { ...this.dataSource.data.find(item => item.id === customerId) }
      }
    });
  
    dialogRef.afterClosed().subscribe(result => {
      if (result === 'edited') {
        // Mettre à jour les données après l'édition
        const updatedItemIndex = this.dataSource.data.findIndex(item => item.id === customerId);
        if (updatedItemIndex !== -1) {
          // Mettre à jour les données dans le tableau de données
          this.dataSource.data[updatedItemIndex] = dialogRef.componentInstance.updatedData;
          console.log('Données mises à jour dans le tableau :', this.dataSource.data[updatedItemIndex]);
          
          // Mettre à jour la source de données de la table pour rafraîchir la vue
          this.dataSource.data = [...this.dataSource.data];
        }
      }
    });
  }
  
  /*editCustomer(customerId: number) {
    const dialogRef = this.dialog.open(EditClientComponent, {
      width: '400px',
      height: '600px',
      data: {
        customerId,
        updatedData: { ...this.dataSource.data.find(item => item.id === customerId) }
      }
    });
  
    dialogRef.afterClosed().subscribe(result => {
      if (result === 'edited') {
        // Call a function to refresh data in the table
        this.refreshTableData();
      }
    });
  }
  
  // Function to refresh data in the table
  refreshTableData() {
    // Fetch and update your data source here
    this.getDataFromServer().subscribe(data => {
      this.dataSource.data = data;
    });
  }
  
  // Simulate fetching data from server
  getDataFromServer() {
    // Replace 'your_api_endpoint' with the actual API endpoint to fetch updated customer data
    return this.http.get<any[]>('/get_all_customers');
  }
  */
  
}
