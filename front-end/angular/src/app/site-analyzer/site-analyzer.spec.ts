import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SiteAnalyzer } from './site-analyzer';

describe('SiteAnalyzer', () => {
  let component: SiteAnalyzer;
  let fixture: ComponentFixture<SiteAnalyzer>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SiteAnalyzer]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SiteAnalyzer);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
