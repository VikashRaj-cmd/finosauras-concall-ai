from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from backend.database import (
    get_all_filings_api,
    get_all_summaries,
    get_summary,
    get_markdown,
)
from backend.models import ConcallSummary, FilingRecord

router = APIRouter()


@router.get("/filings", response_model=list[FilingRecord])
def list_filings():
    return get_all_filings_api()


@router.get("/summaries", response_model=list[ConcallSummary])
def list_summaries():
    return get_all_summaries()


@router.get("/summaries/{symbol}", response_model=ConcallSummary)
def get_summary_by_symbol(symbol: str, quarter: str = None):
    summary = get_summary(symbol.upper(), quarter)
    if not summary:
        raise HTTPException(status_code=404, detail=f"No summary found for {symbol}")
    return summary


@router.get("/summaries/{symbol}/markdown", response_class=PlainTextResponse)
def get_markdown_by_symbol(symbol: str, quarter: str = None):
    md = get_markdown(symbol.upper(), quarter)
    if not md:
        raise HTTPException(status_code=404, detail=f"No markdown found for {symbol}")
    return md
