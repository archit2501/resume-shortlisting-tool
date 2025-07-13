@echo off
echo.
echo ================================================
echo   SCREENSHOT COPY SCRIPT FOR GITHUB
echo ================================================
echo.

REM Set source path (the WhatsApp image)
set "SOURCE=c:\Users\Jain\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\TempState\FA1DCF25E93FEABD8335F5D20BFF7172\WhatsApp Image 2025-07-09 at 00.41.15_e5b7cd01.jpg"

REM Set destination path
set "DEST=screenshots\main-interface.png"

echo Copying screenshot for GitHub repository...
echo.
echo Source: %SOURCE%
echo Destination: %DEST%
echo.

REM Check if source file exists
if exist "%SOURCE%" (
    echo ✓ Source file found!
    
    REM Copy the file
    copy "%SOURCE%" "%DEST%" >nul 2>&1
    
    if exist "%DEST%" (
        echo ✓ Screenshot copied successfully to screenshots\main-interface.png
        echo.
        echo Next steps:
        echo 1. Take more screenshots ^(results page, batch analysis^)
        echo 2. Run: git add screenshots/
        echo 3. Run: git commit -m "Add: project screenshots"
        echo 4. Run: git push
    ) else (
        echo ✗ Failed to copy screenshot
    )
) else (
    echo ✗ Source screenshot not found at expected location
    echo.
    echo Please manually copy your screenshot to:
    echo screenshots\main-interface.png
)

echo.
echo ================================================
pause
