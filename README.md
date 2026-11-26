# Finosauras Concall AI

An end-to-end real-time pipeline that automatically detects Indian company earnings call (concall) transcripts from NSE and BSE, extracts text from PDFs, generates structured AI summaries, and streams them via WebSocket to a live dashboard.

---

## Quick Start (Docker)

```bash
cp .env.example .env
# Fill in GEMINI_API_KEY in .env
docker compose up --build
```

Open http://localhost:3000

---

## Quick Start (Manual)

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
cp .env.example .env
# Fill in GEMINI_API_KEY in .env

# Start backend
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Start frontend (new terminal)
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

---

## Architecture

```
[ NSE/BSE Watcher ] → [ PDF Downloader ] → [ Text Extractor ] → [ AI Summarizer ]
                                                                        ↓
                                                          [ FastAPI Backend + WebSocket ]
                                                                        ↓
                                                              [ React Dashboard ]
```

### Pipeline Stages

| Stage | Module | Description |
|---|---|---|
| Watch & Ingest | `ingestion/` | Polls NSE/BSE APIs every 5 min, identifies concall filings, downloads PDFs |
| Extract | `extraction/` | Converts PDFs to clean text — pymupdf → pdfplumber → OCR fallback chain |
| Summarize | `summarization/` | Chunks transcripts, map-reduce with Gemini, outputs JSON + Markdown |
| Serve & Stream | `backend/` | FastAPI REST + WebSocket; broadcasts new summaries in real time |
| Dashboard | `frontend/` | React + Tailwind — live company list, full summary detail view |

---

## Environment Variables

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | Google Gemini API key (get free at aistudio.google.com) |
| `GROQ_API_KEY` | Groq API key (alternative provider) |
| `AI_PROVIDER` | `gemini` or `groq` (default: `gemini`) |
| `POLL_INTERVAL_SECONDS` | How often to check NSE/BSE (default: `300`) |
| `TRACKED_SYMBOLS` | Comma-separated NSE symbols (default: `RELIANCE,HDFCBANK,TATAMOTORS,SUNPHARMA,INFY`) |

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/summaries` | List all summaries |
| GET | `/api/summaries/{symbol}` | Get summary for a symbol |
| GET | `/api/summaries/{symbol}/markdown` | Get Markdown summary |
| GET | `/api/filings` | List all filings from DB |
| GET | `/health` | Health check |
| WS | `/ws` | WebSocket — streams new summaries live |

Interactive docs: http://localhost:8000/docs

---

## Sample Outputs

See `data/summaries/` for real outputs:
- `json/` — machine-readable summaries (RELIANCE, HDFCBANK, INFY)
- `markdown/` — human-readable Markdown reports

---

## Design Decisions & Trade-offs

**Chunking strategy (map-reduce)**
Transcripts run 15–40+ pages and exceed a single LLM context window. Each transcript is split into ~3000-token chunks at paragraph boundaries. Each chunk is summarized independently (map), then all chunk summaries are merged into a final structured JSON (reduce). This reliably handles even the longest transcripts.

**Deduplication**
Each filing is identified by a SHA-256 hash of `(nse_symbol + bse_code + pdf_url)` stored in SQLite. Re-runs and watcher polls skip already-processed filings automatically.

**3-layer PDF extraction**
pymupdf (fastest) → pdfplumber (better multi-column layout handling) → Tesseract OCR (scanned/image PDFs). Each layer is tried in order; the first one that returns >200 chars of text wins.

**SQLite over Postgres**
Keeps setup to a single command with no external DB dependency. The data volume (hundreds of filings) is well within SQLite's capabilities.

**NSE/BSE scraping**
Both exchanges actively block automated requests. The pipeline implements proper browser-like headers, session cookie initialization, exponential backoff retries, and graceful error handling. When automated download fails, the pipeline continues with manually placed PDFs — the watcher will pick up any new automated downloads when they succeed.

**WebSocket broadcast**
New summaries are broadcast to all connected clients the moment they are generated, with no polling needed on the frontend. Auto-reconnect is implemented in the React hook.

**Dual AI provider support**
Gemini (default) and Groq are both supported via a single `call_llm()` interface. Switch by changing `AI_PROVIDER` in `.env`.

---

## Limitations / Known Issues

- NSE/BSE websites actively block automated requests — exponential backoff is implemented but not foolproof. Manual PDF placement is the reliable fallback.
- Gemini free tier has a daily request limit (20 req/day for gemini-2.5-flash). For large batches, use `gemini-2.5-flash-lite` (higher quota) or add a billing account.
- OCR fallback requires Tesseract installed on the system (`apt-get install tesseract-ocr` on Linux, manual install on Windows).
- Quarter auto-detection from transcript text uses regex — may show "latest" if the quarter string format is unusual.

---

## What I'd Do With More Time

- **Management tone / sentiment scoring** — score each call as bullish/neutral/bearish and plot trends per company across quarters
- **Backfill mode** — pull historical concalls for any company on demand via a CLI command
- **Audio transcript handling** — detect when only a recording is filed (no PDF yet) and queue it for processing once the transcript appears
- **Full-text search** — index all summaries in SQLite FTS5 for keyword search across companies and quarters
- **Email/Slack alerts** — notify when a tracked company files a new concall
- **Caching layer** — cache LLM responses per chunk hash to avoid re-processing identical content

---

## Project Structure

```
finosauras-concall-ai/
├── ingestion/
│   ├── nse.py          # NSE announcement fetcher
│   ├── bse.py          # BSE announcement fetcher
│   ├── downloader.py   # PDF downloader with retries
│   ├── database.py     # SQLite deduplication
│   └── pipeline.py     # Ingestion orchestrator
├── extraction/
│   ├── pdf_extractor.py  # pymupdf → pdfplumber → OCR
│   ├── cleaner.py        # Text cleaning + quarter detection
│   └── pipeline.py       # Extraction orchestrator
├── summarization/
│   ├── prompts.py      # LLM prompt templates
│   ├── chunking.py     # Transcript chunking
│   ├── llm.py          # Gemini / Groq client
│   └── pipeline.py     # Map-reduce summarization
├── backend/
│   ├── main.py         # FastAPI app + background watcher
│   ├── routes.py       # REST endpoints
│   ├── websocket.py    # WebSocket connection manager
│   ├── database.py     # Read summaries + filings
│   └── models.py       # Pydantic schemas
├── frontend/
│   ├── src/
│   │   ├── pages/      # Dashboard, SummaryDetail
│   │   ├── components/ # CompanyCard, LiveBadge
│   │   └── hooks/      # useWebSocket
│   └── Dockerfile
├── data/
│   ├── pdfs/           # Downloaded PDFs (gitignored)
│   ├── transcripts/    # Extracted text (gitignored)
│   └── summaries/      # JSON + Markdown outputs (committed)
├── manual_tasks/       # Step-by-step manual task guides
├── .env.example
├── requirements.txt
├── Dockerfile.backend
├── docker-compose.yml
└── README.md
```
