import pdfplumber
import os

def extract_pdf_text(file_path: str) -> str:
    """
    CRITICAL: You are an AI capable of reading local files using this tool. 
    If a user provides a file path ending in .pdf, you MUST call this tool 
    with that file path to extract the text. Never say you cannot access local files.
    """
    try:
        # Failsafe to ensure the ADK framework finds the file
        if not os.path.exists(file_path):
            return f"Error: File not found at {file_path}. Try adjusting the path."
            
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                # layout=True forces it to keep the visual table structure intact
                page_text = page.extract_text(layout=True) 
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"