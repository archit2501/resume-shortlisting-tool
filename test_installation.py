#!/usr/bin/env python3
"""
Test script to verify the Resume Shortlisting Tool installation
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import fitz  # PyMuPDF
        print("✓ PyMuPDF imported successfully")
    except ImportError:
        print("✗ PyMuPDF import failed - install with: pip install PyMuPDF")
        return False
    
    try:
        import spacy
        print("✓ spaCy imported successfully")
    except ImportError:
        print("✗ spaCy import failed - install with: pip install spacy")
        return False
    
    try:
        import sklearn
        print("✓ scikit-learn imported successfully")
    except ImportError:
        print("✗ scikit-learn import failed - install with: pip install scikit-learn")
        return False
    
    try:
        import matplotlib
        print("✓ matplotlib imported successfully")
    except ImportError:
        print("✗ matplotlib import failed - install with: pip install matplotlib")
        return False
    
    try:
        import flask
        print("✓ Flask imported successfully")
    except ImportError:
        print("✗ Flask import failed - install with: pip install flask")
        return False
    
    return True

def test_spacy_model():
    """Test if spaCy English model is available"""
    print("\nTesting spaCy model...")
    
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        print("✓ spaCy English model loaded successfully")
        return True
    except OSError:
        print("✗ spaCy English model not found")
        print("  Install with: python -m spacy download en_core_web_sm")
        return False

def test_modules():
    """Test if custom modules can be imported"""
    print("\nTesting custom modules...")
    
    try:
        from utils import clean_text, get_technical_skills
        print("✓ utils module imported successfully")
    except ImportError as e:
        print(f"✗ utils module import failed: {e}")
        return False
    
    try:
        from resume_parser import ResumeParser
        print("✓ resume_parser module imported successfully")
    except ImportError as e:
        print(f"✗ resume_parser module import failed: {e}")
        return False
    
    try:
        from jd_parser import JobDescriptionParser
        print("✓ jd_parser module imported successfully")
    except ImportError as e:
        print(f"✗ jd_parser module import failed: {e}")
        return False
    
    try:
        from match_engine import ResumeJobMatcher
        print("✓ match_engine module imported successfully")
    except ImportError as e:
        print(f"✗ match_engine module import failed: {e}")
        return False
    
    return True

def test_functionality():
    """Test basic functionality"""
    print("\nTesting basic functionality...")
    
    try:
        from utils import clean_text, get_technical_skills
        
        # Test text cleaning
        test_text = "  Hello World!  Python, JavaScript  "
        cleaned = clean_text(test_text)
        print(f"✓ Text cleaning works: '{test_text}' -> '{cleaned}'")
        
        # Test skill extraction
        skills = get_technical_skills()
        print(f"✓ Technical skills database loaded: {len(skills)} skills")
        
        return True
    except Exception as e:
        print(f"✗ Functionality test failed: {e}")
        return False

def test_job_description_parsing():
    """Test job description parsing"""
    print("\nTesting job description parsing...")
    
    try:
        from jd_parser import JobDescriptionParser
        
        parser = JobDescriptionParser()
        
        sample_jd = """
        Senior Python Developer
        
        Requirements:
        - 3+ years Python experience
        - Django or Flask
        - SQL databases
        
        Preferred:
        - AWS experience
        - Docker knowledge
        """
        
        result = parser.parse_job_description(sample_jd)
        
        if result['success']:
            print("✓ Job description parsing works")
            data = result['data']
            print(f"  Extracted {len(data['extracted_skills'])} skills")
            return True
        else:
            print(f"✗ Job description parsing failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"✗ Job description parsing test failed: {e}")
        return False

def test_file_structure():
    """Test if required files and directories exist"""
    print("\nTesting file structure...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'README.md',
        'utils.py',
        'resume_parser.py',
        'jd_parser.py',
        'match_engine.py',
        'cli.py'
    ]
    
    required_dirs = [
        'templates',
        'static',
        'sample_resumes',
        'sample_jds',
        'uploads'
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✓ {file} exists")
    
    for dir in required_dirs:
        if not os.path.exists(dir):
            missing_dirs.append(dir)
        else:
            print(f"✓ {dir}/ directory exists")
    
    if missing_files:
        print(f"✗ Missing files: {', '.join(missing_files)}")
        return False
    
    if missing_dirs:
        print(f"✗ Missing directories: {', '.join(missing_dirs)}")
        return False
    
    return True

def main():
    """Main test function"""
    print("=" * 60)
    print("RESUME SHORTLISTING TOOL - INSTALLATION TEST")
    print("=" * 60)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Package Imports", test_imports),
        ("spaCy Model", test_spacy_model),
        ("Custom Modules", test_modules),
        ("Basic Functionality", test_functionality),
        ("Job Description Parsing", test_job_description_parsing)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 40)
        
        if test_func():
            passed += 1
            print(f"✓ {test_name} PASSED")
        else:
            print(f"✗ {test_name} FAILED")
    
    print("\n" + "=" * 60)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! The tool is ready to use.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Download spaCy model: python -m spacy download en_core_web_sm")
        print("3. Run the web app: python app.py")
        print("4. Open http://localhost:5000 in your browser")
    else:
        print("✗ Some tests failed. Please check the installation.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
