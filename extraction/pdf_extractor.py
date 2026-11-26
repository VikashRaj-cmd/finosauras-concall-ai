import logging
from pathlib import Path

import fitz  # pymupdf
import pdfplumber

logger = logging.getLogger(__name__)


def _extract_with_pymupdf(pdf_path: str) -> str:
    text_parts = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text_parts.append(page.get_text("text"))
    return "\n".join(text_parts)


def _extract_with_pdfplumber(pdf_path: str) -> str:
    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text(x_tolerance=3, y_tolerance=3)
            if text:
                text_parts.append(text)
    return "\n".join(text_parts)


def _extract_with_ocr(pdf_path: str) -> str:
    """OCR fallback for scanned/image-only PDFs. Requires Tesseract installed."""
    try:
        import pytesseract
        from PIL import Image

        text_parts = []
        with fitz.open(pdf_path) as doc:
            for page in doc:
                pix = page.get_pixmap(dpi=200)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                text_parts.append(pytesseract.image_to_string(img))
        return "\n".join(text_parts)
    except ImportError:
        logger.warning("pytesseract/Pillow not available — OCR skipped")
        return ""
    except Exception as e:
        logger.warning(f"OCR failed: {e}")
        return ""


def extract_text(pdf_path: str) -> str:
    """
    Extract text from a PDF file.
    Tries pymupdf first, falls back to pdfplumber, then OCR for scanned PDFs.
    Returns raw extracted text.
    """
    # Try pymupdf first (fastest)
    try:
        text = _extract_with_pymupdf(pdf_path)
        if len(text.strip()) > 200:
            logger.info(f"Extracted via pymupdf: {pdf_path} ({len(text)} chars)")
            return text
    except Exception as e:
        logger.warning(f"pymupdf failed for {pdf_path}: {e}")

    # Fallback to pdfplumber (better for complex layouts)
    try:
        text = _extract_with_pdfplumber(pdf_path)
        if len(text.strip()) > 200:
            logger.info(f"Extracted via pdfplumber: {pdf_path} ({len(text)} chars)")
            return text
    except Exception as e:
        logger.warning(f"pdfplumber failed for {pdf_path}: {e}")

    # Last resort: OCR
    logger.info(f"Attempting OCR for {pdf_path}")
    text = _extract_with_ocr(pdf_path)
    if text.strip():
        logger.info(f"Extracted via OCR: {pdf_path} ({len(text)} chars)")
        return text

    logger.error(f"All extraction methods failed for {pdf_path}")
    return ""
