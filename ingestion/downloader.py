import hashlib
import logging
import time
from pathlib import Path

import requests

logger = logging.getLogger(__name__)

DATA_DIR = Path("data/pdfs")
DATA_DIR.mkdir(parents=True, exist_ok=True)

DOWNLOAD_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/pdf,*/*",
}

MAX_RETRIES = 3
BACKOFF_BASE = 2  # seconds


def _url_hash(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()[:12]


def download_pdf(filing: dict) -> str | None:
    """
    Download a PDF for a filing dict.
    Returns local file path on success, None on failure.
    filing must have: pdf_url, nse_symbol, source
    """
    url = filing["pdf_url"]
    symbol = filing.get("nse_symbol") or filing.get("bse_code", "unknown")
    filename = f"{symbol}_{_url_hash(url)}.pdf"
    dest = DATA_DIR / filename

    if dest.exists():
        logger.info(f"Already downloaded: {dest}")
        return str(dest)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, headers=DOWNLOAD_HEADERS, timeout=30, stream=True)
            resp.raise_for_status()

            content_type = resp.headers.get("Content-Type", "")
            if "pdf" not in content_type and "octet-stream" not in content_type:
                logger.warning(f"Unexpected content type '{content_type}' for {url}")

            with open(dest, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)

            logger.info(f"Downloaded: {dest} ({dest.stat().st_size} bytes)")
            return str(dest)

        except Exception as e:
            wait = BACKOFF_BASE ** attempt
            logger.warning(f"Download attempt {attempt} failed for {url}: {e}. Retrying in {wait}s...")
            time.sleep(wait)

    logger.error(f"All {MAX_RETRIES} download attempts failed for {url}")
    return None
