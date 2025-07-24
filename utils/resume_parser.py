from pdfminer.high_level import extract_text
import docx
import re

def clean_resume_text(text):
    # Remove multiple spaces, newlines, and weird characters
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII
    return text.strip()

def extract_resume_text(path):
    raw_text = ""
    
    if path.endswith('.pdf'):
        raw_text = extract_text(path)
    elif path.endswith('.docx'):
        doc = docx.Document(path)
        raw_text = '\n'.join([para.text for para in doc.paragraphs])
    else:
        return "Unsupported file format"
    
    return clean_resume_text(raw_text)
