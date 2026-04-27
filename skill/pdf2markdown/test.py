#!/usr/bin/env python3
"""
Test script for PDF to Markdown Converter Skill.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")

    try:
        from src.config import Config
        print("  ✓ config")
    except Exception as e:
        print(f"  ✗ config: {e}")
        return False

    try:
        from src.logger import get_logger
        print("  ✓ logger")
    except Exception as e:
        print(f"  ✗ logger: {e}")
        return False

    try:
        from src.pdf_processor import PDFProcessor
        print("  ✓ pdf_processor")
    except Exception as e:
        print(f"  ✗ pdf_processor: {e}")
        return False

    try:
        from src.model_client import ModelClient
        print("  ✓ model_client")
    except Exception as e:
        print(f"  ✗ model_client: {e}")
        return False

    try:
        from src.converter import PDFToMarkdownConverter
        print("  ✓ converter")
    except Exception as e:
        print(f"  ✗ converter: {e}")
        return False

    try:
        from src.state_manager import StateManager
        print("  ✓ state_manager")
    except Exception as e:
        print(f"  ✗ state_manager: {e}")
        return False

    print("\n✓ All imports successful!\n")
    return True


def test_config():
    """Test configuration loading."""
    print("Testing configuration...")

    try:
        config = Config()
        print(f"  ✓ Config loaded")
        print(f"    Model: {config.model.get('name', 'N/A')}")
        print(f"    API URL: {config.api_url or 'N/A'}")
        print(f"    Max retries: {config.model.get('max_retries', 'N/A')}")
        print()
        return True
    except Exception as e:
        print(f"  ✗ Config: {e}")
        print()
        return False


def test_pdf_processor():
    """Test PDF processor."""
    print("Testing PDF processor...")

    try:
        from src.pdf_processor import PDFProcessor
        processor = PDFProcessor()
        print("  ✓ PDFProcessor initialized")

        # Check if test PDF exists
        test_pdf = Path("test.pdf")
        if test_pdf.exists():
            page_count = processor.get_page_count(str(test_pdf))
            print(f"  ✓ Test PDF has {page_count} pages")
        else:
            print("  ℹ  No test.pdf found, skipping page count test")

        print()
        return True
    except Exception as e:
        print(f"  ✗ PDFProcessor: {e}")
        print()
        return False


def main():
    """Run all tests."""
    print("=" * 50)
    print("PDF to Markdown Converter Skill - Tests")
    print("=" * 50)
    print()

    results = []
    results.append(("Imports", test_imports()))
    results.append(("Configuration", test_config()))
    results.append(("PDF Processor", test_pdf_processor()))

    print("=" * 50)
    print("Test Results")
    print("=" * 50)

    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {name}")

    all_passed = all(r[1] for r in results)
    print()
    if all_passed:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())