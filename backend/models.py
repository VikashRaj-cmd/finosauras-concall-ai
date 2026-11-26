from pydantic import BaseModel


class SegmentPerformance(BaseModel):
    segment: str
    notes: str


class KeyMetric(BaseModel):
    metric: str
    value: str
    context: str = ""


class NotableQA(BaseModel):
    question: str
    answer: str
    asked_by: str = "Unknown"


class ConcallSummary(BaseModel):
    company: str
    scrip_code: str = ""
    nse_symbol: str = ""
    quarter: str = ""
    call_date: str = ""
    source: str = ""
    source_url: str = ""
    tldr: list[str] = []
    management_commentary: list[str] = []
    guidance: list[str] = []
    segment_performance: list[SegmentPerformance] = []
    key_metrics: list[KeyMetric] = []
    notable_qa: list[NotableQA] = []
    risks: list[str] = []


class FilingRecord(BaseModel):
    id: int
    company: str
    nse_symbol: str = ""
    bse_code: str = ""
    quarter: str = ""
    source: str = ""
    status: str = ""
    created_at: str = ""
