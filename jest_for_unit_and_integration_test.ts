import { Test, TestingModule } from '@nestjs/testing';
import { DocumentsService } from './documents.service';
import { getRepositoryToken } from '@nestjs/typeorm';
import { Document } from './document.entity';
import { HttpService } from '@nestjs/axios';

describe('DocumentsService', () => {
  let service: DocumentsService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        DocumentsService,
        {
          provide: getRepositoryToken(Document),
          useValue: { create: jest.fn(), save: jest.fn() },
        },
        { provide: HttpService, useValue: { post: jest.fn() } },
      ],
    }).compile();

    service = module.get<DocumentsService>(DocumentsService);
  });

  it('should upload document', async () => {
    const result = await service.uploadDocument({ name: 'test', content: 'content' });
    expect(result).toEqual({ message: 'Document uploaded and ingestion triggered' });
  });
});
