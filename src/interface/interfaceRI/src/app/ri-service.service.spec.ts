import { TestBed, inject } from '@angular/core/testing';

import { RiServiceService } from './ri-service.service';

describe('RiServiceService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [RiServiceService]
    });
  });

  it('should be created', inject([RiServiceService], (service: RiServiceService) => {
    expect(service).toBeTruthy();
  }));
});
