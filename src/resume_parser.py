import re
import os
import PyPDF2
from docx import Document
from typing import Optional, List, Dict, Any

class ResumeParser:
    """Parse resume files (PDF/DOCX) and extract text content."""
    
    def __init__(self, file_path: str):
        """Initialize with the path to the resume file.
        
        Args:
            file_path: Path to the resume file (PDF or DOCX)
        """
        self.file_path = file_path
        self.file_type = self._get_file_type()
        
    def _get_file_type(self) -> str:
        """Determine the file type using file extension and magic numbers."""
        # First try to determine by file extension
        _, ext = os.path.splitext(self.file_path.lower())
        
        if ext == '.pdf':
            return 'pdf'
        elif ext in ['.docx', '.doc']:
            return 'docx'
        else:
            # Fallback to checking file signature
            try:
                with open(self.file_path, 'rb') as f:
                    header = f.read(4)
                    if header == b'%PDF':
                        return 'pdf'
                    elif header in [b'PK\x03\x04', b'\xD0\xCF\x11\xE0']:  # DOCX or DOC
                        return 'docx'
            except:
                pass
                
            raise ValueError(f"Unsupported file type: {self.file_path}")
    
    def extract_text(self) -> str:
        """Extract text from the resume file based on its type."""
        if self.file_type == 'pdf':
            return self._extract_from_pdf()
        elif self.file_type == 'docx':
            return self._extract_from_docx()
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}")
    
    def _extract_from_pdf(self) -> str:
        """Extract text from a PDF file."""
        text = ""
        try:
            with open(self.file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
        return text
    
    def _extract_from_docx(self) -> str:
        """Extract text from a DOCX file."""
        try:
            doc = Document(self.file_path)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            # If it's a .doc file, try using textract if available
            if self.file_path.lower().endswith('.doc'):
                try:
                    import textract
                    return textract.process(self.file_path).decode('utf-8')
                except:
                    pass
            raise Exception(f"Error extracting text from DOCX: {str(e)}. Please ensure the file is not corrupted and is a valid Word document.")
    
    def clean_text(self, text: str) -> str:
        """Clean and preprocess the extracted text."""
        # Remove special characters and extra whitespace
        text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with single space
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII characters
        text = text.strip()
        return text
    
    def parse(self) -> Dict[str, Any]:
        """Parse the resume and return structured data."""
        try:
            raw_text = self.extract_text()
            clean_text = self.clean_text(raw_text)
            
            return {
                'raw_text': raw_text,
                'clean_text': clean_text,
                'file_type': self.file_type,
                'file_name': os.path.basename(self.file_path)
            }
        except Exception as e:
            raise Exception(f"Error parsing resume: {str(e)}")
