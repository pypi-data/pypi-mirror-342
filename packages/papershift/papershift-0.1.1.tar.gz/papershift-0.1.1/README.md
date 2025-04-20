# PaperShift

A Python library for converting PDF documents to Markdown format with AI assistance. Shift from scanned documents to editable, searchable text.

## Features

- Converts PDF documents to well-formatted Markdown
- Process documents in parallel for faster conversion
- Optimized memory usage with batch processing
- Fast mode option for quicker processing with lower resolution
- Detailed progress reporting
- Customizable AI model selection
- Adaptive resolution based on output requirements

## Installation

```bash
pip install papershift
```

## Usage

```python
from papershift import convert_pdf_to_markdown

# Basic usage
markdown_content = convert_pdf_to_markdown(
    pdf_path="path/to/your/document.pdf",
    api_key="your-openrouter-api-key"
)

# Advanced usage with options
markdown_content = convert_pdf_to_markdown(
    pdf_path="path/to/your/document.pdf",
    output_dir="output_folder",
    dpi=300,
    target_height_px=2048,
    model="openrouter/google/gemini-2.0-flash-001",
    api_key="your-openrouter-api-key",
    max_workers=4,
    batch_size=5,
    fast_mode=True
)

# Save the output
with open("output.md", "w", encoding="utf-8") as f:
    f.write(markdown_content)
```

## Configuration Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| pdf_path | Path to the PDF file | (Required) |
| output_dir | Directory to save the output markdown files | None |
| dpi | DPI for image rendering | 300 |
| target_height_px | Target height in pixels | 2048 |
| aspect_threshold | Aspect ratio threshold for height adjustment | 1.5 |
| prompt | Text prompt to send with each page image | "Convert this document to markdown" |
| model | The model to use for processing | "openrouter/google/gemini-2.0-flash-001" |
| api_key | OpenRouter API key | None |
| site_url | Optional site URL for OpenRouter | None |
| app_name | Optional app name for OpenRouter | None |
| combined_output | If True, returns a single string with all pages combined | True |
| verbose | If True, prints progress information | False |
| max_workers | Maximum number of worker processes for PDF conversion | 4 |
| batch_size | Number of pages to process in a single batch | 5 |
| quality | Image quality (1-100) for JPEG compression in fast mode | 95 |
| fast_mode | If True, uses reduced resolution and JPEG format for faster processing | False |

## Dependencies

- PyMuPDF: PDF processing library
- litellm: LLM API integration
- openrouter: API for accessing various AI models
- python-dotenv: Environment variable management