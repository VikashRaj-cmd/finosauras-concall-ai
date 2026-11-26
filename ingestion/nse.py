import logging
import time
import requests

logger = logging.getLogger(__name__)

# NSE symbols → scrip info mapping for our tracked companies
TRACKED_COMPANIES = {
    "RELIANCE":   {"name": "Reliance Industries Ltd",  "bse_code": "500325"},
    "HDFCBANK":   {"name": "HDFC Bank Ltd",            "bse_code": "500180"},
    "TATAMOTORS": {"name": "Tata Motors Ltd",          "bse_code": "500570"},
    "SUNPHARMA":  {"name": "Sun Pharmaceutical Industries Ltd", "bse_code": "524715"},
    "INFY":       {"name": "Infosys Ltd",              "bse_code": "500209"},
}

CONCALL_KEYWORDS = [
    "concall", "conference call", "earnings call",
    "analyst meet", "investor meet", "analyst/institutional",
    "transcript", "con call",
]

NSE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/companies-listing/corporate-filings-announcements",
    "Connection": "keep-alive",
}

NSE_BASE = "https://www.nseindia.com"


def _get_session() -> requests.Session:
    """Create a session with NSE cookies by hitting the homepage first."""
    session = requests.Session()
    session.headers.update(NSE_HEADERS)
    try:
        # Hit homepage first to get cookies
        session.get(NSE_BASE, timeout=15)
        time.sleep(2)
        # Hit the announcements page to get additional cookies
        session.get(
            f"{NSE_BASE}/companies-listing/corporate-filings-announcements",
            timeout=15
        )
        time.sleep(1)
    except Exception as e:
        logger.warning(f"NSE session init warning: {e}")
    return session


def _is_concall(subject: str, attachment_name: str = "") -> bool:
    text = (subject + " " + attachment_name).lower()
    return any(kw in text for kw in CONCALL_KEYWORDS)


def fetch_nse_announcements(symbol: str, session: requests.Session = None) -> list[dict]:
    """
    Fetch recent corporate announcements for a symbol from NSE.
    Returns list of dicts with keys: company, nse_symbol, subject, pdf_url, date, source.
    """
    if session is None:
        session = _get_session()

    url = f"{NSE_BASE}/api/corp-announcements?index=equities&symbol={symbol}"
    results = []

    try:
        resp = session.get(url, timeout=20)
        resp.raise_for_status()
        data = resp.json()

        announcements = data if isinstance(data, list) else data.get("data", [])

        for item in announcements:
            subject = item.get("subject", "") or item.get("desc", "")
            attachments = item.get("attchmntFile", "") or item.get("attachment", "")
            an_date = item.get("an_dt", "") or item.get("date", "")

            if not _is_concall(subject, attachments):
                continue

            # Build PDF URL
            pdf_url = None
            if attachments:
                if attachments.startswith("http"):
                    pdf_url = attachments
                else:
                    pdf_url = f"{NSE_BASE}/corporate-announcements/{attachments}"

            if not pdf_url:
                continue

            results.append({
                "company": TRACKED_COMPANIES.get(symbol, {}).get("name", symbol),
                "nse_symbol": symbol,
                "bse_code": TRACKED_COMPANIES.get(symbol, {}).get("bse_code", ""),
                "subject": subject,
                "pdf_url": pdf_url,
                "date": an_date,
                "source": "NSE",
            })

        logger.info(f"NSE [{symbol}]: found {len(results)} concall filing(s)")

    except Exception as e:
        logger.error(f"NSE fetch failed for {symbol}: {e}")

    return results


def fetch_all_nse(symbols: list[str] = None) -> list[dict]:
    """Fetch concall announcements for all tracked symbols."""
    if symbols is None:
        symbols = list(TRACKED_COMPANIES.keys())

    session = _get_session()
    all_results = []

    for symbol in symbols:
        results = fetch_nse_announcements(symbol, session)
        all_results.extend(results)
        time.sleep(1.5)  # be respectful with rate

    return all_results
