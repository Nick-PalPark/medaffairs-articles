#!/bin/bash
# Simple wrapper script for the articles capture workflow

echo "Medical Affairs Articles Capture"
echo "================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if config exists
if [ ! -f "config.py" ]; then
    echo "ERROR: config.py not found!"
    echo "Please copy config_template.py to config.py and configure your Inoreader credentials."
    exit 1
fi

# Run the capture workflow
echo "Starting articles capture..."
python capture_articles.py

echo "Done!"