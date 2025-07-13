// JavaScript for Batch Analysis

document.addEventListener('DOMContentLoaded', function() {
    const batchForm = document.getElementById('batchAnalysisForm');
    batchForm.addEventListener('submit', handleBatchSubmission);
});

let batchResults = []; // Store results for export

async function handleBatchSubmission(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    
    // Validate inputs
    if (!validateBatchInputs(formData)) {
        return;
    }
    
    // Show loading state
    showBatchLoading();
    
    try {
        const response = await fetch('/batch_upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            batchResults = result.data.results;
            displayBatchResults(result.data);
        } else {
            displayBatchError(result.error);
        }
        
    } catch (error) {
        console.error('Error:', error);
        displayBatchError('Network error occurred. Please try again.');
    } finally {
        hideBatchLoading();
    }
}

function validateBatchInputs(formData) {
    const resumes = formData.getAll('resumes');
    const jobDescription = formData.get('job_description');
    
    if (!resumes || resumes.length === 0 || resumes[0].size === 0) {
        showAlert('Please select at least one resume file.', 'warning');
        return false;
    }
    
    if (!jobDescription || jobDescription.trim().length < 50) {
        showAlert('Please provide a detailed job description (at least 50 characters).', 'warning');
        return false;
    }
    
    // Check each file
    for (let i = 0; i < resumes.length; i++) {
        const resume = resumes[i];
        
        if (resume.size > 16 * 1024 * 1024) {
            showAlert(`File "${resume.name}" is too large. Maximum size is 16MB.`, 'danger');
            return false;
        }
        
        if (!resume.name.toLowerCase().endsWith('.pdf')) {
            showAlert(`File "${resume.name}" is not a PDF. Only PDF files are allowed.`, 'danger');
            return false;
        }
    }
    
    return true;
}

function showBatchLoading() {
    const analyzeBtn = document.getElementById('batchAnalyzeBtn');
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
    
    document.getElementById('batchLoadingIndicator').style.display = 'block';
    document.getElementById('batchResultsSection').style.display = 'none';
    document.getElementById('batchErrorSection').style.display = 'none';
}

function hideBatchLoading() {
    const analyzeBtn = document.getElementById('batchAnalyzeBtn');
    analyzeBtn.disabled = false;
    analyzeBtn.innerHTML = '<i class="fas fa-magic me-2"></i>Analyze All Resumes';
    
    document.getElementById('batchLoadingIndicator').style.display = 'none';
}

