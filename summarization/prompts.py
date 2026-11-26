CHUNK_SUMMARY_PROMPT = """You are analyzing a portion of an earnings conference call transcript.
Extract ONLY what is explicitly stated in this excerpt. Do not invent or infer anything not present.

Excerpt:
{chunk}

Extract the following (skip any section if not mentioned in this excerpt):
- Key financial metrics mentioned (revenue, margins, profit, volumes, order book, capex)
- Management statements about business performance
- Forward-looking guidance or targets
- Segment or vertical performance details
- Notable analyst questions and management answers
- Risks or concerns raised

Respond in plain text, clearly labeled by section. Be concise."""


FINAL_SUMMARY_PROMPT = """You are a financial analyst. Based on the following extracted notes from an earnings call transcript, produce a structured summary.

Company: {company}
Quarter: {quarter}

Extracted notes:
{chunk_summaries}

Produce a JSON object with EXACTLY this schema. Every claim must come from the notes above — do not hallucinate:

{{
  "company": "{company}",
  "scrip_code": "{scrip_code}",
  "nse_symbol": "{nse_symbol}",
  "quarter": "{quarter}",
  "call_date": "{call_date}",
  "source": "{source}",
  "source_url": "{source_url}",
  "tldr": ["3 to 5 bullet points summarizing the call"],
  "management_commentary": ["key highlights from management"],
  "guidance": ["forward-looking statements and targets"],
  "segment_performance": [
    {{"segment": "segment name", "notes": "performance details"}}
  ],
  "key_metrics": [
    {{"metric": "metric name", "value": "value", "context": "brief context"}}
  ],
  "notable_qa": [
    {{"question": "analyst question", "answer": "management answer", "asked_by": "analyst name or Unknown"}}
  ],
  "risks": ["risk or concern mentioned"]
}}

Return ONLY the JSON object, no markdown fences, no extra text."""


MARKDOWN_PROMPT = """Convert this earnings call summary JSON into a clean, readable Markdown report.

{summary_json}

Format:
# {{company}} — {{quarter}} Earnings Call Summary

## TL;DR
(bullet points)

## Management Commentary
(bullet points)

## Guidance & Outlook
(bullet points)

## Segment Performance
(table or bullet points)

## Key Metrics
(table with Metric | Value | Context columns)

## Notable Q&A
(each Q&A as a sub-section)

## Risks & Concerns
(bullet points)

Return only the Markdown, no extra commentary."""
