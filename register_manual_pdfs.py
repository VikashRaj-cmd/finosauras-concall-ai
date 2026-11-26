"""
Run this after manually placing PDFs in data/pdfs/ to register them in the database.
Usage: python register_manual_pdfs.py
"""
from ingestion.database import init_db, save_filing, get_all_filings

MANUAL_FILINGS = [
    {
        "filing": {
            "company": "Reliance Industries Ltd",
            "nse_symbol": "RELIANCE",
            "bse_code": "500325",
            "source": "BSE",
            "pdf_url": "manual_reliance",
            "quarter": "",
        },
        "pdf_path": "data/pdfs/RELIANCE_manual.pdf",
    },
    {
        "filing": {
            "company": "HDFC Bank Ltd",
            "nse_symbol": "HDFCBANK",
            "bse_code": "500180",
            "source": "BSE",
            "pdf_url": "manual_hdfcbank",
            "quarter": "",
        },
        "pdf_path": "data/pdfs/HDFCBANK_manual.pdf",
    },
    {
        "filing": {
            "company": "Infosys Ltd",
            "nse_symbol": "INFY",
            "bse_code": "500209",
            "source": "BSE",
            "pdf_url": "manual_infy",
            "quarter": "",
        },
        "pdf_path": "data/pdfs/INFY_manual.pdf",
    },
]

if __name__ == "__main__":
    import os

    init_db()

    for entry in MANUAL_FILINGS:
        path = entry["pdf_path"]
        if not os.path.exists(path):
            print(f"  MISSING: {path} — download this PDF first")
            continue
        save_filing(entry["filing"], pdf_path=path, status="downloaded")
        print(f"  Registered: {entry['filing']['company']} → {path}")

    print("\nAll filings in database:")
    for f in get_all_filings():
        print(f"  {f['company']} | {f['source']} | {f['status']} | {f['pdf_path']}")
