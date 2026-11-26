import logging
import os

from dotenv import load_dotenv

from ingestion.nse import fetch_all_nse
from ingestion.bse import fetch_all_bse
from ingestion.downloader import download_pdf
from ingestion.database import init_db, is_duplicate, save_filing, update_status

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def run_ingestion(symbols: list[str] = None) -> list[dict]:
    """
    Full ingestion run:
    1. Fetch announcements from NSE + BSE
    2. Deduplicate
    3. Download new PDFs
    Returns list of new filings with pdf_path set.
    """
    init_db()

    tracked = symbols or os.getenv("TRACKED_SYMBOLS", "RELIANCE,HDFCBANK,TATAMOTORS,SUNPHARMA,INFY").split(",")
    tracked = [s.strip() for s in tracked]

    logger.info(f"Fetching announcements for: {tracked}")

    nse_filings = fetch_all_nse(tracked)
    bse_filings = fetch_all_bse()

    all_filings = nse_filings + bse_filings
    logger.info(f"Total concall filings found: {len(all_filings)}")

    new_filings = []
    for filing in all_filings:
        if is_duplicate(filing):
            logger.info(f"Skipping duplicate: {filing['company']} [{filing['source']}]")
            continue

        pdf_path = download_pdf(filing)
        if not pdf_path:
            save_filing(filing, status="download_failed")
            continue

        save_filing(filing, pdf_path=pdf_path, status="downloaded")
        filing["pdf_path"] = pdf_path
        new_filings.append(filing)
        logger.info(f"New filing saved: {filing['company']} → {pdf_path}")

    logger.info(f"Ingestion complete. New filings: {len(new_filings)}")
    return new_filings


if __name__ == "__main__":
    new = run_ingestion()
    print(f"\n✅ Done. {len(new)} new filing(s) downloaded.")
    for f in new:
        print(f"  {f['company']} [{f['source']}] → {f['pdf_path']}")
