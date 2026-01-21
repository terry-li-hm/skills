# PDF Extract

Extract text from PDFs, including large and image-based (scanned) documents.

## When to Use

- PDF too large to read directly (>20MB)
- Image-based/scanned PDFs that need OCR
- Salary guides, reports, research papers
- Any PDF where standard tools fail

## Usage

```
/pdf-extract <path-or-url>
```

Examples:
```
/pdf-extract /tmp/salary_guide.pdf
/pdf-extract https://example.com/report.pdf
```

## How It Works

1. **Try pymupdf4llm first** — fast, produces clean markdown
2. **Check if extraction worked** — if empty or very short, PDF is likely image-based
3. **Fall back to OCR** — use PyMuPDF to render pages as images, then pytesseract for OCR
4. **Output to file** — saves to `/tmp/<filename>.md` or specified output path

## Implementation

Run this Python script with `uv run`:

```python
# /// script
# dependencies = ["pymupdf4llm", "pymupdf", "pytesseract", "pillow"]
# ///

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
        filename = os.path.basename(source.split('?')[0]) or 'document.pdf'
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

    for page_num in range(len(doc)):
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
        if (page_num + 1) % 10 == 0:
            print(f"  Processed {page_num + 1}/{len(doc)} pages...")

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
        print("Usage: python pdf_extract.py <pdf-path-or-url> [output-path]")
        sys.exit(1)

    source = sys.argv[1]

    # Download if URL
    pdf_path = download_if_url(source)

    if not os.path.exists(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)

    # Determine output path
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_path = sys.argv[2] if len(sys.argv) > 2 else f"/tmp/{base_name}.md"

    print(f"Extracting: {pdf_path}")
    print(f"Output: {output_path}")

    # Try pymupdf4llm first
    print("Trying pymupdf4llm extraction...")
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

    print(f"\nDone! Output written to: {output_path}")
    print(f"Total characters: {len(text):,}")

if __name__ == "__main__":
    main()
```

## Requirements

- **pytesseract**: Requires tesseract-ocr installed on system
  - macOS: `brew install tesseract`
  - Ubuntu: `apt install tesseract-ocr`
- Other deps handled by `uv run` inline metadata

## Output

- Markdown file at `/tmp/<original-filename>.md`
- Or specify custom output path as second argument

## Notes

- Large image-based PDFs (like salary guides) can take several minutes for OCR
- pymupdf4llm is very fast for text-based PDFs (~0.1s)
- OCR quality depends on scan quality; 2x zoom helps accuracy
