// JavaScript for Resume Shortlisting Tool - Single Analysis

document.addEventListener('DOMContentLoaded', function() {
    const analysisForm = document.getElementById('analysisForm');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const resultsSection = document.getElementById('resultsSection');
    const errorSection = document.getElementById('errorSection');
    const analyzeBtn = document.getElementById('analyzeBtn');

    analysisForm.addEventListener('submit', handleFormSubmission);
});

async function handleFormSubmission(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    
    // Validate inputs
    if (!validateInputs(formData)) {
        return;
    }
    
    // Show loading state
    showLoading();
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayResults(result.data);
        } else {
            displayError(result.error);
        }
        
    } catch (error) {
        console.error('Error:', error);
        displayError('Network error occurred. Please try again.');
    } finally {
        hideLoading();
    }
}

function validateInputs(formData) {
    const resume = formData.get('resume');
    const jobDescription = formData.get('job_description');
    
    if (!resume || resume.size === 0) {
        showAlert('Please select a resume file.', 'warning');
        return false;
    }
    
    if (!jobDescription || jobDescription.trim().length < 50) {
        showAlert('Please provide a detailed job description (at least 50 characters).', 'warning');
        return false;
    }
    
    // Check file size (16MB limit)
    if (resume.size > 16 * 1024 * 1024) {
        showAlert('File size too large. Maximum size is 16MB.', 'danger');
        return false;
    }
    
    // Check file type
    if (!resume.name.toLowerCase().endsWith('.pdf')) {
        showAlert('Only PDF files are allowed.', 'danger');
        return false;
    }
    
    return true;
}

function showLoading() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Analyzing...';
    
    document.getElementById('loadingIndicator').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
}

function hideLoading() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    analyzeBtn.disabled = false;
    analyzeBtn.innerHTML = '<i class="fas fa-magic me-2"></i>Analyze Match';
    
    document.getElementById('loadingIndicator').style.display = 'none';
}

function displayResults(data) {
    // Update match score
    const matchScore = Math.round(data.match_score);
    document.getElementById('matchScore').textContent = `${matchScore}%`;
    
    // Apply color coding to match score
    const scoreElement = document.getElementById('matchScore');
    scoreElement.className = 'display-1 fw-bold ' + getScoreColorClass(matchScore);
    
    // Display matched skills
    displaySkills('matchedSkills', data.skills_analysis.common_skills, 'matched');
    
    // Display missing skills
    displaySkills('missingSkills', data.skills_analysis.missing_skills, 'missing');
    
    // Display suggestions
    document.getElementById('suggestions').textContent = data.suggestions;
    
    // Display contact information if available
    displayContactInfo(data.contact_info);
    
    // Display visualization if available
    if (data.visualization) {
        displayVisualization(data.visualization);
    }
    
    // Show results section with animation
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.style.display = 'block';
    resultsSection.classList.add('fade-in');
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function displaySkills(containerId, skills, type) {
    const container = document.getElementById(containerId);
    
    if (!skills || skills.length === 0) {
        container.innerHTML = '<p class="text-muted mb-0">None identified</p>';
        return;
    }
    
    const skillsHtml = skills.slice(0, 10).map(skill => 
        `<span class="skill-tag ${type}">${capitalizeWords(skill)}</span>`
    ).join('');
    
    const remainingCount = skills.length - 10;
    const remainingText = remainingCount > 0 ? 
        `<p class="text-muted mt-2 mb-0">and ${remainingCount} more...</p>` : '';
    
    container.innerHTML = skillsHtml + remainingText;
}

function displayContactInfo(contactInfo) {
    const contactSection = document.getElementById('contactSection');
    const contactContainer = document.getElementById('contactInfo');
    
    if (!contactInfo || (!contactInfo.email && !contactInfo.phone)) {
        contactSection.style.display = 'none';
        return;
    }
    
    let contactHtml = '';
    
    if (contactInfo.email) {
        contactHtml += `
            <div class="contact-item">
                <i class="fas fa-envelope"></i>
                <span>${contactInfo.email}</span>
            </div>
        `;
    }
    
    if (contactInfo.phone) {
        contactHtml += `
            <div class="contact-item">
                <i class="fas fa-phone"></i>
                <span>${contactInfo.phone}</span>
            </div>
        `;
    }
    
    contactContainer.innerHTML = contactHtml;
    contactSection.style.display = 'block';
}

function displayVisualization(base64Image) {
    const container = document.getElementById('matchVisualization');
    if (base64Image) {
        container.innerHTML = `<img src="data:image/png;base64,${base64Image}" class="img-fluid border-rounded" alt="Match Visualization">`;
    }
}

function displayError(errorMessage) {
    document.getElementById('errorMessage').textContent = errorMessage;
    document.getElementById('errorSection').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';
    
    // Scroll to error
    document.getElementById('errorSection').scrollIntoView({ behavior: 'smooth' });
}

function getScoreColorClass(score) {
    if (score >= 85) return 'score-excellent';
    if (score >= 70) return 'score-good';
    if (score >= 50) return 'score-fair';
    return 'score-poor';
}

function capitalizeWords(str) {
    return str.split(' ').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
    ).join(' ');
}

function showAlert(message, type = 'info') {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at top of container
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Sample job description functionality
function showSampleJD() {
    const sampleJD = `Senior Python Developer

We are seeking an experienced Python developer to join our growing engineering team.

Requirements:
• 3+ years of Python development experience
• Strong experience with Django or Flask frameworks
• Proficiency in SQL databases (PostgreSQL, MySQL)
• Experience with RESTful API development
• Knowledge of Git version control
• Understanding of software development best practices
• Bachelor's degree in Computer Science or related field

Preferred Qualifications:
• Experience with AWS cloud services
• Knowledge of Docker and containerization
• Familiarity with React or Vue.js
• Experience with data analysis libraries (pandas, numpy)
• Understanding of machine learning concepts
• Agile/Scrum methodology experience

Responsibilities:
• Develop and maintain web applications using Python
• Design and implement RESTful APIs
• Collaborate with frontend developers and designers
• Write clean, maintainable, and well-documented code
• Participate in code reviews and technical discussions
• Troubleshoot and debug applications`;

    document.getElementById('sampleJDText').textContent = sampleJD;
    new bootstrap.Modal(document.getElementById('sampleJDModal')).show();
}

function useSampleJD() {
    const sampleJD = document.getElementById('sampleJDText').textContent;
    document.getElementById('jobDescription').value = sampleJD;
    bootstrap.Modal.getInstance(document.getElementById('sampleJDModal')).hide();
    showAlert('Sample job description loaded successfully!', 'success');
}

// Add sample JD button to the job description field
document.addEventListener('DOMContentLoaded', function() {
    const jdContainer = document.querySelector('label[for="jobDescription"]').parentNode;
    const sampleButton = document.createElement('button');
    sampleButton.type = 'button';
    sampleButton.className = 'btn btn-outline-secondary btn-sm mt-2';
    sampleButton.innerHTML = '<i class="fas fa-lightbulb me-1"></i>Load Sample JD';
    sampleButton.onclick = showSampleJD;
    
    jdContainer.appendChild(sampleButton);
});
