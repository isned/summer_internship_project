import { Component, OnInit } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Observable } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators';
import { Router } from '@angular/router'; // Importez le Router depuis @angular/router
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.css']
})
export class NavigationComponent implements OnInit {
  constructor(private breakpointObserver: BreakpointObserver, private router: Router, private http: HttpClient) { } // Injectez le BreakpointObserver et le Router
  ngOnInit(): void {
    const userLoggedIn = localStorage.getItem('idUser');
    if (!userLoggedIn) {
      this.router.navigate(['/login']);
    }
  }

  logout() {
    localStorage.removeItem('idUser'); 
    this.http.get<any>('http://localhost:5000/logout', { withCredentials: true }).subscribe(
        () => {
            localStorage.removeItem('idUser');
            this.router.navigate(['/login']);
        },
        (error) => {
            console.error('Erreur lors de la déconnexion :', error);
        }
    );
}


  isHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(
      map(result => result.matches),
      shareReplay()
    );

  //showTable = false; // Initialiser à false pour masquer le composant table
  showDashboard = true; // Initialiser à true pour afficher la dashboard
  showTable = false;
  showClient = false ;
  // Gestionnaire d'événements pour le lien "Link 1"
  onLink1Click() {
    this.showDashboard = true; // Masquer la dashboard
    this.showTable = false;
    this.showClient = false;
  }
  onLink2Click() {
    this.showTable = true;
    this.showDashboard = false;
    this.showClient=false;
  }
  onLink3Click(){
    this.showTable = false;
    this.showDashboard = false;
    this.showClient=true;
  }
}








