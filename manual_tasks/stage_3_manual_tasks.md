# Manual Tasks — Stage 3: PDF Extraction

---

## Step 1: Run the extraction pipeline

```bash
python -m extraction.pipeline
```

### What to expect:
- It reads all filings with status "downloaded" from the database
- Extracts text from each PDF using pymupdf → pdfplumber → OCR (fallback chain)
- Saves clean `.txt` files in `data/transcripts/`
- Output example:
  ```
  ✅ Done. 3 transcript(s) extracted.
    Reliance Industries Ltd [Q2 FY26] → data/transcripts/RELIANCE_Q2_FY26.txt
    HDFC Bank Ltd [Q2 FY26] → data/transcripts/HDFCBANK_Q2_FY26.txt
    Infosys Ltd [Q2 FY26] → data/transcripts/INFY_Q2_FY26.txt
  ```

---

## Step 2: Verify the transcripts

Open any `.txt` file in `data/transcripts/` and check:
- Text is readable (not garbled)
- Speaker labels are visible (Moderator:, Management:, Analyst:)
- No excessive blank lines or page numbers

```bash
type data\transcripts\RELIANCE_latest.txt | more
```

---

## Step 3: If quarter shows as "latest" instead of "Q2 FY26"

That just means the quarter wasn't detected automatically from the PDF text.
It does NOT affect the pipeline — the summary will still work fine.

---

## Git Commit Commands

```bash
git add .
```

```bash
git commit -m "PDF extraction: text extractor, cleaner, transcript pipeline"
```

```bash
git push origin main
```

---

Once transcripts are in `data/transcripts/`, reply: **"Stage 3 done"**
