import os

import pdfplumber
import pytesseract
from django.conf import settings
from docx import Document

pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using a combination of pdfplumber and OCR.

    This function first attempts to extract text directly using pdfplumber.
    If no text is found on a page, it falls back to OCR using pytesseract.

    Args:
        pdf_path (str): Path to the PDF file to be processed.

    Returns:
        str: Extracted text from all pages of the PDF, with each page's
             content separated by newlines.

    Note:
        The function uses Tesseract OCR with specific configuration:
        - Language: English
        - PSM Mode: 4 (Assume a single column of text)
        - OEM Mode: 3 (Default)
    """

    text_data = set()
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text and text.strip():
                text_data.add(text)
            else:
                page_img = page.to_image(resolution=400)
                pil_image = page_img.original.convert("L")
                ocr_text = pytesseract.image_to_string(
                    pil_image, lang="eng", config="--psm 4 --oem 3"
                )
                text_data.add(ocr_text)

    return "\n".join(text for text in text_data)


def extract_text_from_docx(docx_path):
    """
    Extract structured text from a .docx file using python-docx.
    Returns a string combining paragraphs
    """
    doc = Document(docx_path)
    text_data = set()
    for paragraph in doc.paragraphs:
        style_name = paragraph.style.name if paragraph.style else ""
        if "List" in style_name or "Bullet" in style_name or "Number" in style_name:
            line = f"- {paragraph.text}"
        else:
            line = paragraph.text
        text_data.add(line)

    return "\n".join(text for text in text_data)


def extract_text_from_file(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    if extension == ".pdf":
        return extract_text_from_pdf(file_path)
    elif extension == ".docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format")
