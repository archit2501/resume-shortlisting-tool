#!/usr/bin/env python3
"""
Command Line Interface for Resume Shortlisting Tool
Usage: python cli.py <resume_path> <job_description_file>
"""

import sys
import os
from match_engine import ResumeJobMatcher

def main():
    if len(sys.argv) != 3:
        print("Usage: python cli.py <resume_path> <job_description_file>")
        print("\nExample:")
        print("python cli.py sample_resumes/resume.pdf sample_jds/senior_python_developer.txt")
        sys.exit(1)
    
    resume_path = sys.argv[1]
    jd_file_path = sys.argv[2]
    
    # Check if files exist
    if not os.path.exists(resume_path):
        print(f"Error: Resume file '{resume_path}' not found.")
        sys.exit(1)
    
    if not os.path.exists(jd_file_path):
        print(f"Error: Job description file '{jd_file_path}' not found.")
        sys.exit(1)
    
    # Read job description
    try:
        with open(jd_file_path, 'r', encoding='utf-8') as f:
            job_description = f.read()
    except Exception as e:
        print(f"Error reading job description file: {e}")
        sys.exit(1)
    
    # Initialize matcher
    print("Initializing Resume Shortlisting Tool...")
    matcher = ResumeJobMatcher()
    
    # Analyze match
    print(f"\nAnalyzing resume: {resume_path}")
    print(f"Against job description: {jd_file_path}")
    print("-" * 50)
    
    result = matcher.analyze_match(resume_path, job_description)
    
    if result['success']:
        data = result['data']
        print(data['formatted_output'])
        
        # Additional details
        print("\n=== DETAILED ANALYSIS ===")
        print(f"Text Similarity Score: {data['similarity_score']:.3f}")
        print(f"Skills Match Ratio: {data['skill_match_ratio']:.3f}")
        
        skills_analysis = data['skills_analysis']
        print(f"\nResume Skills Found: {skills_analysis['total_resume_skills']}")
        print(f"Job Requirements: {skills_analysis['total_jd_skills']}")
        print(f"Skills Matched: {skills_analysis['matched_skills']}")
        
        if data['contact_info'].get('email') or data['contact_info'].get('phone'):
            print(f"\n=== CONTACT INFORMATION ===")
            if data['contact_info'].get('email'):
                print(f"Email: {data['contact_info']['email']}")
            if data['contact_info'].get('phone'):
                print(f"Phone: {data['contact_info']['phone']}")
        
        # Resume quality check
        quality = data['resume_quality']
        print(f"\n=== RESUME QUALITY ASSESSMENT ===")
        print(f"Overall Quality Score: {quality['overall_score']:.1f}%")
        if quality['missing_sections']:
            print(f"Missing Sections: {', '.join(quality['missing_sections'])}")
        
    else:
        print(f"Error: {result['error']}")
        sys.exit(1)

if __name__ == "__main__":
    main()
