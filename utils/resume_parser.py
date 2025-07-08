from pdfminer.high_level import extract_text
import docx

def extract_resume_text(path):
    if path.endswith('.pdf'):
        return extract_text(path)
    elif path.endswith('.docx'):
        doc = docx.Document(path)
        return '\n'.join([para.text for para in doc.paragraphs])
    else:
        return "Unsupported file format"