function displayBatchResults(data) {
    // Update summary
    document.getElementById('batchSummary').textContent = 
        `Analyzed ${data.total_resumes} resumes, sorted by match score`;
    
    // Populate results table
    const tbody = document.getElementById('batchResultsBody');
    tbody.innerHTML = '';
    
    data.results.forEach((result, index) => {
        const row = createResultRow(result, index + 1);
        tbody.appendChild(row);
    });
    
    // Show results section
    const resultsSection = document.getElementById('batchResultsSection');
    resultsSection.style.display = 'block';
    resultsSection.classList.add('fade-in');
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function createResultRow(result, rank) {
    const row = document.createElement('tr');
    const matchScore = Math.round(result.match_score);
    
    // Add row class based on score
    if (matchScore >= 85) row.classList.add('table-success');
    else if (matchScore >= 70) row.classList.add('table-info');
    else if (matchScore >= 50) row.classList.add('table-warning');
    else row.classList.add('table-danger');
    
    row.innerHTML = `
        <td>
            <span class="badge bg-primary">${rank}</span>
        </td>
        <td>
            <strong>${result.filename}</strong>
        </td>
        <td>
            <div class="d-flex align-items-center">
                <div class="progress me-2" style="width: 60px; height: 20px;">
                    <div class="progress-bar ${getProgressBarClass(matchScore)}" 
                         style="width: ${matchScore}%"></div>
                </div>
                <strong class="${getScoreColorClass(matchScore)}">${matchScore}%</strong>
            </div>
        </td>
        <td>
            ${formatContactInfo(result.contact_info)}
        </td>
        <td>
            <div class="skills-preview">
                ${formatSkillsPreview(result.common_skills, 'matched')}
            </div>
        </td>
        <td>
            <div class="skills-preview">
                ${formatSkillsPreview(result.missing_skills, 'missing')}
            </div>
        </td>
        <td>
            <button class="btn btn-outline-primary btn-sm me-1" 
                    onclick="showDetailedView('${result.filename}', ${JSON.stringify(result).replace(/"/g, '&quot;')})">
                <i class="fas fa-eye"></i>
            </button>
            <button class="btn btn-outline-success btn-sm" 
                    onclick="downloadResult('${result.filename}', ${JSON.stringify(result).replace(/"/g, '&quot;')})">
                <i class="fas fa-download"></i>
            </button>
        </td>
    `;
    
    return row;
}

function formatContactInfo(contactInfo) {
    if (!contactInfo) return '<span class="text-muted">Not available</span>';
    
    let html = '';
    if (contactInfo.email) {
        html += `<div><i class="fas fa-envelope me-1"></i>${contactInfo.email}</div>`;
    }
    if (contactInfo.phone) {
        html += `<div><i class="fas fa-phone me-1"></i>${contactInfo.phone}</div>`;
    }
    
    return html || '<span class="text-muted">Not available</span>';
}

function formatSkillsPreview(skills, type) {
    if (!skills || skills.length === 0) {
        return '<span class="text-muted">None</span>';
    }
    
    const displaySkills = skills.slice(0, 3);
    const remaining = skills.length - 3;
    
    let html = displaySkills.map(skill => 
        `<span class="skill-tag ${type}">${capitalizeWords(skill)}</span>`
    ).join('');
    
    if (remaining > 0) {
        html += `<span class="text-muted">+${remaining} more</span>`;
    }
    
    return html;
}

function showDetailedView(filename, result) {
    const modal = new bootstrap.Modal(document.getElementById('detailModal'));
    
    document.getElementById('detailModalTitle').textContent = `Detailed Analysis: ${filename}`;
    
    const modalBody = document.getElementById('detailModalBody');
    modalBody.innerHTML = `
        <div class="row mb-3">
            <div class="col-md-6">
                <h5>Match Score</h5>
                <div class="text-center">
                    <div class="display-4 ${getScoreColorClass(Math.round(result.match_score))}">${Math.round(result.match_score)}%</div>
                </div>
            </div>
            <div class="col-md-6">
                <h5>Contact Information</h5>
                ${formatContactInfo(result.contact_info)}
            </div>
        </div>
        
        <div class="row">
            <div class="col-md-6">
                <h5>Matched Skills (${result.common_skills.length})</h5>
                <div class="mb-3">
                    ${result.common_skills.map(skill => 
                        `<span class="skill-tag matched">${capitalizeWords(skill)}</span>`
                    ).join('')}
                </div>
            </div>
            <div class="col-md-6">
                <h5>Missing Skills (${result.missing_skills.length})</h5>
                <div class="mb-3">
                    ${result.missing_skills.map(skill => 
                        `<span class="skill-tag missing">${capitalizeWords(skill)}</span>`
                    ).join('')}
                </div>
            </div>
        </div>
        
        <div class="mt-3">
            <h5>Suggestions</h5>
            <div class="alert alert-info">
                ${result.suggestions}
            </div>
        </div>
    `;
    
    modal.show();
}

function downloadResult(filename, result) {
    const data = {
        filename: filename,
        match_score: result.match_score,
        contact_info: result.contact_info,
        matched_skills: result.common_skills,
        missing_skills: result.missing_skills,
        suggestions: result.suggestions,
        timestamp: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${filename.replace('.pdf', '')}_analysis.json`;
    a.click();
    URL.revokeObjectURL(url);
}

function exportResults(format) {
    if (!batchResults || batchResults.length === 0) {
        showAlert('No results to export.', 'warning');
        return;
    }
    
    if (format === 'csv') {
        exportAsCSV();
    } else if (format === 'json') {
        exportAsJSON();
    }
}

function exportAsCSV() {
    const headers = ['Rank', 'Filename', 'Match Score', 'Email', 'Phone', 'Matched Skills', 'Missing Skills', 'Suggestions'];
    
    const csvData = batchResults.map((result, index) => [
        index + 1,
        result.filename,
        Math.round(result.match_score),
        result.contact_info?.email || '',
        result.contact_info?.phone || '',
        result.common_skills.join('; '),
        result.missing_skills.join('; '),
        result.suggestions
    ]);
    
    const csvContent = [headers, ...csvData]
        .map(row => row.map(field => `"${field}"`).join(','))
        .join('\n');
    
    downloadFile(csvContent, 'batch_analysis_results.csv', 'text/csv');
}

function exportAsJSON() {
    const exportData = {
        analysis_date: new Date().toISOString(),
        total_resumes: batchResults.length,
        results: batchResults
    };
    
    const jsonContent = JSON.stringify(exportData, null, 2);
    downloadFile(jsonContent, 'batch_analysis_results.json', 'application/json');
}

function downloadFile(content, filename, contentType) {
    const blob = new Blob([content], { type: contentType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
    
    showAlert(`Successfully exported ${filename}`, 'success');
}

function displayBatchError(errorMessage) {
    document.getElementById('batchErrorMessage').textContent = errorMessage;
    document.getElementById('batchErrorSection').style.display = 'block';
    document.getElementById('batchResultsSection').style.display = 'none';
    
    // Scroll to error
    document.getElementById('batchErrorSection').scrollIntoView({ behavior: 'smooth' });
}

// Utility functions (shared with main script)
function getScoreColorClass(score) {
    if (score >= 85) return 'score-excellent';
    if (score >= 70) return 'score-good';
    if (score >= 50) return 'score-fair';
    return 'score-poor';
}

function getProgressBarClass(score) {
    if (score >= 85) return 'bg-success';
    if (score >= 70) return 'bg-info';
    if (score >= 50) return 'bg-warning';
    return 'bg-danger';
}

function capitalizeWords(str) {
    return str.split(' ').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
    ).join(' ');
}

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}
