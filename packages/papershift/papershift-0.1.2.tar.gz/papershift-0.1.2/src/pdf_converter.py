import fitz  # pip install PyMuPDF
import os
import base64
import time
from typing import List, Dict, Union, Tuple, Optional, Any
import concurrent.futures
import gc

def process_page(
    args: Tuple[Any, ...]
) -> Tuple[Optional[str], Optional[Dict]]:
    """
    Process a single PDF page to convert it to an image.
    
    Args:
        args: Tuple containing (pdf_path, page_num, out_dir, dpi, target_height_px, 
              aspect_threshold, return_base64, store_output, quality, fast_mode)
    
    Returns:
        Tuple of (image_path, base64_image_dict)
    """
    pdf_path, page_num, out_dir, dpi, target_height_px, aspect_threshold, return_base64, store_output, quality, fast_mode = args
    
    start_time = time.time()
    
    # Open the PDF and get the specific page - this avoids pickling issues
    doc = fitz.open(pdf_path)
    page = doc[page_num - 1]  # Convert from 1-based to 0-based indexing
    
    # page.rect is in points (1pt = 1/72")
    w_pt, h_pt = page.rect.width, page.rect.height
    ar = h_pt / w_pt

    # decide final pixel‐height
    h_px = (
        max(target_height_px, int(ar * target_height_px))
        if ar > aspect_threshold
        else target_height_px
    )
    
    # In fast mode, reduce resolution for base64 images
    if fast_mode and return_base64:
        h_px = min(h_px, 1024)  # Limit height to 1024px for base64 in fast mode
    
    # zoom = px / pt  →  px = pt * zoom
    zoom = h_px / h_pt

    # but also factor in desired DPI: zoom_dpi = dpi/72
    # you can multiply them together if you want both effects:
    zoom_total = zoom * (dpi / 72)

    mat = fitz.Matrix(zoom_total, zoom_total)
    
    # Use lower DPI for base64 images in fast mode
    if fast_mode and return_base64 and not store_output:
        # If we're only returning base64 (not storing), use a lower resolution matrix
        mat = fitz.Matrix(zoom_total * 0.75, zoom_total * 0.75)
    
    pix = page.get_pixmap(matrix=mat, alpha=False)
    
    image_path = None
    base64_image = None
    
    if store_output:
        out_path = os.path.join(out_dir, f"page_{page_num:03}.png")
        pix.save(out_path, quality=quality)
        image_path = out_path
        
    if return_base64:
        # Convert pixmap to base64
        if fast_mode:
            # Use JPEG format with quality setting for base64 in fast mode (smaller size)
            img_bytes = pix.tobytes("jpeg", quality=quality)
            img_format = "jpeg"
        else:
            # Use PNG format for better quality in normal mode
            img_bytes = pix.tobytes()
            img_format = "png"
            
        img_b64 = base64.b64encode(img_bytes).decode('utf-8')
        base64_image = {
            "page": page_num,
            "width": pix.width,
            "height": pix.height,
            "data": img_b64,
            "format": img_format
        }
    
    # Free up memory
    pix = None
    doc.close()
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    return image_path, base64_image, processing_time

