import logging
from pathlib import Path

from extraction.pdf_extractor import extract_text
from extraction.cleaner import clean_transcript, detect_quarter
from ingestion.database import get_all_filings, update_status, _connect

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

TRANSCRIPTS_DIR = Path("data/transcripts")
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)


def get_transcript_path(filing: dict) -> Path:
    symbol = filing.get("nse_symbol") or filing.get("bse_code", "unknown")
    quarter = filing.get("quarter", "").replace(" ", "_") or "latest"
    return TRANSCRIPTS_DIR / f"{symbol}_{quarter}.txt"


def process_filing(filing: dict) -> str | None:
    """
    Extract + clean text from a filing's PDF.
    Saves to data/transcripts/ and returns the transcript path.
    """
    pdf_path = filing.get("pdf_path")
    if not pdf_path or not Path(pdf_path).exists():
        logger.warning(f"PDF not found for {filing.get('company')}: {pdf_path}")
        return None

    # Extract raw text
    raw_text = extract_text(pdf_path)
    if not raw_text:
        update_status(filing, "extraction_failed")
        return None

    # Clean text
    clean_text = clean_transcript(raw_text)

    # Detect quarter if not already set
    if not filing.get("quarter"):
        quarter = detect_quarter(clean_text)
        if quarter:
            filing["quarter"] = quarter
            _update_quarter(filing, quarter)

    # Save transcript
    transcript_path = get_transcript_path(filing)
    transcript_path.write_text(clean_text, encoding="utf-8")
    logger.info(f"Saved transcript: {transcript_path} ({len(clean_text)} chars)")

    update_status(filing, "extracted")
    return str(transcript_path)


def _update_quarter(filing: dict, quarter: str):
    from ingestion.database import _connect, _filing_hash
    fh = _filing_hash(filing)
    with _connect() as conn:
        conn.execute(
            "UPDATE filings SET quarter = ? WHERE filing_hash = ?", (quarter, fh)
        )
        conn.commit()


def run_extraction(filings: list[dict] = None) -> list[dict]:
    """
    Run extraction on all downloaded filings (or a provided list).
    Returns filings with transcript_path added.
    """
    if filings is None:
        all_filings = get_all_filings()
        filings = [f for f in all_filings if f["status"] == "downloaded"]

    logger.info(f"Extracting text from {len(filings)} filing(s)...")
    results = []

    for filing in filings:
        transcript_path = process_filing(filing)
        if transcript_path:
            filing["transcript_path"] = transcript_path
            results.append(filing)

    logger.info(f"Extraction complete. {len(results)}/{len(filings)} succeeded.")
    return results


if __name__ == "__main__":
    processed = run_extraction()
    print(f"\n✅ Done. {len(processed)} transcript(s) extracted.")
    for f in processed:
        print(f"  {f['company']} [{f.get('quarter', 'unknown')}] → {f['transcript_path']}")
