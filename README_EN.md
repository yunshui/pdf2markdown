# PDF to Markdown Converter

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-production--ready-brightgreen.svg)]()

A Python tool that converts PDF documents to Markdown format using Large Language Models (LLMs). Default model: Qwen3.5-Plus.

## ✨ Features

- 📄 **Single/Multi-page Support** - Automatically detects and processes single or multi-page PDFs
- 🔄 **Smart Retry** - Automatic retry on network errors ensures successful conversion
- 📝 **Comprehensive Logging** - Daily detailed logs with execution context
- ⚙️ **Flexible Configuration** - JSON config file and command-line parameters
- 🎯 **Format Preservation** - Maintains original PDF formatting and structure
- 🔍 **Page Summaries** - Auto-generates Chinese page summaries for multi-page PDFs
- 🚀 **Easy to Use** - One command to complete conversion

## 📦 Installation

### Prerequisites

- Python 3.10+
- pip

### Installation Steps

```bash
# Clone the repository
git clone <repository-url>
cd pdf2markdown

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Quick Start

### 1. Configure API

Edit `conf/setting.json` to configure your API:

```json
{
  "model": {
    "name": "qwen3.5-plus",
    "api_url": "https://coding.dashscope.aliyuncs.com/v1/chat/completions",
    "api_key": "your-api-key-here",
    "timeout": 60
  },
  "conversion": {
    "max_retries": 3,
    "single_page_prompt": "请将这张图片中的内容转换为Markdown格式，保持原有的格式和结构。",
    "multi_page_summary_prompt": "请总结这张图片中的关键信息，用简短的中文描述。"
  },
  "paths": {
    "output_dir": "output",
    "logs_dir": "logs"
  }
}
```

### 2. Convert PDF

```bash
# Basic usage
python3 pdf2md.py document.pdf

# Validate API connection
python3 pdf2md.py document.pdf --validate-api

# Custom retry count
python3 pdf2md.py document.pdf --max-retries 5

# Specify output directory
python3 pdf2md.py document.pdf --output-dir ./markdown_output
```

## 📖 Usage

### Command-line Arguments

| Parameter | Description | Default |
|-----------|-------------|---------|
| `pdf_path` | PDF file path (required) | - |
| `--config, -c` | Configuration file path | conf/setting.json |
| `--model` | Model name | Config value |
| `--api-url` | API endpoint URL | Config value |
| `--api-key` | API key | Config value |
| `--timeout` | Request timeout (seconds) | 120 |
| `--max-retries` | Max retry count | Config value |
| `--single-page-prompt` | Single page prompt | Config value |
| `--multi-page-summary-prompt` | Multi-page summary prompt | Config value |
| `--output-dir` | Output directory | output |
| `--logs-dir` | Log directory | logs |
| `--validate-api` | Validate API connection | false |
| `--resume` | Resume from previous interruption | false |
| `--reset-state` | Reset state and start from beginning | false |
| `--show-progress` | Show current progress (no conversion) | false |
| `-v, --verbose` | Verbose output | false |
| `--version` | Show version | - |
| `--help` | Show help | - |

### New Features

#### Progress Display
- Real-time console progress bar
- Per-page processing time statistics
- Remaining time estimation
- Average time per page display

#### Resume Capability
- Support for interrupt and resume (Ctrl+C)
- Automatic state saving
- Skip completed pages
- Retry failed pages

#### Fault Tolerance
- Single page failure doesn't stop entire conversion
- Generate placeholder files for failed pages
- Record error details
- Generate failure report after completion

### Output Format

#### Single-page PDF
```
output/
└── document.md    # Complete Markdown content
```

#### Multi-page PDF
```
output/
└── document_md/
    ├── document.md          # Main index file with navigation links and Chinese summaries
    └── pages/
        ├── page_1.md        # Page 1 complete content
        ├── page_2.md        # Page 2 complete content
        └── ...
```

### Configuration

#### Model Configuration
- `name`: Model name (e.g., qwen3.5-plus, gpt-4-vision-preview)
- `api_url`: API endpoint URL (supports full path or base URL)
- `api_key`: API key
- `timeout`: Request timeout (seconds)

#### Conversion Configuration
- `max_retries`: Retry count on failure
- `single_page_prompt`: Prompt for single page conversion
- `multi_page_summary_prompt`: Prompt for multi-page summary

#### Paths Configuration
- `output_dir`: Markdown output directory
- `logs_dir`: Log file directory

### Usage Examples

#### Basic Usage
```bash
# Convert PDF (shows progress bar)
python3 pdf2md.py document.pdf
```

#### Resume Capability
```bash
# Resume after interruption
python3 pdf2md.py document.pdf --resume

# Show current progress (no conversion)
python3 pdf2md.py document.pdf --show-progress

# Reset state and start from beginning
python3 pdf2md.py document.pdf --reset-state
```

#### Console Progress Output Example
```
[Processing page 5/87] Progress: 5.75% (5/87 done, 0 failed)
  Average: 45s/page | Estimated remaining: 1h 2m 15s
