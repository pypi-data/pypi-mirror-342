"""
Image to Markdown Converter

This module provides functionality to convert image files to markdown format.
It uses the page_parser to convert each image to markdown.
"""
import os
import sys
import argparse
from typing import List, Dict, Optional, Union
import json
import base64
from PIL import Image
import io
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .page_parser import process_page


def process_image_file(
    image_path: str,
    target_height_px: int = 2048,
    aspect_threshold: float = 1.5,
    quality: int = 95,
    fast_mode: bool = False
) -> Dict:
    """
    Process a single image file and convert it to base64.
    
    Args:
        image_path: Path to the image file
        target_height_px: Target height in pixels
        aspect_threshold: Aspect ratio threshold for height adjustment
        quality: Image quality (1-100) for JPEG compression
        fast_mode: If True, uses reduced resolution for faster processing
        
    Returns:
        Dictionary containing the base64 encoded image and metadata
    """
    # Open the image file
    img = Image.open(image_path)
    
    # Get original dimensions
    w, h = img.size
    ar = h / w
    
    # Decide final pixel-height
    h_px = (
        max(target_height_px, int(ar * target_height_px))
        if ar > aspect_threshold
        else target_height_px
    )
    
    # In fast mode, reduce resolution
    if fast_mode:
        h_px = min(h_px, 1024)  # Limit height to 1024px in fast mode
    
    # Calculate new width to maintain aspect ratio
    w_px = int(h_px / ar)
    
    # Resize image
    img = img.resize((w_px, h_px), Image.LANCZOS)
    
    # Convert to base64
    buffer = io.BytesIO()
    
    # Use JPEG format with quality setting for fast mode (smaller size)
    if fast_mode:
        if img.mode == 'RGBA':
            # Convert RGBA to RGB for JPEG
            img = img.convert('RGB')
        img.save(buffer, format="JPEG", quality=quality)
        img_format = "jpeg"
    else:
        # Use PNG format for better quality in normal mode
        img.save(buffer, format="PNG")
        img_format = "png"
    
    img_bytes = buffer.getvalue()
    img_b64 = base64.b64encode(img_bytes).decode('utf-8')
    
    # Get file name without extension
    file_name = os.path.basename(image_path)
    
    return {
        "name": file_name,
        "width": w_px,
        "height": h_px,
        "data": img_b64,
        "format": img_format
    }


