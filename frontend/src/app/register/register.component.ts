import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  registerForm: FormGroup | any;
  hidePassword = true;
  message: string | undefined; // Message à afficher à l'utilisateur

  constructor(private formBuilder: FormBuilder, private http: HttpClient) {}

  ngOnInit() {
    this.registerForm = this.formBuilder.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  onRegister() {
    if (this.registerForm.valid) {
      const registrationData = this.registerForm.value;

      this.http.post<any>('http://localhost:5000/create_db_user', registrationData).subscribe(
        response => {
          console.log(response); 
          if (response.message === 'Database user created successfully') {  // Modifiez ici
            this.message = 'Inscription réussie !'; 
          } else {
            this.message = 'Lenregistrement a échoué. Veuillez réessayer.'; 
          }
        },
        error => {
          console.error(error); 
          this.message = 'Une erreur est produite. Veuillez réessayer.'; 
        }
      );
      
    }
  }

  togglePasswordVisibility() {
    this.hidePassword = !this.hidePassword;
  }
}
