import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NavigationComponent } from './navigation/navigation.component';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatCardModule } from '@angular/material/card';
import { MatMenuModule } from '@angular/material/menu';
import { DashboardComponent } from './dashboard/dashboard.component';
import { Mychart2Component } from './mychart2/mychart2.component';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { LinechartComponent } from './linechart/linechart.component';
import { MychartComponent } from './mychart/mychart.component';
import { MychartdoughnutComponent } from './mychartdoughnut/mychartdoughnut.component';
import { MatInputModule } from '@angular/material/input';
import { ReactiveFormsModule } from '@angular/forms';
import { LoginComponent } from './login/login.component';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';
import { RegisterComponent } from './register/register.component';
import { OrdersTableComponent } from './orders-table/orders-table.component';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatSortModule } from '@angular/material/sort';
import { WithCredentialsInterceptor } from './with-credentials.interceptor';
import { AddClientComponent } from './add-client/add-client.component';
import { MatRadioModule } from '@angular/material/radio';
import { FormsModule } from '@angular/forms';
import { EditClientComponent } from './edit-client/edit-client.component';
import { MatDialogModule } from '@angular/material/dialog';
import { SuccessDialogComponent } from './success-dialog/success-dialog.component';

@NgModule({
  declarations: [
    AppComponent,
    NavigationComponent,
    DashboardComponent,
    Mychart2Component,
    LinechartComponent,
    MychartComponent,
    MychartdoughnutComponent,
    LoginComponent,
    RegisterComponent,
    OrdersTableComponent,
    AddClientComponent,
    EditClientComponent,
    SuccessDialogComponent,
   




  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatToolbarModule,
    MatButtonModule,
    MatSidenavModule,
    MatIconModule,
    MatListModule,
    MatGridListModule,
    MatCardModule,
    MatMenuModule,
    HttpClientModule,
    MatInputModule,
    ReactiveFormsModule,
    MatTableModule,
    MatPaginatorModule,
    MatSortModule,
    MatRadioModule,
    FormsModule,
    MatDialogModule,
  

   


  ],
  providers: [{
    provide: HTTP_INTERCEPTORS,
    useClass: WithCredentialsInterceptor,
    multi: true
  }],
  bootstrap: [AppComponent]
})
export class AppModule { }
