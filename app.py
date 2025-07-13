"""
Flask Web Application for Resume Shortlisting Tool
"""

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename
import traceback

from match_engine import ResumeJobMatcher
from resume_parser import ResumeParser
from jd_parser import JobDescriptionParser

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize components
matcher = ResumeJobMatcher()
resume_parser = ResumeParser()
jd_parser = JobDescriptionParser()

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and job description submission"""
    try:
        # Check if file is present
        if 'resume' not in request.files:
            return jsonify({'success': False, 'error': 'No resume file provided'})
        
        file = request.files['resume']
        job_description = request.form.get('job_description', '').strip()
        
        # Validate inputs
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        if not job_description:
            return jsonify({'success': False, 'error': 'Job description is required'})
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Only PDF files are allowed'})
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Analyze the match
        result = matcher.analyze_match(file_path, job_description)
        
        # Clean up uploaded file
        try:
            os.remove(file_path)
        except:
            pass
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': result['data']
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            })
            
    except Exception as e:
        # Clean up file if it exists
        try:
            if 'file_path' in locals():
                os.remove(file_path)
        except:
            pass
        
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        })

@app.route('/batch_analysis')
def batch_analysis():
    """Page for batch analysis of multiple resumes"""
    return render_template('batch_analysis.html')

@app.route('/batch_upload', methods=['POST'])
def batch_upload():
    """Handle batch upload of multiple resumes"""
    try:
        # Get job description
        job_description = request.form.get('job_description', '').strip()
        if not job_description:
            return jsonify({'success': False, 'error': 'Job description is required'})
        
        # Get uploaded files
        files = request.files.getlist('resumes')
        if not files or all(f.filename == '' for f in files):
            return jsonify({'success': False, 'error': 'No resume files provided'})
        
        results = []
        file_paths = []
        
        try:
            # Save and process each file
            for file in files:
                if file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    file_paths.append(file_path)
            
            # Analyze all resumes
            if file_paths:
                batch_results = matcher.batch_analyze(file_paths, job_description)
                
                # Format results for display
                for i, result in enumerate(batch_results):
                    if result['success']:
                        original_filename = os.path.basename(result['resume_path'])
                        results.append({
                            'filename': original_filename,
                            'match_score': result['data']['match_score'],
                            'common_skills': result['data']['skills_analysis']['common_skills'],
                            'missing_skills': result['data']['skills_analysis']['missing_skills'],
                            'suggestions': result['data']['suggestions'],
                            'contact_info': result['data']['contact_info']
                        })
            
            return jsonify({
                'success': True,
                'data': {
                    'total_resumes': len(results),
                    'results': results
                }
            })
            
        finally:
            # Clean up uploaded files
            for file_path in file_paths:
                try:
                    os.remove(file_path)
                except:
                    pass
                    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        })

@app.route('/api/parse_resume', methods=['POST'])
def api_parse_resume():
    """API endpoint to parse resume only"""
    try:
        if 'resume' not in request.files:
            return jsonify({'success': False, 'error': 'No resume file provided'})
        
        file = request.files['resume']
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Only PDF files are allowed'})
        
        # Save and parse file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            result = resume_parser.parse_resume(file_path)
            return jsonify(result)
        finally:
            os.remove(file_path)
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        })

@app.route('/api/parse_jd', methods=['POST'])
def api_parse_jd():
    """API endpoint to parse job description only"""
    try:
        jd_text = request.json.get('job_description', '').strip()
        if not jd_text:
            return jsonify({'success': False, 'error': 'Job description is required'})
        
        result = jd_parser.parse_job_description(jd_text)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        })

@app.route('/help')
def help_page():
    """Help and documentation page"""
    return render_template('help.html')

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum size is 16MB.'
    }), 413

@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error occurred.'
    }), 500

if __name__ == '__main__':
    print("Starting Resume Shortlisting Tool...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
