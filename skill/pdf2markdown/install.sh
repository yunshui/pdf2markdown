#!/bin/bash
# PDF to Markdown Converter Skill - Install Script

set -e

echo "=================================="
echo "PDF to Markdown Converter Skill"
echo "=================================="
echo ""

# Check Python 3.10+
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "✗ Error: Python 3 is not installed"
    exit 1
fi

python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Check minimum version
required_version="3.10"
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "✗ Error: Python 3.10+ required (current: $python_version)"
    exit 1
fi

# Check pip
echo "Checking pip..."
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "✗ Error: pip is not installed"
    exit 1
fi
echo "✓ pip is available"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip

if pip install -r requirements.txt; then
    echo "✓ Dependencies installed successfully"
else
    echo "✗ Error: Failed to install dependencies"
    exit 1
fi

# Verify installation
echo ""
echo "Verifying installation..."
if python3 -c "import fitz, requests, PIL, tqdm" 2>/dev/null; then
    echo "✓ All dependencies verified"
else
    echo "✗ Error: Some dependencies are missing"
    exit 1
fi

echo ""
echo "=================================="
echo "✓ Installation complete!"
echo "=================================="
echo ""
echo "Usage:"
echo "  python main.py document.pdf --api-key YOUR_API_KEY"
echo ""
echo "Or set API key as environment variable:"
echo "  export PDF2MD_API_KEY='your-api-key'"
echo "  python main.py document.pdf"
echo ""
echo "Run tests:"
echo "  python test.py"
echo ""