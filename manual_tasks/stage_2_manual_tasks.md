# Manual Tasks — Stage 2: NSE + BSE Ingestion

---

## Step 1: Activate your virtual environment

```bash
venv\Scripts\activate
```

---

## Step 2: Test the ingestion pipeline

```bash
python -m ingestion.pipeline
```

### What to expect:
- It will try to fetch announcements from NSE and BSE for: RELIANCE, HDFCBANK, TATAMOTORS, SUNPHARMA, INFY
- NSE/BSE may return 0 results if no new concall filings exist right now — that is NORMAL
- If PDFs are found, they will be saved in `data/pdfs/`
- A SQLite database will be created at `data/filings.db`

### If you see errors like "Connection refused" or "403 Forbidden":
- NSE/BSE block automated requests sometimes — this is expected
- The pipeline has retry logic built in
- We will handle this with manual PDF uploads in Stage 3

---

## Step 3: Manually download sample PDFs (IMPORTANT)

Since NSE/BSE may block automated downloads, we need at least 3 real concall PDFs to test the full pipeline.

Download these PDFs manually from BSE:

### How to find concall PDFs on BSE:
1. Go to: https://www.bseindia.com/corporates/ann.html
2. In "Scrip Code" enter: `500325` (Reliance)
3. In "Category" select: "Analyst / Institutional Investor Meet"
4. Click Search
5. Find a result with "Transcript" or "Concall" in the subject
6. Download the PDF attachment
7. Save it as: `data/pdfs/RELIANCE_manual.pdf`

Repeat for:
- HDFC Bank (scrip code: `500180`) → save as `data/pdfs/HDFCBANK_manual.pdf`
- Infosys (scrip code: `500209`) → save as `data/pdfs/INFY_manual.pdf`

### Alternative — NSE:
1. Go to: https://www.nseindia.com/companies-listing/corporate-filings-announcements
2. Search by symbol (e.g. RELIANCE)
3. Filter by "Analyst/Institutional Investor Meet"
4. Download the PDF

---

## Step 4: Verify database was created

```bash
dir data\
```

You should see `filings.db` in the `data/` folder.

---

## Git Commit Commands

```bash
git add .
```

```bash
git commit -m "Ingestion pipeline: NSE + BSE fetchers, PDF downloader, SQLite deduplication"
```

```bash
git push origin main
```

---

Once done (even if NSE/BSE returned 0 results — as long as you have 3 manual PDFs in `data/pdfs/`), reply: **"Stage 2 done"**
