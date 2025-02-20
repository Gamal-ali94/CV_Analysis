# Django CV Analysis Project

A simple Django-based application that handles CV uploads (PDF or Word), uses OCR for text extraction, parses the content via an LLM (OpenAI GPT), and provides a chat-based interface for querying the stored information.

## Features
- **Multi-Format Support**: Accepts both PDF and `.docx` files.
- **OCR**: Automatically uses Tesseract if the PDF is image-based.
- **Structured Parsing**: Extracts key resume fields (personal info, education, work experience, skills, projects, certifications).
- **LLM Integration**: Leverages OpenAI GPT to convert raw text into JSON.
- **Chat Interface**: Users can query stored candidate data in natural language.
- **Rate Limiting**: Middleware enforces 10 requests per IP per hour.
- **Redis Cache**: Shared cache backend to support scaling and ensure consistent throttling.

---

## Key Files
- **`models.py`**: Defines the `Candidate` model (storing parsed CV data).
- **`forms.py`**: Contains `CandidateForm` (for uploading CVs) and `PromptForm` (for chatbot prompts).
- **`views.py`**: Includes `upload_cv`, `candidate_view`, and `handle_response` for the chatbot.
- **`urls.py`**: Routes for `upload_cv`, `candidate_view`, and the chat endpoint (`/chat/`).
- **`ocr.py`**: Provides OCR utilities for both PDFs (pdfplumber + pytesseract) and `.docx` files.
- **`openai_services.py`**: Handles the LLM prompt logic with OpenAI (parsing resumes into JSON).
- **`middleware.py`**: Implements IP-based rate limiting using a Redis cache.

---

## Core App Overview

### Models

- **`Candidate`**
  - Stores JSON fields for:
    - `personal_info`
    - `education`
    - `work_experience`
    - `skills`
    - `projects`
    - `certificates`
  - Holds the uploaded CV file in `uploaded_file`.
  - Auto-tracks creation/update timestamps with `created_at` and `updated_at`.

### Forms

- **`CandidateForm`**
  - Validates uploaded files (PDF or `.docx` only).
  - Enforces a 5MB file size limit.

- **`PromptForm`**
  - Captures a single `prompt` field for the chatbot query.

### OCR

- **`extract_text_from_pdf`**
  - Attempts to extract text with `pdfplumber`.
  - Falls back to **Tesseract** if no text is found.

- **`extract_text_from_docx`**
  - Uses `python-docx` to parse paragraphs from a Word document.

### LLM Integration

- **`parse_resume_with_llm`**
  - Sends extracted text to OpenAI GPT with a strict JSON schema prompt.
  - Returns a structured JSON string containing personal info, education, work experience, skills, projects, and certificates.
  - Raises exceptions if JSON is malformed or if the OpenAI call fails.

### Views

- **`upload_cv`**
  - Renders a form for uploading a CV (`CandidateForm`).
  - Extracts text (with OCR if needed), calls the LLM to parse, and saves the structured data in `Candidate` fields.

- **`candidate_view`**
  - Displays the parsed CV details for a specific `Candidate`.

- **`handle_response`**
  - Implements a minimal chat interface where the user’s prompt is appended to a conversation history.
  - Sends candidate data + user prompt to OpenAI GPT, returning a response displayed to the user.

---

## How the Chat Querying Works

1. **User Enters a Prompt**
   For example: “Who has React skills?” or “Which candidate worked at Google?”.

2. **Data + Prompt → GPT**
   All `Candidate` data is retrieved. The user’s prompt plus the candidate data are appended to a conversation history in the session.

3. **GPT Responds**
   GPT interprets the question based on the provided data and returns the best match (or “not found”).

4. **Multi-Turn**
   The conversation history is retained in the session, allowing follow-up questions without losing context.

---
## Installation & Setup

1. **Install Dependencies**


    pip install -r requirements.txt

- For tesseract :

   - **Ubuntu/Debian**:
     ```bash
     sudo apt-get update
     sudo apt-get install tesseract-ocr
     ```
   - **macOS** (Homebrew):
     ```bash
     brew install tesseract
     ```
   - **Windows**: [Download from official Tesseract page](https://github.com/UB-Mannheim/tesseract/wiki).
---
- For Redis :
    - **Ubuntu/Debian**
    Ubuntu/Debian:
r
     ```bash
    sudo apt-get update
    sudo apt-get install redis-server
    sudo systemctl enable redis-server
    sudo systemctl start redis-serve
     ```

2. **Configure Environment Variables**
    Copy .env.example to .env and fill in:
        SECRET_KEY
        DEBUG
        OPENAI_KEY


3. **Run Migrations**
    python manage.py migrate


4. **Start the Server**
    python manage.py runserver
