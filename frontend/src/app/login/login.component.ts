import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup | any;
  hide = true;
  showErrorMessage: boolean = false; // Propriété pour contrôler l'affichage du message d'erreur

  constructor(
    private formBuilder: FormBuilder,
    private router: Router,
    private http: HttpClient
  ) { }

  ngOnInit() {
    this.loginForm = this.formBuilder.group({
      username: ['', Validators.required], // Utilisez 'username' comme nom de champ
      password: ['', Validators.required]
    });
  }

  userLoggedOut = false; // Initialiser à false

  // ...

  onLogin() {
    const loginData = {
      username: this.loginForm.value.username,
      password: this.loginForm.value.password
    };

    this.http.post<any>('http://localhost:5000/login', loginData, { withCredentials: true }).subscribe(
      response => {
        console.log(response);
        console.log(response.session)
        localStorage.setItem('idUser', response.idUser); // Stocker l'état de connexion

        this.router.navigate(['/dashboard']);

      },
      error => {
        console.error(error);
        this.showErrorMessage = true; // Afficher le message d'erreur
      }
    );
  }

  openRegister() {
    this.router.navigate(['/register']);
  }

  togglePasswordVisibility() {
    this.hide = !this.hide;
  }
}

