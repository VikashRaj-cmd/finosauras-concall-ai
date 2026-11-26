import hashlib
import logging
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)

DB_PATH = Path("data/filings.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist."""
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS filings (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                filing_hash TEXT    UNIQUE NOT NULL,
                company     TEXT    NOT NULL,
                nse_symbol  TEXT,
                bse_code    TEXT,
                quarter     TEXT,
                source      TEXT,
                pdf_url     TEXT,
                pdf_path    TEXT,
                status      TEXT    DEFAULT 'downloaded',
                created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    logger.info("Database initialized")


def _filing_hash(filing: dict) -> str:
    """Unique hash per filing based on company + pdf_url."""
    key = f"{filing.get('nse_symbol','')}{filing.get('bse_code','')}{filing.get('pdf_url','')}"
    return hashlib.sha256(key.encode()).hexdigest()[:16]


def is_duplicate(filing: dict) -> bool:
    fh = _filing_hash(filing)
    with _connect() as conn:
        row = conn.execute(
            "SELECT id FROM filings WHERE filing_hash = ?", (fh,)
        ).fetchone()
    return row is not None


def save_filing(filing: dict, pdf_path: str = None, status: str = "downloaded"):
    fh = _filing_hash(filing)
    with _connect() as conn:
        conn.execute("""
            INSERT OR IGNORE INTO filings
                (filing_hash, company, nse_symbol, bse_code, quarter, source, pdf_url, pdf_path, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            fh,
            filing.get("company", ""),
            filing.get("nse_symbol", ""),
            filing.get("bse_code", ""),
            filing.get("quarter", ""),
            filing.get("source", ""),
            filing.get("pdf_url", ""),
            pdf_path or "",
            status,
        ))
        conn.commit()


def update_status(filing: dict, status: str):
    fh = _filing_hash(filing)
    with _connect() as conn:
        conn.execute(
            "UPDATE filings SET status = ? WHERE filing_hash = ?", (status, fh)
        )
        conn.commit()


def get_all_filings() -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM filings ORDER BY created_at DESC"
        ).fetchall()
    return [dict(r) for r in rows]
