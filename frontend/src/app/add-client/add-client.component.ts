import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MatDialog } from '@angular/material/dialog';
import { SuccessDialogComponent } from '../success-dialog/success-dialog.component';
@Component({
  selector: 'app-add-client',
  templateUrl: './add-client.component.html',
  styleUrls: ['./add-client.component.css']
})
export class AddClientComponent {
  newCustomer = {
    credit_score: null,
    country: '',
    gender: '',
    age: null,
    anciennete: null,
    solde: null,
    carte_de_credit: '',
    membre_actif: '',
    salaire_estime: null,
    desabonnement: ''
  };

  constructor(private http: HttpClient, private dialog: MatDialog) {}

  addCustomer() {
    // Convert radio button values to integers
    this.newCustomer.carte_de_credit = this.newCustomer.carte_de_credit === 'oui' ? '1' : '0';
    this.newCustomer.membre_actif = this.newCustomer.membre_actif === 'oui' ? '1' : '0';
    this.newCustomer.desabonnement = this.newCustomer.desabonnement === 'oui' ? '1' : '0';
  
    this.http.post('http://localhost:5000/add_customer', this.newCustomer)
      .subscribe(
        (data) => {
          console.log(data);
          this.openSuccessDialog(); // Open the success dialog
        },
        (error) => {
          console.error(error);
          console.error('Error details:', error.message, error.status, error.statusText);
        }
      );
  }
  
  openSuccessDialog() {
    const dialogRef = this.dialog.open(SuccessDialogComponent);
  
    dialogRef.afterClosed().subscribe(result => {
      // Handle any actions after the dialog is closed, if needed
    });
  }
}
