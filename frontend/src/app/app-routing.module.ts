import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component'; // Importez le DashboardComponent
import { NavigationComponent } from './navigation/navigation.component';
import { RegisterComponent } from './register/register.component';
import { AddClientComponent } from './add-client/add-client.component';
import { EditClientComponent } from './edit-client/edit-client.component';
import { OrdersTableComponent } from './orders-table/orders-table.component';

const routes: Routes = [
  {
    path: 'login',
    component: LoginComponent
  },
  
  {
    path: 'dashboard', // Chemin pour le DashboardComponent
    component: NavigationComponent
  }, 
  { path: 'register', component: RegisterComponent },
  // Autres routes si nécessaire
  {
    path: '',
    redirectTo: '/login', // Redirige la racine vers la page de connexion
    pathMatch: 'full'
  },
  { path: 'add-client', component: AddClientComponent },
  { path: 'edit_client/:customerId', component: EditClientComponent }, 
  {path:'table',component:OrdersTableComponent},// Configurez la route avec le paramètre customerId
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }




