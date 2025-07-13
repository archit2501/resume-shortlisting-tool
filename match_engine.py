"""
Match Engine Module
Core engine for computing similarity between resumes and job descriptions
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

from resume_parser import ResumeParser
from jd_parser import JobDescriptionParser
from utils import calculate_match_percentage, get_improvement_suggestions, format_skills_list

class ResumeJobMatcher:
    def __init__(self):
        """Initialize the matcher with parsers and vectorizer"""
        self.resume_parser = ResumeParser()
        self.jd_parser = JobDescriptionParser()
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),
            lowercase=True
        )
    
    def compute_similarity(self, resume_text: str, jd_text: str) -> float:
        """
        Compute cosine similarity between resume and job description
        
        Args:
            resume_text: Cleaned resume text
            jd_text: Cleaned job description text
            
        Returns:
            Cosine similarity score (0-1)
        """
        try:
            # Combine texts for fitting the vectorizer
            documents = [resume_text, jd_text]
            
            # Create TF-IDF vectors
            tfidf_matrix = self.vectorizer.fit_transform(documents)
            
            # Compute cosine similarity
            similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            
            return similarity_matrix[0][0]
            
        except Exception as e:
            print(f"Error computing similarity: {str(e)}")
            return 0.0
    
    def analyze_skill_overlap(self, resume_skills: List[str], jd_skills: List[str]) -> Dict[str, List[str]]:
        """
        Analyze skill overlap between resume and job description
        
        Args:
            resume_skills: Skills extracted from resume
            jd_skills: Skills extracted from job description
            
        Returns:
            Dictionary with common and missing skills
        """
        # Convert to sets for easier comparison
        resume_set = set([skill.lower() for skill in resume_skills])
        jd_set = set([skill.lower() for skill in jd_skills])
        
        # Find common skills
        common_skills = list(resume_set.intersection(jd_set))
        
        # Find missing skills (in JD but not in resume)
        missing_skills = list(jd_set - resume_set)
        
        # Find extra skills (in resume but not in JD)
        extra_skills = list(resume_set - jd_set)
        
        return {
            'common_skills': common_skills,
            'missing_skills': missing_skills,
            'extra_skills': extra_skills
        }
    
    def calculate_weighted_score(self, similarity_score: float, skill_match_ratio: float, 
                               experience_match: bool = True) -> float:
        """
        Calculate a weighted match score considering multiple factors
        
        Args:
            similarity_score: Text similarity score
            skill_match_ratio: Ratio of matched skills
            experience_match: Whether experience requirements are met
            
        Returns:
            Weighted match score (0-1)
        """
        # Weights for different components
        text_weight = 0.4
        skill_weight = 0.4
        experience_weight = 0.2
        
        # Calculate weighted score
        weighted_score = (
            similarity_score * text_weight +
            skill_match_ratio * skill_weight +
            (1.0 if experience_match else 0.5) * experience_weight
        )
        
        return min(1.0, weighted_score)
    
    def generate_match_report(self, resume_data: Dict, jd_data: Dict, 
                            similarity_score: float, skill_analysis: Dict) -> Dict[str, any]:
        """
        Generate a comprehensive match report
        
        Args:
            resume_data: Processed resume data
            jd_data: Processed job description data
            similarity_score: Similarity score
            skill_analysis: Skill overlap analysis
            
        Returns:
            Comprehensive match report
        """
        # Calculate skill match ratio
        total_jd_skills = len(jd_data['extracted_skills'])
        matched_skills = len(skill_analysis['common_skills'])
        skill_match_ratio = matched_skills / total_jd_skills if total_jd_skills > 0 else 0
        
        # Calculate weighted score
        weighted_score = self.calculate_weighted_score(similarity_score, skill_match_ratio)
        
        # Convert to percentage
        match_percentage = calculate_match_percentage(weighted_score)
        
        # Generate suggestions
        suggestions = get_improvement_suggestions(
            skill_analysis['missing_skills'], 
            match_percentage
        )
        
        # Create detailed report
        report = {
            'match_score': match_percentage,
            'similarity_score': similarity_score,
            'skill_match_ratio': skill_match_ratio,
            'skills_analysis': {
                'total_resume_skills': len(resume_data['extracted_skills']),
                'total_jd_skills': len(jd_data['extracted_skills']),
                'matched_skills': matched_skills,
                'common_skills': skill_analysis['common_skills'][:10],  # Top 10
                'missing_skills': skill_analysis['missing_skills'][:10],  # Top 10
                'extra_skills': skill_analysis['extra_skills'][:5]  # Top 5
            },
            'contact_info': resume_data.get('contact_info', {}),
            'suggestions': suggestions,
            'resume_quality': self.resume_parser.validate_resume(resume_data),
            'jd_requirements': jd_data.get('requirements', {}),
            'formatted_output': self._format_output(match_percentage, skill_analysis, suggestions)
        }
        
        return report
    
    def _format_output(self, match_percentage: float, skill_analysis: Dict, suggestions: str) -> str:
        """Format the output for display"""
        output = f"""
=== RESUME-JOB MATCH ANALYSIS ===

Match Score: {match_percentage:.1f}%

Common Skills: {format_skills_list(skill_analysis['common_skills'])}

Missing Skills: {format_skills_list(skill_analysis['missing_skills'])}

Suggestions: {suggestions}

