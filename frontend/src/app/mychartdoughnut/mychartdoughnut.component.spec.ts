import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MychartdoughnutComponent } from './mychartdoughnut.component';

describe('MychartdoughnutComponent', () => {
  let component: MychartdoughnutComponent;
  let fixture: ComponentFixture<MychartdoughnutComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [MychartdoughnutComponent]
    });
    fixture = TestBed.createComponent(MychartdoughnutComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
