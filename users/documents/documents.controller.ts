import { Controller, Post, Body, UseGuards, Get } from '@nestjs/common';
import { DocumentsService } from './documents.service';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { DocumentDto } from './dto';

@Controller('documents')
export class DocumentsController {
  constructor(private documentsService: DocumentsService) {}

  @UseGuards(JwtAuthGuard)
  @Post('upload')
  async uploadDocument(@Body() documentDto: DocumentDto) {
    return this.documentsService.uploadDocument(documentDto);
  }

  @UseGuards(JwtAuthGuard)
  @Get()
  async listDocuments() {
    return this.documentsService.listDocuments();
  }
}
