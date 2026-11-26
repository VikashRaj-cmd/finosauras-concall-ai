import logging
import time
import requests

logger = logging.getLogger(__name__)

# BSE scrip codes for our tracked companies
TRACKED_BSE = {
    "500325": {"name": "Reliance Industries Ltd",              "nse_symbol": "RELIANCE"},
    "500180": {"name": "HDFC Bank Ltd",                        "nse_symbol": "HDFCBANK"},
    "500570": {"name": "Tata Motors Ltd",                      "nse_symbol": "TATAMOTORS"},
    "524715": {"name": "Sun Pharmaceutical Industries Ltd",    "nse_symbol": "SUNPHARMA"},
    "500209": {"name": "Infosys Ltd",                          "nse_symbol": "INFY"},
}

CONCALL_KEYWORDS = [
    "concall", "conference call", "earnings call",
    "analyst meet", "investor meet", "analyst/institutional",
    "transcript", "con call",
]

# BSE category codes that typically contain concall transcripts
CONCALL_CATEGORY_CODES = ["41", "43", "44"]  # Analyst/Investor Meet categories

BSE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.bseindia.com/corporates/ann.html",
    "Connection": "keep-alive",
}

BSE_BASE = "https://api.bseindia.com"
BSE_PDF_BASE = "https://www.bseindia.com/xml-data/corpfiling/AttachLive"


def _is_concall(headline: str, attachment: str = "") -> bool:
    text = (headline + " " + attachment).lower()
    return any(kw in text for kw in CONCALL_KEYWORDS)


def fetch_bse_announcements(scrip_code: str) -> list[dict]:
    """
    Fetch recent corporate announcements for a BSE scrip code.
    Returns list of dicts with keys: company, nse_symbol, bse_code, subject, pdf_url, date, source.
    """
    url = (
        f"{BSE_BASE}/BseIndiaAPI/api/AnnSubCategoryGetData/w"
        f"?strCat=-1&strPrevDate=&strScrip={scrip_code}&strSearch=P&strToDate=&strType=C&subcategory=-1"
    )
    results = []

    try:
        resp = requests.get(url, headers=BSE_HEADERS, timeout=20)
        resp.raise_for_status()
        data = resp.json()

        announcements = data.get("Table", []) if isinstance(data, dict) else data

        for item in announcements:
            headline = item.get("HEADLINE", "") or item.get("headline", "")
            attachment = item.get("ATTACHMENTNAME", "") or item.get("attachmentname", "")
            an_date = item.get("NEWS_DT", "") or item.get("news_dt", "")

            if not _is_concall(headline, attachment):
                continue

            pdf_url = None
            if attachment:
                pdf_url = f"{BSE_PDF_BASE}/{attachment}"

            if not pdf_url:
                continue

            company_info = TRACKED_BSE.get(scrip_code, {})
            results.append({
                "company": company_info.get("name", scrip_code),
                "nse_symbol": company_info.get("nse_symbol", ""),
                "bse_code": scrip_code,
                "subject": headline,
                "pdf_url": pdf_url,
                "date": an_date,
                "source": "BSE",
            })

        logger.info(f"BSE [{scrip_code}]: found {len(results)} concall filing(s)")

    except Exception as e:
        logger.error(f"BSE fetch failed for {scrip_code}: {e}")

    return results


def fetch_all_bse(scrip_codes: list[str] = None) -> list[dict]:
    """Fetch concall announcements for all tracked BSE scrip codes."""
    if scrip_codes is None:
        scrip_codes = list(TRACKED_BSE.keys())

    all_results = []
    for code in scrip_codes:
        results = fetch_bse_announcements(code)
        all_results.extend(results)
        time.sleep(1.5)

    return all_results
