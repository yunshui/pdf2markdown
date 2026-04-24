"""Command-line interface for PDF to Markdown converter."""

import argparse
import sys
from pathlib import Path

from .config import Config
from .converter import PDFToMarkdownConverter
from .logger import get_logger
from .state_manager import StateManager


def parse_args():
    """Parse command-line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description='Convert PDF files to Markdown format using LLM',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s document.pdf
  %(prog)s document.pdf --model gpt-4-vision-preview
  %(prog)s document.pdf --api-url https://api.example.com/v1
  %(prog)s document.pdf --max-retries 5
  %(prog)s document.pdf --config /path/to/config.json
        '''
    )

    # Positional arguments
    parser.add_argument(
        'pdf_path',
        help='Path to the PDF file to convert'
    )

    # Configuration
    parser.add_argument(
        '--config', '-c',
        help='Path to configuration file (default: conf/setting.json)'
    )

    # Model settings
    parser.add_argument(
        '--model',
        help='Model name to use (overrides config)'
    )
    parser.add_argument(
        '--api-url',
        help='API URL for the model (overrides config)'
    )
    parser.add_argument(
        '--api-key',
        help='API key for authentication (overrides config)'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        help='Request timeout in seconds (overrides config)'
    )

    # Conversion settings
    parser.add_argument(
        '--max-retries',
        type=int,
        help='Maximum number of retry attempts (overrides config)'
    )
    parser.add_argument(
        '--single-page-prompt',
        help='Prompt for single page conversion (overrides config)'
    )
    parser.add_argument(
        '--multi-page-summary-prompt',
        help='Prompt for multi-page summary (overrides config)'
    )

    # Paths
    parser.add_argument(
        '--output-dir',
        help='Output directory for Markdown files (overrides config)'
    )
    parser.add_argument(
        '--logs-dir',
        help='Directory for log files (overrides config)'
    )

    # Options
    parser.add_argument(
        '--validate-api',
        action='store_true',
        help='Validate API connectivity before conversion'
    )
    parser.add_argument(
        '--resume',
        action='store_true',
        help='Resume from previous interrupted conversion'
    )
    parser.add_argument(
        '--reset-state',
        action='store_true',
        help='Reset state and start from the beginning'
    )
    parser.add_argument(
        '--show-progress',
        action='store_true',
        help='Show current progress without performing conversion'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    return parser.parse_args()


def main():
    """Main entry point for the CLI."""
    args = parse_args()

    # Validate PDF path
    pdf_path = args.pdf_path
    if not Path(pdf_path).exists():
        print(f"Error: PDF file not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    if not pdf_path.lower().endswith('.pdf'):
        print(f"Error: File must have .pdf extension: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    # Load configuration
    try:
        config = Config(args.config)
    except Exception as e:
        print(f"Error: Failed to load configuration: {e}", file=sys.stderr)
        sys.exit(1)

    # Override configuration with command-line arguments
    if args.model:
        config.update(**{'model.name': args.model})
    if args.api_url:
        config.update(**{'model.api_url': args.api_url})
    if args.api_key:
        config.update(**{'model.api_key': args.api_key})
    if args.timeout:
        config.update(**{'model.timeout': args.timeout})
    if args.max_retries:
        config.update(**{'conversion.max_retries': args.max_retries})
    if args.single_page_prompt:
        config.update(**{'conversion.single_page_prompt': args.single_page_prompt})
    if args.multi_page_summary_prompt:
        config.update(**{'conversion.multi_page_summary_prompt': args.multi_page_summary_prompt})
    if args.output_dir:
        config.update(**{'paths.output_dir': args.output_dir})
    if args.logs_dir:
        config.update(**{'paths.logs_dir': args.logs_dir})

    # Initialize logger
    logger = get_logger("pdf2markdown", config.logs_dir)

    # Validate API if requested
    if args.validate_api:
        print("Validating API connectivity...")
        temp_client = PDFToMarkdownConverter(config).model_client
        success, message = temp_client.validate_api()
        if success:
            print(f"✓ API validation successful: {message}")
        else:
            print(f"✗ API validation failed: {message}", file=sys.stderr)
            sys.exit(1)

    # Check required configuration
    if not config.api_url:
        print("Error: API URL is not configured. Please set it in conf/setting.json or use --api-url",
              file=sys.stderr)
        sys.exit(1)

    # Perform conversion
    try:
        converter = PDFToMarkdownConverter(config, resume=args.resume)

        # Show progress only mode
        if args.show_progress:
            base_name = Path(pdf_path).stem
            state_manager = StateManager(config.output_dir, base_name)
            state_manager.show_progress()
            sys.exit(0)

        # Reset state if requested
        if args.reset_state:
            base_name = Path(pdf_path).stem
            state_manager = StateManager(config.output_dir, base_name)
            state_manager.reset()
            print("✓ State reset successfully")
            print("  You can now start a fresh conversion")
            sys.exit(0)

        success, result = converter.convert(pdf_path)

        if success:
            print(f"✓ Conversion successful!")
            print(f"  Output: {result}")
            logger.info(f"Conversion completed successfully", output=result)
            sys.exit(0)
        else:
            print(f"✗ Conversion failed: {result}", file=sys.stderr)
            logger.error(f"Conversion failed", error=result)
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nConversion interrupted by user", file=sys.stderr)
        logger.warning("Conversion interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"Error: Unexpected error occurred: {e}", file=sys.stderr)
        logger.error("Unexpected error during conversion", exception=e)
        sys.exit(1)


if __name__ == '__main__':
    main()