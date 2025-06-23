import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Document } from './document.entity';
import { HttpService } from '@nestjs/axios';
import { firstValueFrom } from 'rxjs';

@Injectable()
export class DocumentsService {
  constructor(
    @InjectRepository(Document)
    private documentRepository: Repository<Document>,
    private httpService: HttpService,
  ) {}

  async uploadDocument(documentDto: DocumentDto) {
    const document = this.documentRepository.create({
      name: documentDto.name,
      content: documentDto.content,
    });
    await this.documentRepository.save(document);
    await firstValueFrom(
      this.httpService.post('http://localhost:8000/ingest', { content: documentDto.content })
    );
    return { message: 'Document uploaded and ingestion triggered' };
  }

  async listDocuments() {
    return this.documentRepository.find();
  }
}
