"""
PaperShift: PDF and Image to Markdown Converter

A library for converting PDF documents and images to Markdown format using AI assistance.
"""

from .pdf_to_markdown import convert_pdf_to_markdown
from .image_to_markdown import convert_image_to_markdown, convert_images_to_markdown

__version__ = "0.1.2"
__all__ = ["convert_pdf_to_markdown", "convert_image_to_markdown", "convert_images_to_markdown"]
