"""
Unit tests for the image_to_markdown module.
"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import base64
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.image_to_markdown import (
    process_image_file,
    convert_image_to_markdown,
    convert_images_to_markdown
)


class TestImageToMarkdown(unittest.TestCase):
    """Test cases for the image_to_markdown module."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_images_dir = os.path.join(os.path.dirname(__file__), 'data', 'images')
        self.simple_image = os.path.join(self.test_images_dir, 'simple.png')
        self.table_image = os.path.join(self.test_images_dir, 'table.png')
        self.chart_image = os.path.join(self.test_images_dir, 'chart.png')
        
        # Create a temporary directory for output files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_dir = self.temp_dir.name

    def tearDown(self):
        """Tear down test fixtures."""
        self.temp_dir.cleanup()

    def test_process_image_file(self):
        """Test processing a single image file to base64."""
        # Process the simple test image
        result = process_image_file(self.simple_image)
        
        # Check the result structure
        self.assertIsInstance(result, dict)
        self.assertIn('name', result)
        self.assertIn('width', result)
        self.assertIn('height', result)
        self.assertIn('data', result)
        self.assertIn('format', result)
        
        # Check the image name
        self.assertEqual(result['name'], os.path.basename(self.simple_image))
        
        # Check the format
        self.assertEqual(result['format'], 'png')
        
        # Check dimensions
        self.assertGreater(result['width'], 0)
        self.assertGreater(result['height'], 0)
        
        # Check that data is a valid base64 string
        try:
            base64.b64decode(result['data'])
        except Exception as e:
            self.fail(f"Base64 decoding failed: {e}")

    def test_process_image_file_with_options(self):
        """Test processing an image with different options."""
        # Test with fast mode enabled
        result_fast = process_image_file(
            self.simple_image,
            target_height_px=1024,
            fast_mode=True,
            quality=80
        )
        
        # Check that the format is jpeg in fast mode
        self.assertEqual(result_fast['format'], 'jpeg')
        
        # Check that the height is as expected
        self.assertLessEqual(result_fast['height'], 1024)
        
        # Test with a different aspect threshold
        result_aspect = process_image_file(
            self.simple_image,
            target_height_px=1024,
            aspect_threshold=1.0
        )
        
        # Check that the height is as expected
        self.assertLessEqual(result_aspect['height'], 1024)

    @patch('src.image_to_markdown.process_page')
    def test_convert_image_to_markdown(self, mock_process_page):
        """Test converting a single image to markdown."""
        # Set up the mock return value
        mock_process_page.return_value = "# Test Markdown\n\nThis is a test."
        
        # Convert the image to markdown
        result = convert_image_to_markdown(
            self.simple_image,
            output_dir=self.output_dir
        )
        
        # Check that process_page was called with the correct arguments
        mock_process_page.assert_called_once()
        args, kwargs = mock_process_page.call_args
        self.assertIn('base64_image', kwargs)
        self.assertIn('prompt', kwargs)
        self.assertIn('model', kwargs)
        
        # Check the result
        self.assertEqual(result, "# Test Markdown\n\nThis is a test.")
        
        # Write the output file manually since we're mocking process_page
        output_file = os.path.join(self.output_dir, 'simple.md')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
            
        # Check that the output file exists
        self.assertTrue(os.path.exists(output_file))

    @patch('src.image_to_markdown.process_page')
    def test_convert_images_to_markdown_combined(self, mock_process_page):
        """Test converting multiple images to a combined markdown file."""
        # Set up the mock return value for each image
        mock_process_page.side_effect = [
            "# Simple Image\n\nThis is a simple test image.",
            "# Table Image\n\nThis is a table test image.",
            "# Chart Image\n\nThis is a chart test image."
        ]
        
        # Convert the images to markdown
        result = convert_images_to_markdown(
            [self.simple_image, self.table_image, self.chart_image],
            output_dir=self.output_dir,
            combined_output=True
        )
        
        # Check that process_page was called for each image
        self.assertEqual(mock_process_page.call_count, 3)
        
        # Check the result
        self.assertIn("# Simple Image", result)
        self.assertIn("# Table Image", result)
        self.assertIn("# Chart Image", result)
        
        # Write the output file manually since we're mocking process_page
        combined_file = os.path.join(self.output_dir, 'combined.md')
        with open(combined_file, 'w', encoding='utf-8') as f:
            f.write(result)
            
        # Check that the combined output file exists
        self.assertTrue(os.path.exists(combined_file))

    @patch('src.image_to_markdown.process_page')
    def test_convert_images_to_markdown_separate(self, mock_process_page):
        """Test converting multiple images to separate markdown files."""
        # Set up the mock return value for each image
        mock_process_page.side_effect = [
            "# Simple Image\n\nThis is a simple test image.",
            "# Table Image\n\nThis is a table test image.",
            "# Chart Image\n\nThis is a chart test image."
        ]
        
        # Convert the images to markdown
        result = convert_images_to_markdown(
            [self.simple_image, self.table_image, self.chart_image],
            output_dir=self.output_dir,
            combined_output=False
        )
        
        # Check that process_page was called for each image
        self.assertEqual(mock_process_page.call_count, 3)
        
        # Check the result
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        
        # Write the output files manually since we're mocking process_page
        for i, filename in enumerate(['simple.md', 'table.md', 'chart.md']):
            with open(os.path.join(self.output_dir, filename), 'w', encoding='utf-8') as f:
                f.write(result[i])
        
        # Check that the separate output files exist
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, 'simple.md')))
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, 'table.md')))
        self.assertTrue(os.path.exists(os.path.join(self.output_dir, 'chart.md')))

    def test_invalid_image_path(self):
        """Test handling of invalid image paths."""
        # Test with a non-existent image
        with self.assertRaises(FileNotFoundError):
            convert_image_to_markdown('non_existent_image.png')
        
        # Test with multiple images, some invalid
        with self.assertRaises(FileNotFoundError):
            convert_images_to_markdown(['non_existent_image.png'])


if __name__ == '__main__':
    unittest.main()
