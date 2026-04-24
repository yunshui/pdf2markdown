#!/usr/bin/env python3
"""Main entry point script for PDF to Markdown converter."""

import sys
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_dir))

from src.main import main

if __name__ == '__main__':
    main()