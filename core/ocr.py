import pdfplumber
import pytesseract
from docx import Document
from PIL import Image
import tempfile
import os


pytesseract.pytesseract.tesseract_cmd = r"C:\Users\JIM\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF.
    1- Ties to read text with pdfplumber.
    2- If no text is found on a page, tries to read text with pytesseract.
    """
    text_data = set()
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text and text.strip():
                text_data.add(text)
            else:
                page_img = page.to_image(resolution=400)
                pil_image = page_img.original.convert('L')
                ocr_text = pytesseract.image_to_string(
                    pil_image,
                    lang="eng",
                    config="--psm 4 --oem 3")
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
        raise ValueError(f"Unsupported file format")

