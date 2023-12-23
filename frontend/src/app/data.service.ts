import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  // Exemple de données, remplacez-le par vos propres données
  customers: any[] = [];

  constructor() {}
  
  deleteCustomer(customerId: number) {
    // Code pour supprimer le client avec customerId
    // Après la suppression, mettez à jour this.customers
  }
}
