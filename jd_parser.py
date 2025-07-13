"""
Job Description Parser Module
Handles job description text processing and analysis
"""

import re
from typing import Dict, List
from utils import clean_text, load_spacy_model, extract_skills_from_text

class JobDescriptionParser:
    def __init__(self):
        """Initialize the job description parser with spaCy model"""
        self.nlp = load_spacy_model()
    
    def extract_requirements(self, text: str) -> Dict[str, List[str]]:
        """
        Extract different types of requirements from job description
        
        Args:
            text: Job description text
            
        Returns:
            Dictionary with categorized requirements
        """
        text_lower = text.lower()
        
        requirements = {
            'required_skills': [],
            'preferred_skills': [],
            'experience_level': '',
            'education': [],
            'certifications': []
        }
        
        # Extract required vs preferred skills
        required_patterns = [
            r'required[:\s]+(.*?)(?=preferred|nice to have|plus|bonus|$)',
            r'must have[:\s]+(.*?)(?=preferred|nice to have|plus|bonus|$)',
            r'essential[:\s]+(.*?)(?=preferred|nice to have|plus|bonus|$)'
        ]
        
        preferred_patterns = [
            r'preferred[:\s]+(.*?)(?=required|must have|essential|$)',
            r'nice to have[:\s]+(.*?)(?=required|must have|essential|$)',
            r'plus[:\s]+(.*?)(?=required|must have|essential|$)',
            r'bonus[:\s]+(.*?)(?=required|must have|essential|$)'
        ]
        
        # Extract required skills
        for pattern in required_patterns:
            match = re.search(pattern, text_lower, re.DOTALL | re.IGNORECASE)
            if match:
                requirements['required_skills'].extend(
                    self._extract_skills_from_section(match.group(1))
                )
        
        # Extract preferred skills
        for pattern in preferred_patterns:
            match = re.search(pattern, text_lower, re.DOTALL | re.IGNORECASE)
            if match:
                requirements['preferred_skills'].extend(
                    self._extract_skills_from_section(match.group(1))
                )
        
        # Extract experience level
        experience_patterns = [
            r'(\d+)[+\-\s]*years?\s+(?:of\s+)?experience',
            r'(\d+)[+\-\s]*yrs?\s+(?:of\s+)?experience',
            r'(entry[\s\-]?level|junior|mid[\s\-]?level|senior|lead|principal)'
        ]
        
        for pattern in experience_patterns:
            match = re.search(pattern, text_lower)
            if match:
                requirements['experience_level'] = match.group(1)
                break
        
        # Extract education requirements
        education_patterns = [
            r'(bachelor|master|phd|doctorate|associate)[\s\']*(?:degree|\'s)?',
            r'(bs|ms|mba|ma|ba|bsc|msc)(?:\s+degree)?',
            r'degree\s+in\s+([^,\n]+)'
        ]
        
        for pattern in education_patterns:
            matches = re.findall(pattern, text_lower)
            requirements['education'].extend([match for match in matches if match])
        
        return requirements
    
    def _extract_skills_from_section(self, section_text: str) -> List[str]:
        """Extract skills from a specific section of text"""
        skills = extract_skills_from_text(section_text, self.nlp)
        
        # Also look for skills in bullet points and lists
        lines = section_text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                line_skills = extract_skills_from_text(line, self.nlp)
                skills.extend(line_skills)
        
        return list(set(skills))  # Remove duplicates
    
    def extract_job_info(self, text: str) -> Dict[str, str]:
        """
        Extract basic job information from job description
        
        Args:
            text: Job description text
            
        Returns:
            Dictionary with job information
        """
        job_info = {
            'title': '',
            'company': '',
            'location': '',
            'employment_type': ''
        }
        
        text_lines = text.split('\n')
        first_few_lines = ' '.join(text_lines[:5]).lower()
        
        # Extract job title (usually in the first line or two)
        title_patterns = [
            r'job title[:\s]+([^\n]+)',
            r'position[:\s]+([^\n]+)',
            r'role[:\s]+([^\n]+)'
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, first_few_lines)
            if match:
                job_info['title'] = match.group(1).strip()
                break
        
        # Extract employment type
        employment_patterns = [
            r'(full[\s\-]?time|part[\s\-]?time|contract|temporary|intern|remote)',
            r'(permanent|freelance|consultant)'
        ]
        
        for pattern in employment_patterns:
            match = re.search(pattern, text.lower())
            if match:
                job_info['employment_type'] = match.group(1)
                break
        
        return job_info
    
    def categorize_jd_sections(self, text: str) -> Dict[str, str]:
        """
        Categorize job description into different sections
        
        Args:
            text: Job description text
            
        Returns:
            Dictionary with different JD sections
        """
        sections = {
            'overview': '',
            'responsibilities': '',
            'requirements': '',
            'qualifications': '',
            'benefits': ''
        }
        
        text_lower = text.lower()
        
        section_patterns = {
            'overview': [
                r'(job summary|overview|about the role|description)(.*?)(?=responsibilities|requirements|qualifications|$)',
                r'(company overview|about us)(.*?)(?=responsibilities|requirements|qualifications|$)'
            ],
            'responsibilities': [
                r'(responsibilities|duties|what you\'ll do|role description)(.*?)(?=requirements|qualifications|benefits|$)'
            ],
            'requirements': [
                r'(requirements|qualifications|what we\'re looking for)(.*?)(?=benefits|compensation|$)',
                r'(required skills|must have)(.*?)(?=preferred|benefits|$)'
            ],
            'qualifications': [
                r'(preferred qualifications|nice to have|preferred skills)(.*?)(?=benefits|compensation|$)'
            ],
            'benefits': [
                r'(benefits|compensation|what we offer|perks)(.*?)$'
            ]
        }
        
        for section, patterns in section_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text_lower, re.DOTALL | re.IGNORECASE)
                if match:
                    sections[section] = match.group(2).strip()
                    break
        
        return sections
    
    def preprocess_job_description(self, text: str) -> Dict[str, any]:
        """
        Comprehensive preprocessing of job description text
        
        Args:
            text: Raw job description text
            
        Returns:
            Dictionary with processed job description information
        """
        if not text:
            return {
                'raw_text': '',
                'cleaned_text': '',
                'job_info': {},
                'sections': {},
                'requirements': {},
                'extracted_skills': [],
                'word_count': 0
            }
        
        # Clean the text
        cleaned_text = clean_text(text)
        
        # Extract job information
        job_info = self.extract_job_info(text)
        
        # Categorize sections
        sections = self.categorize_jd_sections(text)
        
        # Extract requirements
        requirements = self.extract_requirements(text)
        
        # Extract all skills mentioned
        extracted_skills = extract_skills_from_text(cleaned_text, self.nlp)
        
        # Calculate word count
        word_count = len(cleaned_text.split())
        
        return {
            'raw_text': text,
            'cleaned_text': cleaned_text,
            'job_info': job_info,
            'sections': sections,
            'requirements': requirements,
            'extracted_skills': extracted_skills,
            'word_count': word_count
        }
    
    def parse_job_description(self, text: str) -> Dict[str, any]:
        """
        Main method to parse job description text
        
        Args:
            text: Job description text
            
        Returns:
            Dictionary with all extracted and processed JD information
        """
        if not text or len(text.strip()) < 50:
            return {
                'success': False,
                'error': 'Job description text is too short or empty',
                'data': None
            }
        
        # Preprocess the job description
        processed_data = self.preprocess_job_description(text)
        
        return {
            'success': True,
            'error': None,
            'data': processed_data
        }
    
    def load_jd_from_file(self, file_path: str) -> str:
        """
        Load job description from a text file
        
        Args:
            file_path: Path to the text file
            
        Returns:
            Job description text
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading job description file: {str(e)}")
            return ""

# Example usage
if __name__ == "__main__":
    parser = JobDescriptionParser()
    
    # Test with sample job description
    sample_jd = """
    Senior Python Developer
    
    We are looking for an experienced Python developer to join our team.
    
    Requirements:
    - 3+ years of Python experience
    - Experience with Django or Flask
    - Knowledge of SQL databases
    - Git version control
    
    Preferred:
    - AWS experience
    - Docker knowledge
    - React experience
    """
    
    result = parser.parse_job_description(sample_jd)
    print(result)
