@echo off
cd ..
setlocal

REM =========================================================
REM Python Virtual Environment Setup Script
REM =========================================================

SET VENV_NAME=venv

echo.
echo ============================================
echo Creating virtual environment...
echo ============================================

python -m venv %VENV_NAME%

if errorlevel 1 (
echo ERROR: Failed to create virtual environment.
pause
exit /b 1
)

echo.
echo Virtual environment created: %VENV_NAME%

echo.
echo ============================================
echo Activating virtual environment...
echo ============================================

call %VENV_NAME%\Scripts\activate

echo.
echo ============================================
echo Upgrading pip...
echo ============================================

python -m pip install --upgrade pip

echo.
echo ============================================
echo Installing required libraries...
echo ============================================

pip install ^
matplotlib ^
Pillow ^
PyPDF2 ^
reportlab ^
charset-normalizer

if errorlevel 1 (
echo.
echo ERROR: Failed to install dependencies.
pause
exit /b 1
)

echo.
echo ============================================
echo Generating requirements.txt...
echo ============================================

pip freeze > requirements.txt

echo.
echo ============================================
echo Environment setup completed successfully!
echo ============================================

pause
