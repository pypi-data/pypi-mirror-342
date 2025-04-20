@echo off
echo =============================================
echo    Codebase Indexer Windows Installer
echo =============================================
echo.

:: Check if Python is installed
python --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found. Please install Python 3.8 or newer.
    exit /b 1
)

:: Check if pip is installed
pip --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] pip not found. Please ensure pip is installed with Python.
    exit /b 1
)

:: Install the package
echo [INFO] Installing codebase-indexer...
pip install --user codebase-indexer
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Installation failed.
    exit /b 1
)
echo [SUCCESS] Package installed successfully.

:: Find the script location
echo [INFO] Finding script location...
for /f "tokens=*" %%a in ('python -c "import site; print(site.USER_SITE.replace('site-packages', 'Scripts'))"') do set SCRIPT_DIR=%%a

echo [INFO] Expected script location: %SCRIPT_DIR%

:: Check if script exists
if exist "%SCRIPT_DIR%\codebase-indexer.exe" (
    echo [SUCCESS] Found codebase-indexer.exe in %SCRIPT_DIR%
) else (
    echo [WARNING] Could not find codebase-indexer.exe in the expected location.
    echo [INFO] Searching for script...
    
    for /f "tokens=*" %%a in ('where /r "%USERPROFILE%\AppData\Roaming\Python" codebase-indexer.exe 2^>nul') do (
        set FOUND_SCRIPT=%%a
        echo [SUCCESS] Found script at: %%a
        for %%b in ("%%a") do set SCRIPT_DIR=%%~dpb
        goto :script_found
    )
    
    echo [WARNING] Could not find the script.
    echo [INFO] Will add common Python script directories to PATH.
    set SCRIPT_DIR=%USERPROFILE%\AppData\Roaming\Python\Python39\Scripts;%USERPROFILE%\AppData\Roaming\Python\Python38\Scripts
)

:script_found

:: Add script directory to PATH temporarily for this session
echo [INFO] Adding script directory to PATH for this session...
set PATH=%PATH%;%SCRIPT_DIR%

:: Offer to add to PATH permanently
echo.
echo [INFO] To run codebase-indexer from anywhere, you need to add it to your PATH.
echo        Current path: %SCRIPT_DIR%
echo.
set /p ADD_TO_PATH="Would you like to add this directory to your PATH permanently? (y/N): "

if /i "%ADD_TO_PATH%"=="y" (
    echo [INFO] Adding to PATH permanently...
    
    :: Use setx to modify the PATH - limited to 1024 characters
    setx PATH "%PATH%;%SCRIPT_DIR%"
    
    echo [SUCCESS] Added to PATH. You may need to restart your command prompt.
) else (
    echo.
    echo [INFO] You can run codebase-indexer using one of these methods:
    echo        1. Using the full path: %SCRIPT_DIR%\codebase-indexer.exe
    echo        2. Using Python module: python -m src.main
    echo        3. Using alternate names: indexer or code-indexer
    echo.
)

echo.
echo [INFO] Testing installation...
codebase-indexer --help > nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] codebase-indexer command is working!
) else (
    echo [WARNING] Command not found in current session.
    echo           Please restart your command prompt or use full path:
    echo           %SCRIPT_DIR%\codebase-indexer.exe
)

echo.
echo =============================================
echo          Installation Complete
echo =============================================
echo.
echo You can now use codebase-indexer with:
echo.
echo 1. Configure your API keys:
echo    codebase-indexer configure
echo.
echo 2. Index a codebase:
echo    codebase-indexer index --path C:\path\to\your\codebase
echo.
echo If the command is still not found after restarting your command prompt, try:
echo    %SCRIPT_DIR%\codebase-indexer.exe
echo    python -m src.main
echo.
echo For more help, see the troubleshooting section in the README.