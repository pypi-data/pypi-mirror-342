"""
Tests for the PDF to Markdown converter.

This module contains tests for the pdf_to_markdown.py module.
"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the parent directory to the path so we can import the src module
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.pdf_to_markdown import convert_pdf_to_markdown


class TestPdfToMarkdown(unittest.TestCase):
    """Test cases for the PDF to Markdown converter."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for output
        self.output_dir = os.path.join(os.path.dirname(__file__), "temp_output")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Sample PDF path (this doesn't need to exist for mocked tests)
        self.pdf_path = os.path.join(os.path.dirname(__file__), "sample.pdf")
        
        # Sample base64 data
        self.sample_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
        
        # Sample markdown content
        self.sample_markdown = "# Sample Document\n\nThis is a test document."

    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up temporary files
        if os.path.exists(self.output_dir):
            for file in os.listdir(self.output_dir):
                os.remove(os.path.join(self.output_dir, file))
            os.rmdir(self.output_dir)

    @patch('src.pdf_to_markdown.convert_pdf_to_images_with_target_height')
    @patch('src.pdf_to_markdown.process_page')
    def test_convert_pdf_to_markdown_basic(self, mock_process_page, mock_convert_pdf):
        """Test basic PDF to markdown conversion with mocked dependencies."""
        # Mock the PDF converter
        mock_convert_pdf.return_value = {
            "order": [1],
            "base64_images": [
                {
                    "page": 1,
                    "width": 100,
                    "height": 100,
                    "data": self.sample_base64,
                    "format": "png"
                }
            ]
        }
        
        # Mock the page parser
        mock_process_page.return_value = self.sample_markdown
        
        # Call the function
        result = convert_pdf_to_markdown(
            pdf_path=self.pdf_path,
            output_dir=self.output_dir,
            verbose=True
        )
        
        # Check the result
        self.assertEqual(result, "## Page 1\n\n" + self.sample_markdown)
        
        # Check if the file was created
        combined_file = os.path.join(self.output_dir, "combined.md")
        self.assertTrue(os.path.exists(combined_file))
        
        # Check the file content
        with open(combined_file, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertEqual(content, "## Page 1\n\n" + self.sample_markdown)
        
        # Verify the mocks were called correctly
        mock_convert_pdf.assert_called_once()
        mock_process_page.assert_called_once_with(
            base64_image=self.sample_base64,
            prompt="Convert this document to markdown",
            model="openrouter/google/gemini-2.0-flash-001",
            api_key=None,
            site_url=None,
            app_name=None,
            output_file=os.path.join(self.output_dir, "page_001.md")
        )

    @patch('src.pdf_to_markdown.convert_pdf_to_images_with_target_height')
    @patch('src.pdf_to_markdown.process_page')
    def test_convert_pdf_to_markdown_multiple_pages(self, mock_process_page, mock_convert_pdf):
        """Test PDF to markdown conversion with multiple pages."""
        # Mock the PDF converter
        mock_convert_pdf.return_value = {
            "order": [1, 2, 3],
            "base64_images": [
                {
                    "page": 1,
                    "width": 100,
                    "height": 100,
                    "data": self.sample_base64,
                    "format": "png"
                },
                {
                    "page": 2,
                    "width": 100,
                    "height": 100,
                    "data": self.sample_base64,
                    "format": "png"
                },
                {
                    "page": 3,
                    "width": 100,
                    "height": 100,
                    "data": self.sample_base64,
                    "format": "png"
                }
            ]
        }
        
        # Mock the page parser with different content for each page
        mock_process_page.side_effect = [
            "# Page 1 Content",
            "# Page 2 Content",
            "# Page 3 Content"
        ]
        
        # Call the function
        result = convert_pdf_to_markdown(
            pdf_path=self.pdf_path,
            output_dir=self.output_dir,
            verbose=True
        )
        
        # Check the result
        expected_result = "\n\n---\n\n".join([
            "## Page 1\n\n# Page 1 Content",
            "## Page 2\n\n# Page 2 Content",
            "## Page 3\n\n# Page 3 Content"
        ])
        self.assertEqual(result, expected_result)
        
        # Check if the combined file was created
        combined_file = os.path.join(self.output_dir, "combined.md")
        self.assertTrue(os.path.exists(combined_file))
        
        # Check the file content
        with open(combined_file, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertEqual(content, expected_result)
        
        # Check if individual page files were created
        for i in range(1, 4):
            page_file = os.path.join(self.output_dir, f"page_{i:03d}.md")
            self.assertTrue(os.path.exists(page_file))
        
        # Verify the mock was called correctly
        self.assertEqual(mock_process_page.call_count, 3)

    @patch('src.pdf_to_markdown.convert_pdf_to_images_with_target_height')
    @patch('src.pdf_to_markdown.process_page')
    def test_convert_pdf_to_markdown_separate_pages(self, mock_process_page, mock_convert_pdf):
        """Test PDF to markdown conversion with separate page output."""
        # Mock the PDF converter
        mock_convert_pdf.return_value = {
            "order": [1, 2],
            "base64_images": [
                {
                    "page": 1,
                    "width": 100,
                    "height": 100,
                    "data": self.sample_base64,
                    "format": "png"
                },
                {
                    "page": 2,
                    "width": 100,
                    "height": 100,
                    "data": self.sample_base64,
                    "format": "png"
                }
            ]
        }
        
        # Mock the page parser
        mock_process_page.side_effect = ["# Page 1 Content", "# Page 2 Content"]
        
        # Call the function with combined_output=False
        result = convert_pdf_to_markdown(
            pdf_path=self.pdf_path,
            output_dir=self.output_dir,
            combined_output=False,
            verbose=True
        )
        
        # Check the result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "## Page 1\n\n# Page 1 Content")
        self.assertEqual(result[1], "## Page 2\n\n# Page 2 Content")
        
        # Check if individual page files were created
        for i in range(1, 3):
            page_file = os.path.join(self.output_dir, f"page_{i:03d}.md")
            self.assertTrue(os.path.exists(page_file))
        
        # Verify the mock was called correctly
        self.assertEqual(mock_process_page.call_count, 2)

    @patch('os.path.exists')
    def test_file_not_found_error(self, mock_exists):
        """Test that FileNotFoundError is raised when PDF file doesn't exist."""
        # Mock os.path.exists to return False
        mock_exists.return_value = False
        
        # Check that FileNotFoundError is raised
        with self.assertRaises(FileNotFoundError):
            convert_pdf_to_markdown(pdf_path="nonexistent.pdf")

    @patch('src.pdf_to_markdown.convert_pdf_to_images_with_target_height')
    def test_empty_pdf(self, mock_convert_pdf):
        """Test handling of an empty PDF (no pages)."""
        # Mock the PDF converter to return empty result
        mock_convert_pdf.return_value = {
            "order": [],
            "base64_images": []
        }
        
        # Call the function
        result = convert_pdf_to_markdown(
            pdf_path=self.pdf_path,
            output_dir=self.output_dir,
            verbose=True
        )
        
        # Check the result
        self.assertEqual(result, "")
        
        # Check if the combined file was created (should be empty)
        combined_file = os.path.join(self.output_dir, "combined.md")
        self.assertTrue(os.path.exists(combined_file))
        
        # Check the file content (should be empty)
        with open(combined_file, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertEqual(content, "")


if __name__ == "__main__":
    unittest.main()
