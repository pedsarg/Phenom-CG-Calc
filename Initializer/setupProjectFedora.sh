#!/bin/bash

echo "========================================================="
echo "Python Virtual Environment Setup Script for Linux"
echo "========================================================="
cd ..
VENV_NAME="venv"

echo
echo "============================================"
echo "Creating virtual environment..."
echo "============================================"

python3 -m venv "$VENV_NAME"

if [ $? -ne 0 ]; then
echo "ERROR: Failed to create virtual environment."
exit 1
fi

echo
echo "Virtual environment created: $VENV_NAME"

echo
echo "============================================"
echo "Activating virtual environment..."
echo "============================================"

source "$VENV_NAME/bin/activate"

echo
echo "============================================"
echo "Upgrading pip..."
echo "============================================"

python -m pip install --upgrade pip

echo
echo "============================================"
echo "Installing required libraries..."
echo "============================================"

pip install \
matplotlib \
Pillow \
PyPDF2 \
reportlab \
charset-normalizer

if [ $? -ne 0 ]; then
echo
echo "ERROR: Failed to install dependencies."
exit 1
fi

echo
echo "============================================"
echo "Generating requirements.txt..."
echo "============================================"

pip freeze > requirements.txt

echo
echo "============================================"
echo "Environment setup completed successfully!"
echo "============================================"
