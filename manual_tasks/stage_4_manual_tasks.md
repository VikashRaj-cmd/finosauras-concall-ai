# Manual Tasks — Stage 4: AI Summarization

---

## Step 1: Make sure your .env has a valid Gemini API key

Open `.env` and confirm:
```
GEMINI_API_KEY=your_actual_key_here
AI_PROVIDER=gemini
```

Get a free key at: https://aistudio.google.com/app/apikey

---

## Step 2: Run the summarization pipeline

```bash
python -m summarization.pipeline
```

### What to expect:
- Each transcript is split into chunks (~3000 tokens each)
- Each chunk is sent to Gemini separately (map step)
- All chunk summaries are merged into a final JSON (reduce step)
- A Markdown report is generated from the JSON
- Files saved in `data/summaries/json/` and `data/summaries/markdown/`

This will take 2-5 minutes per company due to API calls.

### Expected output:
```
✅ Done. 3 summary(ies) generated.
  Reliance Industries Ltd [Q2 FY26]
    JSON → data/summaries/json/RELIANCE_Q2_FY26.json
    MD   → data/summaries/markdown/RELIANCE_Q2_FY26.md
  HDFC Bank Ltd [Q2 FY27]
    JSON → data/summaries/json/HDFCBANK_Q2_FY27.json
    ...
```

---

## Step 3: If you see a rate limit error

Gemini free tier allows ~15 requests/minute. If you see a 429 error, wait 60 seconds and re-run:
```bash
python -m summarization.pipeline
```
It will skip already-summarized filings automatically.

---

## Step 4: Verify the outputs

Check a JSON summary:
```bash
type data\summaries\json\RELIANCE_Q2_FY26.json | more
```

Check a Markdown summary:
```bash
type data\summaries\markdown\RELIANCE_Q2_FY26.md | more
```

The JSON should have all fields: tldr, management_commentary, guidance, segment_performance, key_metrics, notable_qa, risks.

---

## Git Commit Commands

```bash
git add .
```

```bash
git commit -m "AI summarization: chunking, map-reduce pipeline, JSON and Markdown outputs"
```

```bash
git push origin main
```

---

Once you have JSON + Markdown files in `data/summaries/`, reply: **"Stage 4 done"**
