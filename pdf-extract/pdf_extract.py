# /// script
# dependencies = ["pymupdf4llm", "pymupdf", "pytesseract", "pillow"]
# ///

"""
PDF Extract - Extract text from PDFs including large/image-based documents.

Usage:
    uv run pdf_extract.py <pdf-path-or-url> [output-path]

Examples:
    uv run pdf_extract.py /tmp/salary_guide.pdf
    uv run pdf_extract.py https://example.com/report.pdf /tmp/output.md
"""

import sys
import os
import pymupdf4llm
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import tempfile
import urllib.request


def download_if_url(source):
    """Download PDF if source is a URL, return local path."""
    if source.startswith(('http://', 'https://')):
        print(f"Downloading from URL...")
        # Extract filename from URL, handle query params
        filename = os.path.basename(source.split('?')[0]) or 'document.pdf'
        # URL decode common patterns
        filename = urllib.parse.unquote(filename) if '%' in filename else filename
        if not filename.endswith('.pdf'):
            filename += '.pdf'
        local_path = os.path.join(tempfile.gettempdir(), filename)
        urllib.request.urlretrieve(source, local_path)
        print(f"Downloaded to: {local_path}")
        return local_path
    return source


def extract_with_pymupdf4llm(pdf_path):
    """Try fast extraction with pymupdf4llm."""
    try:
        md_text = pymupdf4llm.to_markdown(pdf_path)
        return md_text
    except Exception as e:
        print(f"pymupdf4llm failed: {e}")
        return None


def extract_with_ocr(pdf_path):
    """Fall back to OCR for image-based PDFs."""
    print("Falling back to OCR extraction...")
    doc = fitz.open(pdf_path)
    full_text = []
    total_pages = len(doc)

    print(f"Processing {total_pages} pages with OCR...")

    for page_num in range(total_pages):
        page = doc[page_num]
        # Render page to image at 2x zoom for better OCR
        mat = fitz.Matrix(2, 2)
        pix = page.get_pixmap(matrix=mat)
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))

        # OCR the image
        text = pytesseract.image_to_string(img)
        full_text.append(f"--- Page {page_num + 1} ---\n{text}")

        # Progress indicator
        if (page_num + 1) % 10 == 0 or page_num + 1 == total_pages:
            print(f"  Processed {page_num + 1}/{total_pages} pages...")

    doc.close()
    return "\n\n".join(full_text)


def is_extraction_valid(text, min_chars=500):
    """Check if extraction produced meaningful content."""
    if not text:
        return False
    # Remove whitespace and check length
    cleaned = ''.join(text.split())
    return len(cleaned) > min_chars


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run pdf_extract.py <pdf-path-or-url> [output-path]")
        print("\nExamples:")
        print("  uv run pdf_extract.py /tmp/salary_guide.pdf")
        print("  uv run pdf_extract.py https://example.com/report.pdf")
        print("  uv run pdf_extract.py document.pdf /tmp/output.md")
        sys.exit(1)

    source = sys.argv[1]

    # Download if URL
    pdf_path = download_if_url(source)

    if not os.path.exists(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)

    # Get file size for info
    file_size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
    print(f"File size: {file_size_mb:.1f} MB")

    # Determine output path
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    # Clean up filename for output
    base_name = base_name.replace('%20', '_').replace(' ', '_')
    output_path = sys.argv[2] if len(sys.argv) > 2 else f"/tmp/{base_name}.md"

    print(f"Extracting: {pdf_path}")
    print(f"Output: {output_path}")

    # Try pymupdf4llm first
    print("\nTrying pymupdf4llm extraction...")
    text = extract_with_pymupdf4llm(pdf_path)

    # Check if extraction worked
    if not is_extraction_valid(text):
        print("Text extraction insufficient, PDF likely image-based.")
        text = extract_with_ocr(pdf_path)
    else:
        print("pymupdf4llm extraction successful.")

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"\n✓ Done! Output written to: {output_path}")
    print(f"  Total characters: {len(text):,}")

    # Preview first 500 chars
    preview = text[:500].replace('\n', ' ')[:200]
    print(f"  Preview: {preview}...")


if __name__ == "__main__":
    main()