def convert_pdf_to_images_with_target_height(
    pdf_path: str,
    out_dir: str = None,
    dpi: int = 300,
    target_height_px: int = 2048,
    aspect_threshold: float = 1.5,  # e.g. only bump if height/width > threshold
    return_base64: bool = False,
    store_output: bool = True,
    max_workers: int = 4,
    batch_size: int = 5,
    quality: int = 95,
    fast_mode: bool = False
) -> Union[List[str], Dict[str, Union[List[str], List[Dict[str, str]]]]]:
    """
    Renders each page of pdf_path to a PNG, at `dpi` for crispness,
    then scales its height to at least `target_height_px` (if very tall),
    preserving aspect ratio.
    
    Args:
        pdf_path: Path to the PDF file
        out_dir: Directory to save the output images (required if store_output=True)
        dpi: DPI for image rendering
        target_height_px: Target height in pixels
        aspect_threshold: Aspect ratio threshold for height adjustment
        return_base64: If True, returns base64 encoded images in the result
        store_output: If True, saves images to disk at out_dir
        max_workers: Maximum number of worker threads to use for parallelization
        batch_size: Number of pages to process in a single batch
        quality: Image quality (1-100, only affects JPEG in fast mode)
        fast_mode: If True, uses lower resolution and JPEG format for base64 images
        
    Returns:
        If return_base64=False and store_output=True: List of image file paths
        If return_base64=True: Dict with 'file_paths' (if store_output=True) and 'base64_images' keys
    """
    if store_output and not out_dir:
        raise ValueError("out_dir must be provided when store_output=True")
    
    if store_output:
        os.makedirs(out_dir, exist_ok=True)
    
    # Open the PDF just to get the page count
    with fitz.open(pdf_path) as doc:
        num_pages = len(doc)
    
    # Adjust settings for fast mode
    if fast_mode:
        print(f"Running in fast mode with reduced quality ({quality}%)")
        if dpi > 150 and return_base64:
            dpi = 150
            print(f"Reduced DPI to {dpi} for fast mode")
    
    print(f"PDF has {num_pages} pages. Processing in batches of {batch_size} with {max_workers} workers...")
    
    image_paths = []
    base64_images = []
    page_order = []
    total_time = 0
    
    # Calculate total batches for progress reporting
    total_batches = (num_pages + batch_size - 1) // batch_size
    
    # Process pages in batches to control memory usage
    for batch_idx, batch_start in enumerate(range(0, num_pages, batch_size)):
        batch_end = min(batch_start + batch_size, num_pages)
        batch_start_time = time.time()
        
        print(f"Processing batch {batch_idx+1}/{total_batches}: pages {batch_start+1}-{batch_end} of {num_pages}")
        
        # Prepare batch of pages - pass page numbers instead of page objects
        batch_args = []
        for i in range(batch_start, batch_end):
            page_num = i + 1  # 1-based page numbering
            batch_args.append((pdf_path, page_num, out_dir, dpi, target_height_px, 
                             aspect_threshold, return_base64, store_output, quality, fast_mode))
        
        # Process batch in parallel using ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(process_page, batch_args))
        
        # Collect results from this batch
        batch_times = []
        for page_num, (image_path, base64_image, proc_time) in zip(range(batch_start+1, batch_end+1), results):
            if image_path:
                image_paths.append(image_path)
            if base64_image:
                base64_images.append(base64_image)
                page_order.append(page_num)
            batch_times.append(proc_time)
        
        # Report batch performance
        batch_end_time = time.time()
        batch_total_time = batch_end_time - batch_start_time
        total_time += batch_total_time
        
        avg_page_time = sum(batch_times) / len(batch_times)
        pages_per_second = len(batch_times) / batch_total_time
        
        print(f"  Batch {batch_idx+1} completed in {batch_total_time:.2f}s ({avg_page_time:.2f}s/page, {pages_per_second:.2f} pages/s)")
        
        # Estimate remaining time
        if batch_idx < total_batches - 1:
            remaining_batches = total_batches - (batch_idx + 1)
            est_remaining_time = remaining_batches * batch_total_time
            print(f"  Estimated remaining time: {est_remaining_time:.2f}s ({est_remaining_time/60:.1f}m)")
        
        # Force garbage collection after each batch
        gc.collect()
    
    avg_time_per_page = total_time / num_pages
    pages_per_second = num_pages / total_time
    
    print(f"Finished processing all {num_pages} pages in {total_time:.2f}s")
    print(f"Average: {avg_time_per_page:.2f}s per page, {pages_per_second:.2f} pages per second")
    
    # Return results based on flags
    if return_base64:
        result = {"order": page_order, "base64_images": base64_images}
        if store_output:
            result["file_paths"] = image_paths
        return result
    else:
        return image_paths
