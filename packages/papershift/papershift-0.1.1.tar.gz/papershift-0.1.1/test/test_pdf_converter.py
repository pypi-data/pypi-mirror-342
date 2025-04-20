import os
import sys
import unittest
import json
import base64
from pathlib import Path
import shutil

# Add the parent directory to the path so we can import the src module
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.pdf_converter import convert_pdf_to_images_with_target_height


class TestPDFConverter(unittest.TestCase):
    def setUp(self):
        # Create test output directory
        self.test_output_dir = os.path.join(os.path.dirname(__file__), "test_output")
        os.makedirs(self.test_output_dir, exist_ok=True)
        
        # Path to a sample PDF for testing
        # Note: You'll need to add a sample PDF to the Test directory
        self.sample_pdf_path = os.path.join(os.path.dirname(__file__), "sample.pdf")
        
        # Paths to the different sized PDFs for testing
        self.one_page_pdf = os.path.join(os.path.dirname(__file__), "1-pages.pdf")
        self.ten_page_pdf = os.path.join(os.path.dirname(__file__), "10-pages.pdf")
    
    def test_pdf_conversion(self):
        """Test that PDF conversion works if a sample PDF is available"""
        if not os.path.exists(self.sample_pdf_path):
            self.skipTest("Sample PDF not found. Add a PDF named 'sample.pdf' to the Test directory.")
        
        # Convert the PDF to images
        image_paths = convert_pdf_to_images_with_target_height(
            pdf_path=self.sample_pdf_path,
            out_dir=self.test_output_dir,
            dpi=150,  # Lower DPI for faster tests
            target_height_px=1024,  # Smaller height for faster tests
        )
        
        # Check that images were created
        self.assertTrue(len(image_paths) > 0, "No images were created")
        
        # Check that all image files exist
        for path in image_paths:
            self.assertTrue(os.path.exists(path), f"Image file {path} does not exist")
            self.assertTrue(path.endswith(".png"), f"Image file {path} is not a PNG")
    
    def test_return_base64_with_store_output(self):
        """Test returning base64 encoded images while also storing output to disk"""
        if not os.path.exists(self.one_page_pdf):
            self.skipTest("1-page PDF not found. Add a PDF named '1-pages.pdf' to the Test directory.")
        
        # Create a separate output directory for this test
        base64_output_dir = os.path.join(self.test_output_dir, "base64_with_store")
        os.makedirs(base64_output_dir, exist_ok=True)
        
        # Convert the PDF to images with base64 return and store output
        result = convert_pdf_to_images_with_target_height(
            pdf_path=self.one_page_pdf,
            out_dir=base64_output_dir,
            dpi=150,  # Lower DPI for faster tests
            target_height_px=1024,  # Smaller height for faster tests
            return_base64=True,
            store_output=True
        )
        
        # Check that the result is a dictionary with the expected keys
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertIn("order", result, "Result should contain 'order' key")
        self.assertIn("base64_images", result, "Result should contain 'base64_images' key")
        self.assertIn("file_paths", result, "Result should contain 'file_paths' key")
        
        # Check that the base64 images list is not empty
        self.assertTrue(len(result["base64_images"]) > 0, "No base64 images were returned")
        
        # Check that the order list matches the number of base64 images
        self.assertEqual(len(result["order"]), len(result["base64_images"]), 
                         "Order list length should match base64_images list length")
        
        # Check that the file_paths list matches the number of base64 images
        self.assertEqual(len(result["file_paths"]), len(result["base64_images"]), 
                         "file_paths list length should match base64_images list length")
        
        # Check that all image files exist
        for path in result["file_paths"]:
            self.assertTrue(os.path.exists(path), f"Image file {path} does not exist")
            self.assertTrue(path.endswith(".png"), f"Image file {path} is not a PNG")
        
        # Check that the base64 images have the expected structure
        for img in result["base64_images"]:
            self.assertIn("page", img, "Base64 image should contain 'page' key")
            self.assertIn("width", img, "Base64 image should contain 'width' key")
            self.assertIn("height", img, "Base64 image should contain 'height' key")
            self.assertIn("data", img, "Base64 image should contain 'data' key")
            self.assertIn("format", img, "Base64 image should contain 'format' key")
            
            # Check that the base64 data is valid
            try:
                decoded = base64.b64decode(img["data"])
                self.assertTrue(len(decoded) > 0, "Decoded base64 data should not be empty")
            except Exception as e:
                self.fail(f"Base64 data is not valid: {e}")
    
    def test_return_base64_without_store_output(self):
        """Test returning base64 encoded images without storing output to disk"""
        if not os.path.exists(self.one_page_pdf):
            self.skipTest("1-page PDF not found. Add a PDF named '1-pages.pdf' to the Test directory.")
        
        # Convert the PDF to images with base64 return and no store output
        result = convert_pdf_to_images_with_target_height(
            pdf_path=self.one_page_pdf,
            dpi=150,  # Lower DPI for faster tests
            target_height_px=1024,  # Smaller height for faster tests
            return_base64=True,
            store_output=False
        )
        
        # Check that the result is a dictionary with the expected keys
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertIn("order", result, "Result should contain 'order' key")
        self.assertIn("base64_images", result, "Result should contain 'base64_images' key")
        self.assertNotIn("file_paths", result, "Result should not contain 'file_paths' key")
        
        # Check that the base64 images list is not empty
        self.assertTrue(len(result["base64_images"]) > 0, "No base64 images were returned")
        
        # Check that the order list matches the number of base64 images
        self.assertEqual(len(result["order"]), len(result["base64_images"]), 
                         "Order list length should match base64_images list length")
        
        # Check that the base64 images have the expected structure
        for img in result["base64_images"]:
            self.assertIn("page", img, "Base64 image should contain 'page' key")
            self.assertIn("width", img, "Base64 image should contain 'width' key")
            self.assertIn("height", img, "Base64 image should contain 'height' key")
            self.assertIn("data", img, "Base64 image should contain 'data' key")
            self.assertIn("format", img, "Base64 image should contain 'format' key")
            
            # Check that the base64 data is valid
            try:
                decoded = base64.b64decode(img["data"])
                self.assertTrue(len(decoded) > 0, "Decoded base64 data should not be empty")
            except Exception as e:
                self.fail(f"Base64 data is not valid: {e}")
    
    def test_multi_page_pdf_with_base64(self):
        """Test converting a multi-page PDF with base64 return"""
        if not os.path.exists(self.ten_page_pdf):
            self.skipTest("10-page PDF not found. Add a PDF named '10-pages.pdf' to the Test directory.")
        
        # Create a separate output directory for this test
        multi_page_output_dir = os.path.join(self.test_output_dir, "multi_page")
        os.makedirs(multi_page_output_dir, exist_ok=True)
        
        # Convert the PDF to images with base64 return and store output
        result = convert_pdf_to_images_with_target_height(
            pdf_path=self.ten_page_pdf,
            out_dir=multi_page_output_dir,
            dpi=100,  # Lower DPI for faster tests
            target_height_px=800,  # Smaller height for faster tests
            return_base64=True,
            store_output=True
        )
        
        # Check that the correct number of pages were processed
        self.assertEqual(len(result["base64_images"]), 10, "Should have 10 base64 images")
        self.assertEqual(len(result["file_paths"]), 10, "Should have 10 file paths")
        self.assertEqual(len(result["order"]), 10, "Should have 10 items in order list")
        
        # Check that the order is correct (1-based indexing)
        expected_order = list(range(1, 11))
        self.assertEqual(result["order"], expected_order, "Order should be 1 through 10")
        
        # Check that all image files exist
        for path in result["file_paths"]:
            self.assertTrue(os.path.exists(path), f"Image file {path} does not exist")
    
    def test_store_output_required_with_out_dir(self):
        """Test that an error is raised when store_output=True but out_dir is not provided"""
        if not os.path.exists(self.sample_pdf_path):
            self.skipTest("Sample PDF not found. Add a PDF named 'sample.pdf' to the Test directory.")
        
        # Try to convert the PDF without providing out_dir
        with self.assertRaises(ValueError):
            convert_pdf_to_images_with_target_height(
                pdf_path=self.sample_pdf_path,
                out_dir=None,
                store_output=True
            )
    
    def test_invalid_pdf_path(self):
        """Test that an appropriate error is raised for invalid PDF paths"""
        with self.assertRaises(Exception):
            convert_pdf_to_images_with_target_height(
                pdf_path="nonexistent.pdf",
                out_dir=self.test_output_dir
            )
    
    def tearDown(self):
        # Clean up test output files if needed
        # Uncomment the following lines to clean up after tests
        # if os.path.exists(self.test_output_dir):
        #     shutil.rmtree(self.test_output_dir)
        pass


if __name__ == "__main__":
    unittest.main()
