# CV Analysis System

A Django-based application that:

1. **Processes** uploaded CVs (PDF or .docx) via OCR and text extraction.
2. **Parses** the extracted text with OpenAI GPT (structured JSON).
3. **Stores** candidate data (personal info, education, work experience, skills, projects, certifications).
4. **Provides** a rate-limited chatbot interface for querying the stored CV information.

---

## Features

- **Multi-Format Support**: Supports PDF (with OCR fallback) and Word documents.
- **OCR**: Automatically uses Tesseract if the PDF is image-based.
- **Structured Parsing**: Extracts key resume fields (personal info, education, work experience, skills, projects, certifications).
- **LLM Integration**: Leverages OpenAI GPT for transforming raw text into JSON.
- **Rate Limiting**: Middleware enforces a maximum of 10 requests per IP per hour.
- **Redis Cache**: Shared cache backend for consistent rate limiting across processes.
- **Chat Interface**: Users can query stored candidate data in natural language.

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


## Project Setup

Installation & Setup
Clone the Repository

bash
Copy
git clone https://github.com/YourUsername/YourRepo.git
cd YourRepo
Create a Virtual Environment (optional but recommended)

bash
Copy
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
Install Dependencies

bash
Copy
pip install -r requirements.txt
Configure Environment Variables

Copy .env.example to .env and fill in:
SECRET_KEY
DEBUG
OPENAI_KEY
Make sure Redis is running (redis://127.0.0.1:6379/1 in your settings.py).
Run Migrations

bash
Copy
python manage.py migrate
Start the Server

bash
Copy
python manage.py runserver
