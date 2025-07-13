#!/usr/bin/env python3
"""
Setup script for Resume Shortlisting Tool
This script helps install dependencies and set up the environment
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n{description}...")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed")
        print(f"Error: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    
    version = sys.version_info
    if version.major == 3 and version.minor >= 7:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("This tool requires Python 3.7 or higher")
        return False

def install_requirements():
    """Install Python packages from requirements.txt"""
    if not os.path.exists('requirements.txt'):
        print("✗ requirements.txt not found")
        return False
    
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python packages"
    )

def download_spacy_model():
    """Download spaCy English model"""
    return run_command(
        f"{sys.executable} -m spacy download en_core_web_sm",
        "Downloading spaCy English model"
    )

def create_directories():
    """Create necessary directories"""
    print("\nCreating necessary directories...")
    
    directories = ['uploads', 'sample_resumes', 'sample_jds']
    
    for directory in directories:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print(f"✓ Created directory: {directory}")
            except Exception as e:
                print(f"✗ Failed to create directory {directory}: {e}")
                return False
        else:
            print(f"✓ Directory already exists: {directory}")
    
    return True

def test_installation():
    """Run installation test"""
    print("\nTesting installation...")
    
    try:
        import test_installation
        return test_installation.main() == 0
    except ImportError:
        print("✗ test_installation.py not found")
        return False

def main():
    """Main setup function"""
    print("=" * 60)
    print("RESUME SHORTLISTING TOOL - SETUP SCRIPT")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Create directories
    if not create_directories():
        print("✗ Failed to create directories")
        return 1
    
    # Install requirements
    if not install_requirements():
        print("✗ Failed to install requirements")
        print("You may need to install packages manually:")
        print("pip install -r requirements.txt")
        return 1
    
    # Download spaCy model
    if not download_spacy_model():
        print("✗ Failed to download spaCy model")
        print("You may need to install it manually:")
        print("python -m spacy download en_core_web_sm")
        return 1
    
    # Test installation
    print("\n" + "=" * 60)
    print("RUNNING INSTALLATION TEST")
    print("=" * 60)
    
    if test_installation():
        print("\n" + "=" * 60)
        print("SETUP COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nThe Resume Shortlisting Tool is ready to use!")
        print("\nTo start the web application:")
        print("python app.py")
        print("\nTo use the command line interface:")
        print("python cli.py <resume.pdf> <job_description.txt>")
        print("\nTo run tests:")
        print("python test_installation.py")
        return 0
    else:
        print("\n" + "=" * 60)
        print("SETUP COMPLETED WITH ISSUES")
        print("=" * 60)
        print("Some components may not work correctly.")
        print("Please check the error messages above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