{'='*50}
        """
        return output.strip()
    
    def create_match_visualization(self, match_score: float, skill_analysis: Dict) -> str:
        """
        Create a visualization of the match results
        
        Args:
            match_score: Match percentage
            skill_analysis: Skill analysis results
            
        Returns:
            Base64 encoded plot image
        """
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
            
            # 1. Match Score Gauge
            ax1.pie([match_score, 100-match_score], 
                   startangle=90, counterclock=False,
                   colors=['#2E8B57', '#F5F5F5'],
                   wedgeprops=dict(width=0.3))
            ax1.text(0, 0, f'{match_score:.1f}%', ha='center', va='center', 
                    fontsize=16, fontweight='bold')
            ax1.set_title('Overall Match Score', fontweight='bold')
            
            # 2. Skills Breakdown
            skills_data = [
                len(skill_analysis['common_skills']),
                len(skill_analysis['missing_skills']),
                len(skill_analysis['extra_skills'])
            ]
            skills_labels = ['Matched', 'Missing', 'Extra']
            colors = ['#2E8B57', '#DC143C', '#4682B4']
            
            ax2.pie(skills_data, labels=skills_labels, autopct='%1.1f%%', 
                   colors=colors, startangle=90)
            ax2.set_title('Skills Distribution', fontweight='bold')
            
            # 3. Top Missing Skills
            missing_skills = skill_analysis['missing_skills'][:5]
            if missing_skills:
                y_pos = range(len(missing_skills))
                ax3.barh(y_pos, [1]*len(missing_skills), color='#DC143C', alpha=0.7)
                ax3.set_yticks(y_pos)
                ax3.set_yticklabels([skill.title() for skill in missing_skills])
                ax3.set_xlabel('Priority')
                ax3.set_title('Top Missing Skills', fontweight='bold')
            else:
                ax3.text(0.5, 0.5, 'No Missing Skills!', ha='center', va='center',
                        transform=ax3.transAxes, fontsize=14)
                ax3.set_title('Missing Skills', fontweight='bold')
            
            # 4. Top Matched Skills
            common_skills = skill_analysis['common_skills'][:5]
            if common_skills:
                y_pos = range(len(common_skills))
                ax4.barh(y_pos, [1]*len(common_skills), color='#2E8B57', alpha=0.7)
                ax4.set_yticks(y_pos)
                ax4.set_yticklabels([skill.title() for skill in common_skills])
                ax4.set_xlabel('Match')
                ax4.set_title('Top Matched Skills', fontweight='bold')
            else:
                ax4.text(0.5, 0.5, 'No Matched Skills', ha='center', va='center',
                        transform=ax4.transAxes, fontsize=14)
                ax4.set_title('Matched Skills', fontweight='bold')
            
            plt.tight_layout()
            
            # Convert to base64 string
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
            plt.close()
            
            return img_base64
            
        except Exception as e:
            print(f"Error creating visualization: {str(e)}")
            return ""
    
    def analyze_match(self, resume_path: str, jd_text: str) -> Dict[str, any]:
        """
        Main method to analyze match between resume and job description
        
        Args:
            resume_path: Path to resume PDF file
            jd_text: Job description text
            
        Returns:
            Complete match analysis
        """
        try:
            # Parse resume
            resume_result = self.resume_parser.parse_resume(resume_path)
            if not resume_result['success']:
                return {
                    'success': False,
                    'error': resume_result['error'],
                    'data': None
                }
            
            # Parse job description
            jd_result = self.jd_parser.parse_job_description(jd_text)
            if not jd_result['success']:
                return {
                    'success': False,
                    'error': jd_result['error'],
                    'data': None
                }
            
            resume_data = resume_result['data']
            jd_data = jd_result['data']
            
            # Compute similarity
            similarity_score = self.compute_similarity(
                resume_data['cleaned_text'],
                jd_data['cleaned_text']
            )
            
            # Analyze skill overlap
            skill_analysis = self.analyze_skill_overlap(
                resume_data['extracted_skills'],
                jd_data['extracted_skills']
            )
            
            # Generate comprehensive report
            match_report = self.generate_match_report(
                resume_data, jd_data, similarity_score, skill_analysis
            )
            
            # Create visualization
            visualization = self.create_match_visualization(
                match_report['match_score'], skill_analysis
            )
            
            match_report['visualization'] = visualization
            
            return {
                'success': True,
                'error': None,
                'data': match_report
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Error analyzing match: {str(e)}",
                'data': None
            }
    
    def batch_analyze(self, resume_paths: List[str], jd_text: str) -> List[Dict[str, any]]:
        """
        Analyze multiple resumes against a single job description
        
        Args:
            resume_paths: List of resume PDF file paths
            jd_text: Job description text
            
        Returns:
            List of match analyses sorted by match score
        """
        results = []
        
        for resume_path in resume_paths:
            result = self.analyze_match(resume_path, jd_text)
            if result['success']:
                result['resume_path'] = resume_path
                results.append(result)
        
        # Sort by match score (descending)
        results.sort(key=lambda x: x['data']['match_score'], reverse=True)
        
        return results

# Example usage
if __name__ == "__main__":
    matcher = ResumeJobMatcher()
    
    # Sample job description
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
    
    # This would analyze a real resume file
    # result = matcher.analyze_match("sample_resumes/resume.pdf", sample_jd)
    # print(result['data']['formatted_output'] if result['success'] else result['error'])
