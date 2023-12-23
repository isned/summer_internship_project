import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private authToken: string | null = null;

  constructor() { }

  setAuthToken(token: string) {
    this.authToken = token;
  }

  getAuthToken(): string | null {
    return this.authToken;
  }

  // Ajoutez d'autres méthodes d'authentification ici (connexion, déconnexion, etc.)
}
