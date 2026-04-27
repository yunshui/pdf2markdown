# PDF to Markdown Converter Skill

Convert PDF files to Markdown format using LLM vision models.

## Features

- Convert single-page and multi-page PDFs
- Resume from interrupted conversions
- Format preservation (tables, headings, lists)
- Page summary generation for navigation
- Progress tracking and time estimation

## Usage

### Basic Usage

```bash
python main.py document.pdf
```

### With API Key

```bash
export PDF2MD_API_KEY="your-api-key-here"
python main.py document.pdf
```

Or use command line:

```bash
python main.py document.pdf --api-key your-api-key
```

### Resume Conversion

```bash
python main.py document.pdf --resume
```

### Show Progress

```bash
python main.py document.pdf --show-progress
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `PDF2MD_API_URL` | LLM API endpoint | No |
| `PDF2MD_API_KEY` | LLM API key | Yes |

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--config` | Path to config file | - |
| `--model` | Model name | qwen3.5-plus |
| `--api-url` | API URL | (env or default) |
| `--api-key` | API key | (env) |
| `--timeout` | Timeout (seconds) | 120 |
| `--max-retries` | Max retries | 3 |
| `--output-dir` | Output directory | output |
| `--resume` | Resume from previous | false |
| `--show-progress` | Show progress only | false |
| `--verbose` | Verbose output | false |

## Output

### Single Page PDF

```
output/
└── document.md
```

### Multi Page PDF

```
output/
└── document_md/
    ├── document.md          # Index file
    ├── .state.json          # State file
    └── pages/
        ├── page_1.md
        ├── page_1_summary.txt
        └── ...
```

## Requirements

- Python 3.10+
- Stable internet connection
- LLM API access (Qwen/OpenAI-compatible)

## License

MIT