```

#### Handling Failed Pages
If a page conversion fails, the tool will:
1. Generate `page_X_error.md` placeholder file
2. Record error details
3. Continue processing subsequent pages
4. Generate failure report after completion

#### Log Time Estimation
Logs will show:
```
2026-04-24 18:00:00 - PDFToMarkdownConverter - INFO - Time estimation: Page 5/87
  | current_page: 5
  | total_pages: 87
  | average_time: 45.2
  | total_elapsed: 226.0
  | estimated_remaining: 3710.8
```

## 📚 Documentation

- [Requirements](docs/requirements.md) - Functional requirements, non-functional requirements, acceptance criteria
- [Technical](docs/technical.md) - Tech stack, system architecture, API reference
- [Design](docs/design.md) - Design principles, system design, interface design
- [Workflow](docs/workflow.md) - Detailed workflow documentation
- [Workflow Rules](docs/workflow-rules.md) - Project workflow and decision-making rules ⭐
- [Lessons Learned](docs/lessons-learned.md) - Experiences and lessons from development
- [Progress](docs/progress.md) - Implementation progress and test results

## 🏗️ Project Structure

```
pdf2markdown/
├── bin/                        # Executable files
│   └── pdf2md                  # Startup script
├── conf/                       # Configuration files
│   └── setting.json            # Configuration file
├── docs/                       # Documentation
│   ├── requirements.md         # Requirements document
│   ├── technical.md            # Technical document
│   ├── design.md               # Design document
│   ├── workflow.md             # Workflow document
│   ├── lessons-learned.md      # Lessons learned
│   └── progress.md             # Project progress
├── logs/                       # Log directory (daily)
├── output/                     # Output directory
├── src/                        # Source code
│   ├── __init__.py
│   ├── main.py                 # CLI entry point
│   ├── config.py               # Configuration management
│   ├── logger.py               # Logging system
│   ├── pdf_processor.py        # PDF processing
│   ├── model_client.py         # Model client
│   └── converter.py            # Conversion logic
├── tests/                      # Test code
├── CLAUDE.md                   # Claude project documentation
├── pdf2md.py                   # Main entry script
├── requirements.txt            # Python dependencies
├── README.md                   # This file (Chinese)
└── README_EN.md                # English documentation
```

## 🔧 Tech Stack

- **Python 3.10+** - Main programming language
- **PyMuPDF** - PDF processing and rendering
- **Pillow** - Image processing
- **requests** - HTTP requests
- **tqdm** - Progress display (reserved)

## 📊 Performance

| Metric | Value |
|--------|-------|
| Single-page conversion time | ~24 seconds |
| Multi-page conversion time | ~33 seconds/page |
| Memory usage | < 200MB |
| Image resolution | 1654x2339 (200 DPI) |

## ⚠️ Notes

1. **API Key Security** - Please keep your API key secure and don't commit it to version control
2. **Network Requirement** - Stable network connection required for API access
3. **Processing Time** - Large PDF files may take longer to process
4. **API Costs** - API calls may incur charges, please monitor usage
5. **Log Management** - Log files will grow continuously, clean up regularly

## 🐛 Troubleshooting

### Issue: 404 Error
**Cause**: Incorrect API URL configuration

**Solution**:
```bash
# Check api_url in config file
cat conf/setting.json

# Validate API connection
python3 pdf2md.py test.pdf --validate-api
```

### Issue: Timeout
**Cause**: Slow network or large file size

**Solution**:
```bash
# Increase timeout
python3 pdf2md.py document.pdf --timeout 120

# Reduce DPI to decrease image size (requires code modification)
```

### Issue: Conversion Failed
**Cause**: Invalid API key or insufficient quota

**Solution**:
```bash
# Check API key configuration
# Update api_key and retry
python3 pdf2md.py document.pdf --api-key your-new-key
```

## 🤝 Contributing

Contributions are welcome! Feel free to submit code, report issues, or suggest improvements.

### Development Workflow

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards

- Follow PEP 8 style guide
- Add necessary comments and docstrings
- Write test cases
- Update relevant documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- [PyMuPDF](https://pymupdf.readthedocs.io/) - PDF processing library
- [Qwen](https://help.aliyun.com/zh/dashscope/) - Qwen LLM
- [OpenAI API](https://platform.openai.com/docs/api-reference) - API format reference

## 📞 Contact

For questions or suggestions, please contact via:

- Submit an [Issue](https://github.com/your-repo/issues)
- Email: your-email@example.com

## 📝 Changelog

### v1.0.0 (2026-04-24)
- ✨ Initial release
- ✅ Single-page PDF conversion
- ✅ Multi-page PDF conversion
- ✅ Comprehensive logging system
- ✅ Flexible configuration management
- ✅ Retry mechanism and timeout control

---

**Made with ❤️ by AI Assistant**