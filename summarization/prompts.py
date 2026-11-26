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

Produce a JSON object with EXACTLY this schema. Every claim must come from the notes above — do not hallucinate.
Be CONCISE — max 3 items per array, max 15 words per string:

{{
  "company": "{company}",
  "scrip_code": "{scrip_code}",
  "nse_symbol": "{nse_symbol}",
  "quarter": "{quarter}",
  "call_date": "{call_date}",
  "source": "{source}",
  "source_url": "{source_url}",
  "tldr": ["bullet 1", "bullet 2", "bullet 3"],
  "management_commentary": ["highlight 1", "highlight 2"],
  "guidance": ["guidance 1", "guidance 2"],
  "segment_performance": [
    {{"segment": "name", "notes": "brief notes"}}
  ],
  "key_metrics": [
    {{"metric": "name", "value": "value", "context": "brief"}}
  ],
  "notable_qa": [
    {{"question": "short question", "answer": "short answer", "asked_by": "name or Unknown"}}
  ],
  "risks": ["risk 1", "risk 2"]
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
