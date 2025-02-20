# CV Analysis System

A Django-based application that:

1. **Processes** uploaded CVs (PDF or .docx) via OCR and text extraction.
2. **Parses** the extracted text with OpenAI GPT (structured JSON).
3. **Stores** candidate data (personal info, education, work experience, skills, projects, certifications).
4. **Provides** a rate-limited chatbot interface for querying the stored CV information.

---

## Features

- **File Upload**: Supports PDF (with OCR fallback) and Word documents.
- **Structured Data Extraction**: Uses GPT in JSON-schema mode to produce consistent output.
- **Rate Limiting**: Restricts API usage to 10 requests per hour per IP.
- **Chatbot**: Query candidate data with natural language (e.g., “Who has X skill?”).

---

## Requirements & Prerequisites

1. **Python 3.8+**
2. **Django** (version pinned in `requirements.txt`)
3. **Redis**
4. **Tesseract OCR** (for extracting text from scanned PDFs)
   - Ubuntu/Debian:
     ```bash
     sudo apt-get update
     sudo apt-get install tesseract-ocr
     ```
   - macOS (Homebrew):
     ```bash
     brew install tesseract
     ```
   - Windows: [Download from official Tesseract page](https://github.com/UB-Mannheim/tesseract/wiki).

---
5. **OpenAI API Key** (to call GPT endpoints)
