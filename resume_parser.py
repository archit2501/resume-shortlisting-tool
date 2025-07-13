"""
Resume Parser Module
Handles PDF text extraction and resume preprocessing
"""

import fitz  # PyMuPDF
import re
from typing import Dict, Optional
from utils import clean_text, extract_email, extract_phone, load_spacy_model, extract_skills_from_text

class ResumeParser:
    def __init__(self):
        """Initialize the resume parser with spaCy model"""
        self.nlp = load_spacy_model()
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF file using PyMuPDF
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as string
        """
        try:
            doc = fitz.open(pdf_path)
            text = ""
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text += page.get_text()
            
            doc.close()
            return text
            
        except Exception as e:
            print(f"Error extracting text from PDF: {str(e)}")
            return ""
    
    def extract_contact_info(self, text: str) -> Dict[str, str]:
        """
        Extract contact information from resume text
        
        Args:
            text: Resume text
            
        Returns:
            Dictionary with contact information
        """
        contact_info = {
            'email': extract_email(text),
            'phone': extract_phone(text)
        }
        
        return contact_info
    
    def extract_sections(self, text: str) -> Dict[str, str]:
        """
        Extract different sections from resume
        
        Args:
            text: Resume text
            
        Returns:
            Dictionary with different resume sections
        """
        sections = {
            'experience': '',
            'education': '',
            'skills': '',
            'summary': ''
        }
        
        # Convert to lowercase for pattern matching
        text_lower = text.lower()
        
        # Define section patterns
        section_patterns = {
            'experience': [
                r'(work experience|professional experience|experience|employment history)(.*?)(?=education|skills|projects|certifications|$)',
                r'(professional background|career history)(.*?)(?=education|skills|projects|$)'
            ],
            'education': [
                r'(education|academic background|qualifications)(.*?)(?=experience|skills|projects|certifications|$)'
            ],
            'skills': [
                r'(skills|technical skills|core competencies|expertise)(.*?)(?=experience|education|projects|certifications|$)'
            ],
            'summary': [
                r'(summary|objective|profile|about)(.*?)(?=experience|education|skills|$)'
            ]
        }
        
        for section, patterns in section_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text_lower, re.DOTALL | re.IGNORECASE)
                if match:
                    sections[section] = match.group(2).strip()
                    break
        
        return sections
    
    def preprocess_resume(self, text: str) -> Dict[str, any]:
        """
        Comprehensive preprocessing of resume text
        
        Args:
            text: Raw resume text
            
        Returns:
            Dictionary with processed resume information
        """
        if not text:
            return {
                'raw_text': '',
                'cleaned_text': '',
                'contact_info': {},
                'sections': {},
                'extracted_skills': [],
                'word_count': 0
            }
        
        # Clean the text
        cleaned_text = clean_text(text)
        
        # Extract contact information
        contact_info = self.extract_contact_info(text)
        
        # Extract sections
        sections = self.extract_sections(text)
        
        # Extract skills
        extracted_skills = extract_skills_from_text(cleaned_text, self.nlp)
        
        # Calculate word count
        word_count = len(cleaned_text.split())
        
        return {
            'raw_text': text,
            'cleaned_text': cleaned_text,
            'contact_info': contact_info,
            'sections': sections,
            'extracted_skills': extracted_skills,
            'word_count': word_count
        }
    
    def parse_resume(self, pdf_path: str) -> Dict[str, any]:
        """
        Main method to parse a resume PDF file
        
        Args:
            pdf_path: Path to the PDF resume file
            
        Returns:
            Dictionary with all extracted and processed resume information
        """
        # Extract text from PDF
        raw_text = self.extract_text_from_pdf(pdf_path)
        
        if not raw_text:
            return {
                'success': False,
                'error': 'Could not extract text from PDF',
                'data': None
            }
        
        # Preprocess the extracted text
        processed_data = self.preprocess_resume(raw_text)
        
        return {
            'success': True,
            'error': None,
            'data': processed_data
        }
    
    def validate_resume(self, processed_data: Dict[str, any]) -> Dict[str, any]:
        """
        Validate resume completeness and quality
        
        Args:
            processed_data: Processed resume data
            
        Returns:
            Validation results
        """
        validation = {
            'has_contact_info': False,
            'has_experience': False,
            'has_education': False,
            'has_skills': False,
            'word_count_adequate': False,
            'overall_score': 0,
            'missing_sections': []
        }
        
        if not processed_data:
            return validation
        
        # Check contact info
        contact = processed_data.get('contact_info', {})
        if contact.get('email') or contact.get('phone'):
            validation['has_contact_info'] = True
        else:
            validation['missing_sections'].append('Contact Information')
        
        # Check sections
        sections = processed_data.get('sections', {})
        
        if sections.get('experience') and len(sections['experience']) > 50:
            validation['has_experience'] = True
        else:
            validation['missing_sections'].append('Work Experience')
        
        if sections.get('education') and len(sections['education']) > 20:
            validation['has_education'] = True
        else:
            validation['missing_sections'].append('Education')
        
        if processed_data.get('extracted_skills') and len(processed_data['extracted_skills']) > 2:
            validation['has_skills'] = True
        else:
            validation['missing_sections'].append('Technical Skills')
        
        # Check word count
        word_count = processed_data.get('word_count', 0)
        if word_count >= 200:
            validation['word_count_adequate'] = True
        
        # Calculate overall score
        score_components = [
            validation['has_contact_info'],
            validation['has_experience'],
            validation['has_education'],
            validation['has_skills'],
            validation['word_count_adequate']
        ]
        
        validation['overall_score'] = (sum(score_components) / len(score_components)) * 100
        
        return validation

# Example usage
if __name__ == "__main__":
    parser = ResumeParser()
    
    # Test with a sample PDF (you would need to provide a real PDF path)
    # result = parser.parse_resume("sample_resumes/sample_resume.pdf")
    # print(result)
