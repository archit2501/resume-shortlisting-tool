"""
Utility functions for the Resume Shortlisting Tool
"""

import re
import string
from typing import List, Set
import spacy

def load_spacy_model():
    """Load spaCy model with error handling"""
    try:
        nlp = spacy.load("en_core_web_sm")
        return nlp
    except OSError:
        print("Warning: spaCy model 'en_core_web_sm' not found.")
        print("Please install it using: python -m spacy download en_core_web_sm")
        return None

def clean_text(text: str) -> str:
    """
    Clean and normalize text for processing
    
    Args:
        text: Raw text to clean
        
    Returns:
        Cleaned text string
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep letters, numbers, and basic punctuation
    text = re.sub(r'[^\w\s\-\.]', ' ', text)
    
    # Remove multiple spaces
    text = ' '.join(text.split())
    
    return text.strip()

def extract_email(text: str) -> str:
    """Extract email address from text"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else ""

def extract_phone(text: str) -> str:
    """Extract phone number from text"""
    phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    phones = re.findall(phone_pattern, text)
    return phones[0] if phones else ""

def get_technical_skills() -> Set[str]:
    """
    Return a comprehensive set of technical skills and keywords
    """
    skills = {
        # Programming Languages
        'python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
        'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql', 'html', 'css', 'typescript',
        
        # Frameworks and Libraries
        'react', 'angular', 'vue', 'django', 'flask', 'spring', 'express', 'nodejs',
        'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'opencv', 'keras',
        'bootstrap', 'jquery', 'redux', 'webpack', 'babel',
        
        # Databases
        'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra',
        'oracle', 'sqlite', 'dynamodb', 'firebase',
        
        # Cloud and DevOps
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab', 'github',
        'terraform', 'ansible', 'chef', 'puppet', 'nagios', 'prometheus',
        
        # Data Science and Analytics
        'machine learning', 'deep learning', 'artificial intelligence', 'data analysis',
        'data visualization', 'big data', 'hadoop', 'spark', 'tableau', 'powerbi',
        'excel', 'statistics', 'predictive modeling', 'nlp', 'computer vision',
        
        # Web Technologies
        'rest', 'api', 'json', 'xml', 'graphql', 'microservices', 'soap', 'oauth',
        'jwt', 'cors', 'websocket',
        
        # Operating Systems and Tools
        'linux', 'windows', 'macos', 'unix', 'bash', 'powershell', 'git', 'svn',
        'vim', 'vscode', 'intellij', 'eclipse', 'postman', 'jira', 'confluence',
        
        # Methodologies
        'agile', 'scrum', 'kanban', 'devops', 'ci/cd', 'tdd', 'bdd', 'mvc', 'mvp',
        'design patterns', 'solid principles', 'clean code'
    }
    
    return skills

def extract_skills_from_text(text: str, nlp=None) -> List[str]:
    """
    Extract technical skills from text using keyword matching
    
    Args:
        text: Text to extract skills from
        nlp: spaCy model (optional)
        
    Returns:
        List of extracted skills
    """
    text = clean_text(text)
    technical_skills = get_technical_skills()
    found_skills = []
    
    # Check for exact matches and partial matches
    for skill in technical_skills:
        if skill in text:
            found_skills.append(skill)
    
    # If spaCy is available, also extract named entities
    if nlp:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT'] and ent.text.lower() not in found_skills:
                # Check if it's a potential tech skill
                if any(keyword in ent.text.lower() for keyword in ['tech', 'software', 'system', 'platform']):
                    found_skills.append(ent.text.lower())
    
    return list(set(found_skills))  # Remove duplicates

def calculate_match_percentage(similarity_score: float) -> float:
    """
    Convert cosine similarity to a percentage match score
    
    Args:
        similarity_score: Cosine similarity score (0-1)
        
    Returns:
        Match percentage (0-100)
    """
    # Scale similarity score to percentage and apply some weighting
    percentage = similarity_score * 100
    
    # Apply a curve to make the scoring more intuitive
    # Lower scores get slightly boosted, very high scores get slightly reduced
    if percentage < 30:
        percentage = percentage * 1.2
    elif percentage > 85:
        percentage = 85 + (percentage - 85) * 0.5
    
    return min(100, max(0, percentage))

def get_improvement_suggestions(missing_skills: List[str], match_score: float) -> str:
    """
    Generate improvement suggestions based on missing skills and match score
    
    Args:
        missing_skills: List of skills missing from resume
        match_score: Current match score percentage
        
    Returns:
        Suggestion string
    """
    suggestions = []
    
    if match_score < 50:
        suggestions.append("This role requires significant skill development.")
    elif match_score < 70:
        suggestions.append("Good foundation, but some key skills are missing.")
    elif match_score < 85:
        suggestions.append("Strong match! Adding a few more skills could make this perfect.")
    else:
        suggestions.append("Excellent match for this role!")
    
    if missing_skills:
        if len(missing_skills) <= 3:
            suggestions.append(f"Consider adding experience with: {', '.join(missing_skills[:3])}")
        else:
            suggestions.append(f"Focus on developing skills in: {', '.join(missing_skills[:3])} and {len(missing_skills)-3} others")
    
    return " ".join(suggestions)

def format_skills_list(skills: List[str]) -> str:
    """Format a list of skills for display"""
    if not skills:
        return "None identified"
    
    # Capitalize first letter of each skill
    formatted_skills = [skill.title() for skill in skills]
    
    if len(formatted_skills) <= 5:
        return ", ".join(formatted_skills)
    else:
        return ", ".join(formatted_skills[:5]) + f" and {len(formatted_skills)-5} more"
