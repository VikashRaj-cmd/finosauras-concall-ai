# Manual Tasks — Stage 2: NSE + BSE Ingestion

---

## Step 1: Re-run the pipeline with fixed API endpoints

```bash
python -m ingestion.pipeline
```

NSE/BSE may still return 0 results — that is fine. The APIs block bots aggressively.
The important thing is no crash and `data/filings.db` exists.

---

## Step 2: Manually download 3 real concall PDFs (REQUIRED)

You MUST have at least 3 real PDFs in `data/pdfs/` before Stage 3.

### Option A — Download from BSE website (easiest)

1. Go to: https://www.bseindia.com/corporates/ann.html
2. Enter scrip code and select category as shown below:

| Company | Scrip Code | What to search |
|---|---|---|
| Reliance Industries | 500325 | Category: "Analyst / Institutional Investor Meet" |
| HDFC Bank | 500180 | Category: "Analyst / Institutional Investor Meet" |
| Infosys | 500209 | Category: "Analyst / Institutional Investor Meet" |

3. Click Search → find a result with "Transcript" or "Concall" in the subject
4. Click the PDF icon to download
5. Save files as:
   - `data/pdfs/RELIANCE_manual.pdf`
   - `data/pdfs/HDFCBANK_manual.pdf`
   - `data/pdfs/INFY_manual.pdf`

### Option B — Download from NSE website

1. Go to: https://www.nseindia.com/companies-listing/corporate-filings-announcements
2. In "Symbol" type: RELIANCE → press Enter
3. In "Category" select: "Analyst/Institutional Investor Meet"
4. Find a PDF with "transcript" in the name → download it
5. Repeat for HDFCBANK and INFY

### Option C — Direct BSE search links (fastest)

Open these URLs directly in your browser:

- Reliance: https://www.bseindia.com/corporates/ann.html?scrip=500325&Category=41
- HDFC Bank: https://www.bseindia.com/corporates/ann.html?scrip=500180&Category=41
- Infosys: https://www.bseindia.com/corporates/ann.html?scrip=500209&Category=41

---

## Step 3: Register the manually downloaded PDFs in the database

After saving the PDFs, run this one-time script to register them:

```bash
python -c "
from ingestion.database import init_db, save_filing
init_db()

filings = [
    {'company': 'Reliance Industries Ltd', 'nse_symbol': 'RELIANCE', 'bse_code': '500325', 'source': 'BSE', 'pdf_url': 'manual', 'quarter': ''},
    {'company': 'HDFC Bank Ltd', 'nse_symbol': 'HDFCBANK', 'bse_code': '500180', 'source': 'BSE', 'pdf_url': 'manual_hdfc', 'quarter': ''},
    {'company': 'Infosys Ltd', 'nse_symbol': 'INFY', 'bse_code': '500209', 'source': 'BSE', 'pdf_url': 'manual_infy', 'quarter': ''},
]

paths = [
    'data/pdfs/RELIANCE_manual.pdf',
    'data/pdfs/HDFCBANK_manual.pdf',
    'data/pdfs/INFY_manual.pdf',
]

for filing, path in zip(filings, paths):
    save_filing(filing, pdf_path=path, status='downloaded')
    print(f'Registered: {filing[\"company\"]}')
"
```

---

## Step 4: Verify

```bash
python -c "from ingestion.database import get_all_filings; [print(f['company'], f['pdf_path']) for f in get_all_filings()]"
```

You should see 3 companies listed with their PDF paths.

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

Once you have 3 PDFs in `data/pdfs/` and the commit is pushed, reply: **"Stage 2 done"**
