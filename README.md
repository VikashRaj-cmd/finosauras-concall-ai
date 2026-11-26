# Finosauras Concall AI

An end-to-end real-time pipeline that automatically detects Indian company earnings call (concall) transcripts from NSE and BSE, extracts text from PDFs, generates structured AI summaries, and streams them via WebSocket to a live dashboard.

---

## Quick Start

```bash
cp .env.example .env
# Fill in your API keys in .env
docker compose up --build
```

Then open http://localhost:3000

---

## Architecture

```
[ NSE/BSE Watcher ] → [ PDF Downloader ] → [ Text Extractor ] → [ AI Summarizer ]
                                                                        ↓
                                                          [ FastAPI Backend + WebSocket ]
                                                                        ↓
                                                              [ React Dashboard ]
```

### Stages

| Stage | Module | Description |
|---|---|---|
| Watch & Ingest | `ingestion/` | Polls NSE/BSE APIs, identifies concall filings, downloads PDFs |
| Extract | `extraction/` | Converts PDFs to clean text, handles multi-column layouts |
| Summarize | `summarization/` | Chunks long transcripts, calls LLM, outputs JSON + Markdown |
| Serve & Stream | `backend/` | FastAPI REST + WebSocket; `frontend/` React dashboard |

---

## Setup (Manual / Without Docker)

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your keys
uvicorn backend.main:app --reload
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | Google Gemini API key |
| `GROQ_API_KEY` | Groq API key (alternative) |
| `AI_PROVIDER` | `gemini` or `groq` |
| `POLL_INTERVAL_SECONDS` | How often to check NSE/BSE (default 300s) |
| `TRACKED_SYMBOLS` | Comma-separated NSE symbols to watch |

---

## Sample Outputs

See `data/summaries/` for:
- `json/` — machine-readable summaries
- `markdown/` — human-readable summaries

---

## Design Decisions & Trade-offs

- **Chunking strategy**: Transcripts are split into ~3000-token chunks. Each chunk is summarized independently (map step), then all chunk summaries are merged into a final summary (reduce step). This handles 40+ page transcripts reliably.
- **Deduplication**: Each filing is identified by a hash of `(company, quarter, source_url)` stored in SQLite. Re-runs skip already-processed filings.
- **SQLite over Postgres**: Keeps the setup to a single command with no external DB dependency.
- **Both NSE and BSE**: The same transcript often appears on both exchanges. We deduplicate by content hash.

---

## Limitations / Known Issues

- NSE/BSE websites occasionally block requests; exponential backoff is implemented but not foolproof.
- OCR fallback (for scanned PDFs) requires Tesseract installed on the system.
- Gemini free tier has rate limits; very large batches may need delays.

---

## What I'd Do With More Time

- Management tone / sentiment scoring per quarter with trend charts
- Backfill mode to pull historical concalls on demand
- Audio transcript handling (when only recording is filed)
- Full-text search across all summaries
- Email/Slack alerts when a tracked company files a new concall

---

## Project Structure

```
finosauras-concall-ai/
├── ingestion/          # NSE + BSE fetchers, PDF downloader
├── extraction/         # PDF text extraction + cleaning
├── summarization/      # LLM integration, chunking, prompts
├── backend/            # FastAPI app, routes, WebSocket
├── frontend/           # React dashboard
├── data/
│   ├── pdfs/           # Downloaded PDFs (gitignored)
│   ├── transcripts/    # Extracted text (gitignored)
│   └── summaries/      # JSON + Markdown outputs (committed)
├── tests/
├── manual_tasks/       # Step-by-step manual task guides
├── .env.example
├── requirements.txt
├── docker-compose.yml
└── README.md
```
