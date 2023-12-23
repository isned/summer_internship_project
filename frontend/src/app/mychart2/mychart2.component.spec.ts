import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Mychart2Component } from './mychart2.component';

describe('Mychart2Component', () => {
  let component: Mychart2Component;
  let fixture: ComponentFixture<Mychart2Component>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [Mychart2Component]
    });
    fixture = TestBed.createComponent(Mychart2Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
