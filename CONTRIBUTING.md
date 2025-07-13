# Contributing to Resume Shortlisting Tool

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- Git
- Basic knowledge of Flask, NLP, or machine learning (depending on contribution area)

### Development Setup
1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/resume-shortlisting-tool.git
   cd resume-shortlisting-tool
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```
5. Run tests to ensure everything works:
   ```bash
   python test_installation.py
   ```

## 🎯 How to Contribute

### Reporting Bugs
1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/resume-shortlisting-tool/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce the bug
   - Expected vs actual behavior
   - Your environment (OS, Python version, etc.)
   - Screenshots if applicable

### Suggesting Features
1. Check [Discussions](https://github.com/yourusername/resume-shortlisting-tool/discussions) for similar ideas
2. Create a new discussion with:
   - Clear description of the feature
   - Use case and benefits
   - Possible implementation approach

### Code Contributions

#### Areas for Contribution
- **🧠 NLP & ML**: Improve skill extraction, add new similarity algorithms
- **🌐 Frontend**: Enhance UI/UX, add new visualizations
- **⚡ Backend**: Optimize performance, add new API endpoints
- **📱 Mobile**: Improve responsive design
- **🧪 Testing**: Add unit tests, integration tests
- **📚 Documentation**: Improve docs, add tutorials
- **🔧 DevOps**: Docker, CI/CD, deployment guides

#### Pull Request Process
1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Add tests if applicable
4. Ensure all tests pass:
   ```bash
   python test_installation.py
   ```
5. Format your code:
   ```bash
   black *.py
   flake8 *.py
   ```
6. Commit with a clear message:
   ```bash
   git commit -m "Add: new skill extraction algorithm for technical roles"
   ```
7. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
8. Create a Pull Request on GitHub

## 📝 Code Style Guidelines

### Python Code
- Follow PEP 8 style guide
- Use `black` for code formatting
- Use `flake8` for linting
- Add docstrings to all functions and classes
- Keep functions small and focused
- Use meaningful variable names

### Frontend Code
- Use consistent indentation (2 spaces for HTML/CSS/JS)
- Follow Bootstrap conventions
- Add comments for complex JavaScript logic
- Ensure mobile responsiveness

### Commit Messages
Use conventional commit format:
- `Add: new feature`
- `Fix: bug description`
- `Update: component improvement`
- `Remove: deprecated code`
- `Docs: documentation update`

## 🧪 Testing Guidelines

### Running Tests
```bash
# Full installation test
python test_installation.py

# Test individual components
python -c "from match_engine import ResumeJobMatcher; print('Match engine works!')"
```

### Adding Tests
- Add unit tests for new functions
- Test edge cases and error conditions
- Include sample data for testing
- Document test scenarios

## 📚 Documentation

### Code Documentation
- Add docstrings to all public functions
- Include parameter types and return values
- Add usage examples for complex functions

### User Documentation
- Update README.md for new features
- Add screenshots for UI changes
- Update help.html for user-facing features
- Include code examples

## 🔍 Review Process

### What We Look For
- ✅ Code quality and readability
- ✅ Proper error handling
- ✅ Test coverage for new features
- ✅ Documentation updates
- ✅ Performance considerations
- ✅ Security best practices

### Review Timeline
- Initial review: 2-3 days
- Feedback incorporation: As needed
- Final approval: 1-2 days

## 🏷️ Release Process

### Version Numbers
We use Semantic Versioning (SemVer):
- Major (1.x.x): Breaking changes
- Minor (x.1.x): New features, backward compatible
- Patch (x.x.1): Bug fixes

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version numbers bumped
- [ ] GitHub release created

## 🤝 Community Guidelines

### Be Respectful
- Use inclusive language
- Be constructive in feedback
- Help newcomers
- Respect different opinions

### Communication Channels
- **Issues**: Bug reports and feature requests
- **Discussions**: General questions and ideas
- **Pull Requests**: Code reviews and discussions
- **Email**: Direct contact for sensitive matters

## 📋 Contribution Checklist

Before submitting a contribution:
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] Pull request description is detailed
- [ ] Screenshots included for UI changes

## 🎉 Recognition

Contributors will be:
- Listed in the project's contributors section
- Mentioned in release notes for significant contributions
- Given credit in documentation they help create

Thank you for contributing to the Resume Shortlisting Tool! 🚀
