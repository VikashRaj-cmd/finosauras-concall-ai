import json
import logging
import re
from pathlib import Path

from summarization.chunking import chunk_transcript
from summarization.llm import call_llm
from summarization.prompts import CHUNK_SUMMARY_PROMPT, FINAL_SUMMARY_PROMPT, MARKDOWN_PROMPT
from ingestion.database import get_all_filings, _connect, _filing_hash

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

JSON_DIR = Path("data/summaries/json")
MD_DIR = Path("data/summaries/markdown")
JSON_DIR.mkdir(parents=True, exist_ok=True)
MD_DIR.mkdir(parents=True, exist_ok=True)


def _map_chunks(chunks: list[str]) -> str:
    """Summarize each chunk independently, return combined notes."""
    chunk_summaries = []
    for i, chunk in enumerate(chunks, 1):
        logger.info(f"  Summarizing chunk {i}/{len(chunks)}...")
        prompt = CHUNK_SUMMARY_PROMPT.format(chunk=chunk)
        summary = call_llm(prompt)
        chunk_summaries.append(f"--- Chunk {i} ---\n{summary}")
    return "\n\n".join(chunk_summaries)


def _reduce(chunk_summaries: str, filing: dict) -> dict:
    """Merge all chunk summaries into a final structured JSON."""
    prompt = FINAL_SUMMARY_PROMPT.format(
        company=filing.get("company", ""),
        scrip_code=filing.get("bse_code", ""),
        nse_symbol=filing.get("nse_symbol", ""),
        quarter=filing.get("quarter", ""),
        call_date=filing.get("date", ""),
        source=filing.get("source", ""),
        source_url=filing.get("pdf_url", ""),
        chunk_summaries=chunk_summaries,
    )
    raw = call_llm(prompt)

    # Strip markdown fences if model wrapped the JSON
    raw = re.sub(r"^```(?:json)?\s*", "", raw.strip())
    raw = re.sub(r"\s*```$", "", raw.strip())

    return json.loads(raw)


def _generate_markdown(summary: dict) -> str:
    """Generate human-readable Markdown from the summary dict."""
    prompt = MARKDOWN_PROMPT.format(summary_json=json.dumps(summary, indent=2))
    return call_llm(prompt)


def _save_outputs(summary: dict, markdown: str, filing: dict):
    symbol = filing.get("nse_symbol") or filing.get("bse_code", "unknown")
    quarter = (filing.get("quarter") or "latest").replace(" ", "_")

    json_path = JSON_DIR / f"{symbol}_{quarter}.json"
    md_path = MD_DIR / f"{symbol}_{quarter}.md"

    json_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")

    logger.info(f"Saved: {json_path}")
    logger.info(f"Saved: {md_path}")

    return str(json_path), str(md_path)


def _update_filing_status(filing: dict, status: str, json_path: str = "", md_path: str = ""):
    fh = _filing_hash(filing)
    with _connect() as conn:
        conn.execute(
            "UPDATE filings SET status = ? WHERE filing_hash = ?", (status, fh)
        )
        conn.commit()


def summarize_filing(filing: dict) -> dict | None:
    """
    Full map-reduce summarization for one filing.
    Returns the summary dict or None on failure.
    """
    transcript_path = filing.get("transcript_path") or _find_transcript(filing)
    if not transcript_path or not Path(transcript_path).exists():
        logger.warning(f"No transcript for {filing.get('company')}")
        return None

    text = Path(transcript_path).read_text(encoding="utf-8")
    if len(text.strip()) < 100:
        logger.warning(f"Transcript too short for {filing.get('company')}")
        return None

    logger.info(f"Summarizing: {filing.get('company')} ({len(text)} chars)")

    chunks = chunk_transcript(text)
    logger.info(f"  Split into {len(chunks)} chunk(s)")

    # Map step
    chunk_summaries = _map_chunks(chunks)

    # Reduce step
    try:
        summary = _reduce(chunk_summaries, filing)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse failed for {filing.get('company')}: {e}")
        _update_filing_status(filing, "summarization_failed")
        return None

    # Generate Markdown
    markdown = _generate_markdown(summary)

    # Save both outputs
    json_path, md_path = _save_outputs(summary, markdown, filing)
    _update_filing_status(filing, "summarized", json_path, md_path)

    summary["_json_path"] = json_path
    summary["_md_path"] = md_path
    return summary


def _find_transcript(filing: dict) -> str | None:
    """Look up transcript path from data/transcripts/ by symbol."""
    symbol = filing.get("nse_symbol") or filing.get("bse_code", "")
    matches = list(Path("data/transcripts").glob(f"{symbol}_*.txt"))
    return str(matches[0]) if matches else None


def run_summarization(filings: list[dict] = None) -> list[dict]:
    """Run summarization on all extracted filings."""
    if filings is None:
        all_filings = get_all_filings()
        filings = [f for f in all_filings if f["status"] == "extracted"]

    logger.info(f"Summarizing {len(filings)} filing(s)...")
    results = []

    for filing in filings:
        summary = summarize_filing(filing)
        if summary:
            results.append(summary)

    logger.info(f"Summarization complete. {len(results)}/{len(filings)} succeeded.")
    return results


if __name__ == "__main__":
    summaries = run_summarization()
    print(f"\n✅ Done. {len(summaries)} summary(ies) generated.")
    for s in summaries:
        print(f"  {s.get('company')} [{s.get('quarter')}]")
        print(f"    JSON → {s.get('_json_path')}")
        print(f"    MD   → {s.get('_md_path')}")