def convert_image_to_markdown(
    image_path: str,
    output_dir: Optional[str] = None,
    target_height_px: int = 2048,
    aspect_threshold: float = 1.5,
    prompt: str = "Convert this image to markdown",
    model: str = "openrouter/google/gemini-2.0-flash-001",
    api_key: Optional[str] = None,
    site_url: Optional[str] = None,
    app_name: Optional[str] = None,
    verbose: bool = False,
    quality: int = 95,
    fast_mode: bool = False
) -> str:
    """
    Convert a single image file to markdown format.
    
    Args:
        image_path: Path to the image file
        output_dir: Directory to save the output markdown file (if None, no file is saved)
        target_height_px: Target height in pixels
        aspect_threshold: Aspect ratio threshold for height adjustment
        prompt: Text prompt to send with the image
        model: The model to use for processing
        api_key: OpenRouter API key (defaults to environment variable)
        site_url: Optional site URL for OpenRouter
        app_name: Optional app name for OpenRouter
        verbose: If True, prints progress information
        quality: Image quality (1-100) for JPEG compression in fast mode
        fast_mode: If True, uses reduced resolution and JPEG format for faster processing
        
    Returns:
        String containing the markdown content
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    print(f"Starting image to markdown conversion for: {image_path}")
    print(f"Using model: {model}")
    
    if verbose:
        print(f"Target height: {target_height_px}px")
        print(f"Aspect threshold: {aspect_threshold}")
        if fast_mode:
            print(f"Fast mode: Enabled (quality: {quality}%)")
    
    print(f"Step 1/3: Converting image to base64...")
    
    # Process the image
    base64_image = process_image_file(
        image_path=image_path,
        target_height_px=target_height_px,
        aspect_threshold=aspect_threshold,
        quality=quality,
        fast_mode=fast_mode
    )
    
    print(f"Step 1/3 completed: Successfully converted image to base64")
    print(f"Step 2/3: Processing image to markdown...")
    
    # Create output file path if output_dir is provided
    output_file = None
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        # Use the original filename but with .md extension
        base_name = Path(base64_image["name"]).stem
        output_file = os.path.join(output_dir, f"{base_name}.md")
    
    # Process the image
    print(f"  Sending image to model for processing...")
    markdown_content = process_page(
        base64_image=base64_image["data"],
        prompt=prompt,
        model=model,
        api_key=api_key,
        site_url=site_url,
        app_name=app_name,
        output_file=output_file
    )
    print(f"  Image processing complete")
    
    if output_file:
        print(f"  Saved markdown to {output_file}")
    
    print(f"Step 2/3 completed: Image processed")
    print(f"Step 3/3: Finalizing output...")
    print(f"Step 3/3 completed: Markdown conversion finished successfully")
    
    return markdown_content


def convert_images_to_markdown(
    image_paths: List[str],
    output_dir: Optional[str] = None,
    target_height_px: int = 2048,
    aspect_threshold: float = 1.5,
    prompt: str = "Convert this image to markdown",
    model: str = "openrouter/google/gemini-2.0-flash-001",
    api_key: Optional[str] = None,
    site_url: Optional[str] = None,
    app_name: Optional[str] = None,
    combined_output: bool = True,
    verbose: bool = False,
    max_workers: int = 4,
    quality: int = 95,
    fast_mode: bool = False
) -> Union[str, List[str]]:
    """
    Convert multiple image files to markdown format.
    
    Args:
        image_paths: List of paths to image files
        output_dir: Directory to save the output markdown files (if None, no files are saved)
        target_height_px: Target height in pixels
        aspect_threshold: Aspect ratio threshold for height adjustment
        prompt: Text prompt to send with each image
        model: The model to use for processing
        api_key: OpenRouter API key (defaults to environment variable)
        site_url: Optional site URL for OpenRouter
        app_name: Optional app name for OpenRouter
        combined_output: If True, returns a single string with all images combined
        verbose: If True, prints progress information
        max_workers: Maximum number of worker processes
        quality: Image quality (1-100) for JPEG compression in fast mode
        fast_mode: If True, uses reduced resolution and JPEG format for faster processing
        
    Returns:
        If combined_output=True: A single string containing all markdown content
        If combined_output=False: A list of strings, each containing markdown for one image
    """
    # Validate image paths
    valid_image_paths = []
    for path in image_paths:
        if not os.path.exists(path):
            print(f"Warning: Image file not found: {path}")
        else:
            valid_image_paths.append(path)
    
    if not valid_image_paths:
        raise FileNotFoundError("No valid image files found")
    
    print(f"Starting image to markdown conversion for {len(valid_image_paths)} images")
    print(f"Using model: {model}")
    
    if verbose:
        print(f"Target height: {target_height_px}px")
        print(f"Aspect threshold: {aspect_threshold}")
        print(f"Parallel processing: {max_workers} workers")
        if fast_mode:
            print(f"Fast mode: Enabled (quality: {quality}%)")
    
    print(f"Step 1/3: Converting images to base64...")
    
    # Process images in parallel
    base64_images = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for image_path in valid_image_paths:
            futures.append(
                executor.submit(
                    process_image_file,
                    image_path=image_path,
                    target_height_px=target_height_px,
                    aspect_threshold=aspect_threshold,
                    quality=quality,
                    fast_mode=fast_mode
                )
            )
        
        # Collect results
        for future in futures:
            base64_images.append(future.result())
    
    print(f"Step 1/3 completed: Successfully converted {len(base64_images)} images to base64")
    print(f"Step 2/3: Processing {len(base64_images)} images to markdown...")
    
    # Process each image to markdown
    markdown_contents = []
    image_order = []
    
    for i, image_data in enumerate(base64_images):
        print(f"  Processing image {i+1}/{len(base64_images)}...")
        
        # Create output file path if output_dir is provided
        output_file = None
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            # Use the original filename but with .md extension
            base_name = Path(image_data["name"]).stem
            output_file = os.path.join(output_dir, f"{base_name}.md")
        
        # Process the image
        print(f"  Sending image {i+1} to model for processing...")
        markdown_content = process_page(
            base64_image=image_data["data"],
            prompt=prompt,
            model=model,
            api_key=api_key,
            site_url=site_url,
            app_name=app_name,
            output_file=output_file
        )
        print(f"  Image {i+1} processing complete")
        
        # Add image name as a header if there are multiple images
        if len(base64_images) > 1:
            image_name = Path(image_data["name"]).stem
            markdown_content = f"## Image: {image_name}\n\n{markdown_content}"
        
        markdown_contents.append(markdown_content)
        image_order.append(i+1)
        
        if output_file:
            print(f"  Saved markdown for image {i+1} to {output_file}")
    
    print(f"Step 2/3 completed: All {len(base64_images)} images processed")
    print(f"Step 3/3: Finalizing output...")
    
    # Create combined output if requested
    if combined_output:
        print(f"  Combining {len(markdown_contents)} markdown contents...")
        combined_markdown = "\n\n---\n\n".join(markdown_contents)
        
        # Save combined output if output_dir is provided
        if output_dir:
            combined_file = os.path.join(output_dir, "combined.md")
            with open(combined_file, 'w', encoding='utf-8') as f:
                f.write(combined_markdown)
            
            print(f"  Saved combined markdown to {combined_file}")
        
        print(f"Step 3/3 completed: Markdown conversion finished successfully")
        return combined_markdown
    else:
        print(f"Step 3/3 completed: Generated {len(markdown_contents)} separate markdown files")
        return markdown_contents


if __name__ == "__main__":
    # Command line interface
    parser = argparse.ArgumentParser(description="Convert image files to markdown")
    parser.add_argument("image_paths", nargs="+", help="Paths to image files")
    parser.add_argument("--output-dir", "-o", help="Directory to save output markdown files")
    parser.add_argument("--target-height", type=int, default=2048, help="Target height in pixels")
    parser.add_argument("--aspect-threshold", type=float, default=1.5, help="Aspect ratio threshold")
    parser.add_argument("--prompt", default="Convert this image to markdown", help="Prompt for the model")
    parser.add_argument("--model", default="openrouter/google/gemini-2.0-flash-001", help="Model to use")
    parser.add_argument("--api-key", help="OpenRouter API key")
    parser.add_argument("--site-url", help="Site URL for OpenRouter")
    parser.add_argument("--app-name", help="App name for OpenRouter")
    parser.add_argument("--separate", action="store_true", help="Generate separate markdown files")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print verbose output")
    parser.add_argument("--max-workers", type=int, default=4, help="Maximum number of worker processes")
    parser.add_argument("--quality", type=int, default=95, help="Image quality (1-100)")
    parser.add_argument("--fast", action="store_true", help="Use fast mode with reduced quality")
    
    args = parser.parse_args()
    
    # Check if single or multiple images
    if len(args.image_paths) == 1:
        # Single image
        result = convert_image_to_markdown(
            image_path=args.image_paths[0],
            output_dir=args.output_dir,
            target_height_px=args.target_height,
            aspect_threshold=args.aspect_threshold,
            prompt=args.prompt,
            model=args.model,
            api_key=args.api_key,
            site_url=args.site_url,
            app_name=args.app_name,
            verbose=args.verbose,
            quality=args.quality,
            fast_mode=args.fast
        )
        
        # If no output directory is specified, print the result to stdout
        if not args.output_dir:
            print(result)
    else:
        # Multiple images
        result = convert_images_to_markdown(
            image_paths=args.image_paths,
            output_dir=args.output_dir,
            target_height_px=args.target_height,
            aspect_threshold=args.aspect_threshold,
            prompt=args.prompt,
            model=args.model,
            api_key=args.api_key,
            site_url=args.site_url,
            app_name=args.app_name,
            combined_output=not args.separate,
            verbose=args.verbose,
            max_workers=args.max_workers,
            quality=args.quality,
            fast_mode=args.fast
        )
        
        # If no output directory is specified, print the result to stdout
        if not args.output_dir:
            if isinstance(result, list):
                for i, markdown in enumerate(result):
                    print(f"\n--- Image {i+1} ---\n")
                    print(markdown)
            else:
                print(result)
