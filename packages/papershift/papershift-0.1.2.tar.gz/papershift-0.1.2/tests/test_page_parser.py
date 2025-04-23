import os
import sys
import unittest
import base64
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile

# Add the parent directory to the path so we can import the src module
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.page_parser import process_page
from src.pdf_converter import convert_pdf_to_images_with_target_height


class TestPageParser(unittest.TestCase):
    def setUp(self):
        # Create test output directory
        self.test_output_dir = os.path.join(os.path.dirname(__file__), "test_output")
        os.makedirs(self.test_output_dir, exist_ok=True)
        
        # Path to a sample PDF for testing
        self.sample_pdf_path = os.path.join(os.path.dirname(__file__), "sample.pdf")
        
        # Skip tests if sample PDF is not available
        if not os.path.exists(self.sample_pdf_path):
            self.skipTest("Sample PDF not found. Add a PDF named 'sample.pdf' to the Test directory.")
        
        # Mock response from LiteLLM
        self.mock_response = {
            "id": "chatcmpl-123456789",
            "object": "chat.completion",
            "created": 1677858242,
            "model": "openrouter/google/gemini-2.0-flash-001",
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "# Sample Document\n\nThis is a markdown conversion of the sample document.\n\n## Section 1\n\nSample content for section 1.\n\n<page_number>1</page_number>"
                    },
                    "index": 0,
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 100,
                "completion_tokens": 50,
                "total_tokens": 150
            }
        }
        
        # Expected markdown content
        self.expected_markdown = "# Sample Document\n\nThis is a markdown conversion of the sample document.\n\n## Section 1\n\nSample content for section 1.\n\n<page_number>1</page_number>"

    @patch('src.page_parser.completion')
    def test_process_page_with_pdf_converter(self, mock_completion):
        """Test processing a page from a PDF using the PDF converter"""
        # Configure the mock to return a predefined response
        mock_completion.return_value = self.mock_response
        
        # Convert the PDF to base64 images
        pdf_output_dir = os.path.join(self.test_output_dir, "pdf_output")
        os.makedirs(pdf_output_dir, exist_ok=True)
        
        # Get base64 images from the PDF
        result = convert_pdf_to_images_with_target_height(
            pdf_path=self.sample_pdf_path,
            out_dir=pdf_output_dir,
            dpi=150,  # Lower DPI for faster tests
            target_height_px=1024,  # Smaller height for faster tests
            return_base64=True,
            store_output=True
        )
        
        # Check that we have base64 images
        self.assertIn("base64_images", result)
        self.assertTrue(len(result["base64_images"]) > 0)
        
        # Process the first page
        first_page = result["base64_images"][0]
        base64_image = first_page["data"]
        
        # Process the page using page_parser
        content = process_page(base64_image)
        
        # Verify completion was called with the correct arguments
        mock_completion.assert_called_once()
        args, kwargs = mock_completion.call_args
        
        # Check that the model is correct
        self.assertEqual(kwargs['model'], "openrouter/google/gemini-2.0-flash-001")
        
        # Check that the base64 image is included in the user message
        user_content = kwargs['messages'][1]['content']
        self.assertEqual(len(user_content), 2)
        self.assertEqual(user_content[0]['type'], "text")
        self.assertEqual(user_content[1]['type'], "image_url")
        self.assertTrue(base64_image in user_content[1]['image_url']['url'])
        
        # Check that the content is returned correctly as a string
        self.assertEqual(content, self.expected_markdown)
        self.assertIsInstance(content, str)
        self.assertTrue(len(content) > 0)
        self.assertIn("# Sample Document", content)

    @patch('src.page_parser.completion')
    def test_integration_with_custom_prompt(self, mock_completion):
        """Test integration with a custom prompt"""
        # Configure the mock to return a predefined response with table content
        table_response = {
            "id": "chatcmpl-987654321",
            "object": "chat.completion",
            "created": 1677858242,
            "model": "openrouter/google/gemini-2.0-flash-001",
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "# Data Table\n\n<table>\n<tr><th>Name</th><th>Value</th></tr>\n<tr><td>Item 1</td><td>100</td></tr>\n<tr><td>Item 2</td><td>200</td></tr>\n</table>\n\n<page_number>1</page_number>"
                    },
                    "index": 0,
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 100,
                "completion_tokens": 50,
                "total_tokens": 150
            }
        }
        mock_completion.return_value = table_response
        
        # Expected table content
        expected_table_content = "# Data Table\n\n<table>\n<tr><th>Name</th><th>Value</th></tr>\n<tr><td>Item 1</td><td>100</td></tr>\n<tr><td>Item 2</td><td>200</td></tr>\n</table>\n\n<page_number>1</page_number>"
        
        # Convert the PDF to base64 images
        pdf_output_dir = os.path.join(self.test_output_dir, "pdf_custom_output")
        os.makedirs(pdf_output_dir, exist_ok=True)
        
        # Get base64 images from the PDF
        result = convert_pdf_to_images_with_target_height(
            pdf_path=self.sample_pdf_path,
            out_dir=pdf_output_dir,
            dpi=150,
            target_height_px=1024,
            return_base64=True,
            store_output=True
        )
        
        # Process the first page with a custom prompt
        first_page = result["base64_images"][0]
        base64_image = first_page["data"]
        custom_prompt = "Extract all tables from this document and convert to HTML"
        
        # Process the page using page_parser with custom prompt
        content = process_page(
            base64_image=base64_image,
            prompt=custom_prompt
        )
        
        # Verify the custom prompt was used
        args, kwargs = mock_completion.call_args
        user_content = kwargs['messages'][1]['content']
        self.assertEqual(user_content[0]['text'], custom_prompt)
        
        # Check that we can extract the HTML table from the response
        self.assertIsInstance(content, str)
        self.assertEqual(content, expected_table_content)
        self.assertIn("<table>", content)
        self.assertIn("<tr><th>Name</th><th>Value</th></tr>", content)

    @patch('src.page_parser.completion')
    def test_process_page_with_file_output(self, mock_completion):
        """Test processing a page and saving the output to a file"""
        # Configure the mock to return a predefined response
        mock_completion.return_value = self.mock_response
        
        # Convert the PDF to base64 images
        pdf_output_dir = os.path.join(self.test_output_dir, "pdf_file_output")
        os.makedirs(pdf_output_dir, exist_ok=True)
        
        # Get base64 images from the PDF
        result = convert_pdf_to_images_with_target_height(
            pdf_path=self.sample_pdf_path,
            out_dir=pdf_output_dir,
            dpi=150,
            target_height_px=1024,
            return_base64=True,
            store_output=True
        )
        
        # Process the first page
        first_page = result["base64_images"][0]
        base64_image = first_page["data"]
        
        # Define output file path
        markdown_output_path = os.path.join(self.test_output_dir, "markdown_output", "page_1.md")
        
        # Process the page and save to file
        content = process_page(
            base64_image=base64_image,
            output_file=markdown_output_path
        )
        
        # Check that the file was created
        self.assertTrue(os.path.exists(markdown_output_path), f"Output file {markdown_output_path} not created")
        
        # Check file contents
        with open(markdown_output_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        # Verify file content matches expected content
        self.assertEqual(file_content, self.expected_markdown)
        self.assertEqual(content, file_content)


if __name__ == "__main__":
    unittest.main()
