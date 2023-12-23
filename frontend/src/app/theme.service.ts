import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ThemeService {
  private isDarkMode: boolean = false;

  constructor() {}

  toggleDarkMode(): void {
    this.isDarkMode = !this.isDarkMode;
    // Appliquez ici les modifications de thème en fonction de this.isDarkMode
  }

  getIsDarkMode(): boolean {
    return this.isDarkMode;
  }
}
