import json
from pathlib import Path

from ingestion.database import get_all_filings
from backend.models import ConcallSummary, FilingRecord

JSON_DIR = Path("data/summaries/json")
MD_DIR = Path("data/summaries/markdown")


def get_all_filings_api() -> list[FilingRecord]:
    rows = get_all_filings()
    return [FilingRecord(**{k: v or "" for k, v in r.items() if k in FilingRecord.model_fields}) for r in rows]


def get_summary(nse_symbol: str, quarter: str = None) -> ConcallSummary | None:
    """Load a summary JSON for a given symbol. If quarter not given, returns latest."""
    pattern = f"{nse_symbol}_*.json"
    matches = sorted(JSON_DIR.glob(pattern), reverse=True)

    if not matches:
        return None

    if quarter:
        q = quarter.replace(" ", "_")
        target = JSON_DIR / f"{nse_symbol}_{q}.json"
        if target.exists():
            path = target
        else:
            return None
    else:
        path = matches[0]

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return ConcallSummary(**data)
    except Exception:
        return None


def get_markdown(nse_symbol: str, quarter: str = None) -> str | None:
    """Load Markdown summary for a given symbol."""
    pattern = f"{nse_symbol}_*.md"
    matches = sorted(MD_DIR.glob(pattern), reverse=True)

    if not matches:
        return None

    if quarter:
        q = quarter.replace(" ", "_")
        target = MD_DIR / f"{nse_symbol}_{q}.md"
        path = target if target.exists() else matches[0]
    else:
        path = matches[0]

    return path.read_text(encoding="utf-8") if path.exists() else None


def get_all_summaries() -> list[ConcallSummary]:
    """Return all available summaries."""
    summaries = []
    for path in sorted(JSON_DIR.glob("*.json"), reverse=True):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            summaries.append(ConcallSummary(**data))
        except Exception:
            continue
    return summaries
