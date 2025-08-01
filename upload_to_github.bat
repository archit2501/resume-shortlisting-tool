@echo off
echo.
echo ================================================
echo   GITHUB UPLOAD SCRIPT FOR ARCHIT JAIN
echo   Resume Shortlisting Tool
echo ================================================
echo.

REM Navigate to project directory
cd /d "d:\Users\Jain\Desktop\projects\Resume shortlisting"

echo Current directory: %CD%
echo.

echo Step 1: Initializing Git repository...
git init

echo.
echo Step 1.5: Configuring Git user information...
git config user.name "archit2501"
git config user.email "architjain2501@gmail.com"

echo.
echo Step 2: Adding remote repository...
git remote add origin https://github.com/archit2501/resume-shortlisting-tool.git

echo.
echo Step 3: Adding all files...
git add .

echo.
echo Step 4: Setting up git user configuration...
git config user.name "archit2501"
git config user.email "architjain2501@gmail.com"

echo.
echo Step 5: Creating commit...
git commit -m "Added GitHub Pages website and updated project for web deployment"

echo.
echo Step 6: Pushing to GitHub...
echo Note: You may be prompted for GitHub credentials
echo Username: archit2501
echo Password: Use your Personal Access Token (not your password)
echo.

git push -u origin main

echo.
if %ERRORLEVEL% EQU 0 (
    echo ================================================
    echo ✅ SUCCESS! Your project is now on GitHub!
    echo ================================================
    echo.
    echo Your repository is live at:
    echo https://github.com/archit2501/resume-shortlisting-tool
    echo.
    echo Next steps:
    echo 1. Visit your repository URL above
    echo 2. Add more screenshots to screenshots/ folder
    echo 3. Test your AI analysis and document results
    echo 4. Share your project with potential employers!
) else (
    echo ================================================
    echo ❌ Upload failed - Please check the error above
    echo ================================================
    echo.
    echo Common solutions:
    echo 1. Make sure you created the repository on GitHub first
    echo 2. Use Personal Access Token instead of password
    echo 3. Check your internet connection
    echo 4. Verify repository name: resume-shortlisting-tool
)

echo.
pause
