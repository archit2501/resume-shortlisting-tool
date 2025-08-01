// AI Resume Tool Website JavaScript
document.addEventListener('DOMContentLoaded', function() {
    
    // Sample job descriptions
    const sampleJobs = {
        data_scientist: `We are seeking a skilled Data Scientist to join our team. The ideal candidate should have:

Key Requirements:
• Master's or PhD in Data Science, Statistics, Computer Science, or related field
• 3+ years of experience in data analysis and machine learning
• Proficiency in Python, R, SQL, and statistical modeling
• Experience with machine learning frameworks (scikit-learn, TensorFlow, PyTorch)
• Strong knowledge of data visualization tools (Matplotlib, Seaborn, Plotly)
• Experience with big data technologies (Spark, Hadoop)
• Knowledge of cloud platforms (AWS, GCP, Azure)
• Strong communication and problem-solving skills

Responsibilities:
• Develop and implement machine learning models
• Analyze large datasets to extract actionable insights
• Create data visualizations and reports
• Collaborate with cross-functional teams
• Deploy models to production environments`,

        frontend_developer: `We are looking for a talented Frontend Developer to create amazing user experiences. Requirements:

Key Requirements:
• Bachelor's degree in Computer Science or related field
• 2+ years of frontend development experience
• Proficiency in HTML5, CSS3, JavaScript (ES6+)
• Experience with modern frameworks (React, Vue.js, Angular)
• Knowledge of responsive design and mobile-first development
• Familiarity with CSS preprocessors (Sass, Less)
• Experience with version control (Git)
• Understanding of web performance optimization
• Knowledge of testing frameworks (Jest, Cypress)

Responsibilities:
• Develop responsive web applications
• Implement user interface designs
• Optimize applications for maximum speed
• Collaborate with backend developers and designers
• Ensure cross-browser compatibility`,

        python_developer: `Join our team as a Senior Python Developer. We need someone with strong backend development skills.

Key Requirements:
• Bachelor's degree in Computer Science or equivalent experience
• 4+ years of Python development experience
• Strong knowledge of Python frameworks (Django, Flask, FastAPI)
• Experience with databases (PostgreSQL, MongoDB, Redis)
• Knowledge of RESTful API design and development
• Familiarity with cloud services (AWS, Docker, Kubernetes)
• Experience with testing frameworks (pytest, unittest)
• Understanding of software design patterns
• Knowledge of microservices architecture

Responsibilities:
• Design and develop scalable backend systems
• Build and maintain APIs
• Optimize database queries and performance
• Implement automated testing
• Deploy and monitor applications in production`
    };

    // DOM elements
    const resumeUpload = document.getElementById('resumeUpload');
    const resumeFile = document.getElementById('resumeFile');
    const jobDescription = document.getElementById('jobDescription');
    const sampleJobsSelect = document.getElementById('sampleJobs');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resultsContainer = document.getElementById('resultsContainer');
    const analysisResults = document.getElementById('analysisResults');

    // File upload handling
    resumeUpload.addEventListener('click', () => {
        resumeFile.click();
    });

    resumeUpload.addEventListener('dragover', (e) => {
        e.preventDefault();
        resumeUpload.classList.add('active');
    });

    resumeUpload.addEventListener('dragleave', () => {
        resumeUpload.classList.remove('active');
    });

    resumeUpload.addEventListener('drop', (e) => {
        e.preventDefault();
        resumeUpload.classList.remove('active');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            resumeFile.files = files;
            handleFileUpload(files[0]);
        }
    });

    resumeFile.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });

    // Sample job selection
    sampleJobsSelect.addEventListener('change', (e) => {
        if (e.target.value) {
            jobDescription.value = sampleJobs[e.target.value];
            checkFormValidity();
        }
    });

    // Job description input
    jobDescription.addEventListener('input', checkFormValidity);

    // Analyze button
    analyzeBtn.addEventListener('click', performAnalysis);

    // Handle file upload
    function handleFileUpload(file) {
        const fileName = file.name;
        const fileSize = (file.size / 1024 / 1024).toFixed(2);
        
        resumeUpload.innerHTML = `
            <i class="fas fa-file-alt"></i>
            <p><strong>${fileName}</strong></p>
            <p>Size: ${fileSize} MB</p>
            <small class="text-success">File uploaded successfully!</small>
        `;
        
        checkFormValidity();
    }

    // Check if form is valid
    function checkFormValidity() {
        const hasFile = resumeFile.files.length > 0;
        const hasJobDesc = jobDescription.value.trim().length > 0;
        
        analyzeBtn.disabled = !(hasFile && hasJobDesc);
    }

    // Perform analysis (demo simulation)
    function performAnalysis() {
        // Show loading state
        analyzeBtn.innerHTML = '<span class="loading"></span> Analyzing...';
        analyzeBtn.disabled = true;

        // Simulate AI processing
        setTimeout(() => {
            const mockResults = generateMockResults();
            displayResults(mockResults);
            
            // Reset button
            analyzeBtn.innerHTML = '<i class="fas fa-cog me-2"></i>Analyze Resume';
            analyzeBtn.disabled = false;
            
            // Show results
            resultsContainer.style.display = 'block';
            resultsContainer.scrollIntoView({ behavior: 'smooth' });
        }, 3000);
    }

    // Generate mock analysis results
    function generateMockResults() {
        const skills = extractSkillsFromJobDesc(jobDescription.value);
        const matchedSkills = skills.slice(0, Math.floor(skills.length * 0.7));
        const missingSkills = skills.slice(Math.floor(skills.length * 0.7));
        
        return {
            overallScore: Math.floor(Math.random() * 30) + 70, // 70-100%
            skillsMatch: Math.floor(Math.random() * 20) + 65,
            experienceMatch: Math.floor(Math.random() * 25) + 60,
            educationMatch: Math.floor(Math.random() * 20) + 70,
            matchedSkills: matchedSkills,
            missingSkills: missingSkills,
            recommendations: generateRecommendations(matchedSkills, missingSkills)
        };
    }

    // Extract skills from job description
    function extractSkillsFromJobDesc(text) {
        const commonSkills = [
            'Python', 'JavaScript', 'React', 'Node.js', 'SQL', 'MongoDB',
            'Machine Learning', 'Data Analysis', 'AWS', 'Docker', 'Git',
            'HTML', 'CSS', 'Django', 'Flask', 'TensorFlow', 'scikit-learn',
            'PostgreSQL', 'Redis', 'REST API', 'Microservices', 'Agile'
        ];
        
        return commonSkills.filter(skill => 
            text.toLowerCase().includes(skill.toLowerCase())
        ).slice(0, 8);
    }

    // Generate recommendations
    function generateRecommendations(matched, missing) {
        const recommendations = [];
        
        if (matched.length >= 5) {
            recommendations.push("Strong technical skill alignment with job requirements");
        }
        
        if (missing.length > 0) {
            recommendations.push(`Consider developing skills in: ${missing.slice(0, 3).join(', ')}`);
        }
        
        recommendations.push("Excellent candidate for technical interview");
        recommendations.push("Consider for senior-level position based on skill match");
        
        return recommendations;
    }

    // Display analysis results
    function displayResults(results) {
        analysisResults.innerHTML = `
            <div class="row">
                <div class="col-md-4 text-center mb-4">
                    <h3 class="match-score">${results.overallScore}%</h3>
                    <p class="text-muted">Overall Match Score</p>
                    <div class="progress mb-2">
                        <div class="progress-bar bg-success" style="width: ${results.overallScore}%"></div>
                    </div>
                </div>
                <div class="col-md-8">
                    <h5>Detailed Breakdown:</h5>
                    <div class="mb-3">
                        <div class="d-flex justify-content-between">
                            <span>Skills Match</span>
                            <span>${results.skillsMatch}%</span>
                        </div>
                        <div class="progress mb-2">
                            <div class="progress-bar bg-info" style="width: ${results.skillsMatch}%"></div>
                        </div>
                    </div>
                    <div class="mb-3">
                        <div class="d-flex justify-content-between">
                            <span>Experience Match</span>
                            <span>${results.experienceMatch}%</span>
                        </div>
                        <div class="progress mb-2">
                            <div class="progress-bar bg-warning" style="width: ${results.experienceMatch}%"></div>
                        </div>
                    </div>
                    <div class="mb-3">
                        <div class="d-flex justify-content-between">
                            <span>Education Match</span>
                            <span>${results.educationMatch}%</span>
                        </div>
                        <div class="progress">
                            <div class="progress-bar bg-primary" style="width: ${results.educationMatch}%"></div>
                        </div>
                    </div>
                </div>
            </div>
            
            <hr>
            
            <div class="row">
                <div class="col-md-6">
                    <h5><i class="fas fa-check-circle text-success me-2"></i>Matched Skills</h5>
                    <div class="mb-3">
                        ${results.matchedSkills.map(skill => 
                            `<span class="skill-tag matched">${skill}</span>`
                        ).join('')}
                    </div>
                </div>
                <div class="col-md-6">
                    <h5><i class="fas fa-exclamation-circle text-warning me-2"></i>Skills to Develop</h5>
                    <div class="mb-3">
                        ${results.missingSkills.map(skill => 
                            `<span class="skill-tag">${skill}</span>`
                        ).join('')}
                    </div>
                </div>
            </div>
            
            <hr>
            
            <div class="recommendations">
                <h5><i class="fas fa-lightbulb text-info me-2"></i>Recommendations</h5>
                <ul class="list-unstyled">
                    ${results.recommendations.map(rec => 
                        `<li class="mb-2"><i class="fas fa-arrow-right text-primary me-2"></i>${rec}</li>`
                    ).join('')}
                </ul>
            </div>
            
            <div class="text-center mt-4">
                <button class="btn btn-success me-2">
                    <i class="fas fa-download me-2"></i>Download Report
                </button>
                <button class="btn btn-primary" onclick="performAnalysis()">
                    <i class="fas fa-redo me-2"></i>Analyze Another
                </button>
            </div>
        `;
    }

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Fade in animation on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Observe elements for fade-in animation
    document.querySelectorAll('.feature-card, .process-step, .contact-item').forEach(el => {
        el.classList.add('fade-in');
        observer.observe(el);
    });

    // Navbar background change on scroll
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 100) {
            navbar.style.backgroundColor = 'rgba(0, 102, 204, 0.95)';
        } else {
            navbar.style.backgroundColor = 'rgba(0, 102, 204, 1)';
        }
    });

    // Initialize tooltips and other Bootstrap components
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Demo notification
    console.log('🤖 AI Resume Tool Demo Loaded Successfully!');
    console.log('📧 Contact: architjain2501@gmail.com');
    console.log('🐙 GitHub: https://github.com/archit2501');
});
