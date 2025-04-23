import base64
import os
import json
from typing import Dict, Any, Optional, Union

# Import the LiteLLM library
from litellm import completion




def process_page(
    base64_image: str,
    prompt: str = "Convert this document to markdown",
    model: str = "openrouter/google/gemini-2.0-flash-001",
    api_key: Optional[str] = None,
    site_url: Optional[str] = None,
    app_name: Optional[str] = None,
    output_file: Optional[str] = None
) -> str:
    """
    Process a page (as base64 encoded image) using LiteLLM and a vision model.
    
    Args:
        base64_image: Base64 encoded string of the image/page
        prompt: Text prompt to send with the image/page
        model: The model to use for processing (default: openrouter/google/gemini-2.0-flash-001)
        api_key: OpenRouter API key (defaults to environment variable)
        site_url: Optional site URL for OpenRouter
        app_name: Optional app name for OpenRouter
        output_file: Optional file path to save the markdown output
        
    Returns:
        String content of the processed page (markdown)
    """
    # Set environment variables for OpenRouter
    if api_key:
        os.environ["OPENROUTER_API_KEY"] = api_key
    
    # Set optional environment variables if provided
    if site_url:
        os.environ["OR_SITE_URL"] = site_url
    
    if app_name:
        os.environ["OR_APP_NAME"] = app_name
    
    # System prompt for document-to-markdown conversion
    system_prompt = """Convert the following document to markdown.
Return only the markdown with no explanation text. Do not include delimiters like ```markdown or ```html.

RULES:
  - You must include all information on the page. Do not exclude headers, footers, or subtext.
  - Return tables in an HTML format.
  - Charts & infographics must be interpreted to a markdown format. Prefer table format when applicable.
  - Logos should be wrapped in brackets. Ex: <logo>Coca-Cola<logo>
  - Watermarks should be wrapped in brackets. Ex: <watermark>OFFICIAL COPY<watermark>
  - Page numbers should be wrapped in brackets. Ex: <page_number>14<page_number> or <page_number>9/22<page_number>
  - Prefer using ☐ and ☑ for check boxes."""
    
    # Prepare the messages
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ]
    
    # Use LiteLLM to send the request
    response = completion(
        model=model,
        messages=messages
    )
    
    # Extract the content
    markdown_content = response["choices"][0]["message"]["content"]
    
    # Save to file if output_file is provided
    if output_file:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        
        # Write content to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
    
    # Return the content
    return markdown_content
