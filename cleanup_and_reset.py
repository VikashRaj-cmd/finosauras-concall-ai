import os
from pathlib import Path
from ingestion.database import _connect

# Delete stale _latest files
for pattern_dir, pattern in [
    ("data/transcripts", "*_latest.txt"),
    ("data/summaries/json", "*_latest.json"),
    ("data/summaries/markdown", "*_latest.md"),
]:
    for f in Path(pattern_dir).glob(pattern):
        f.unlink()
        print(f"Deleted: {f}")

# Reset TATAMOTORS and SUNPHARMA to 'extracted' so summarization re-runs
conn = _connect()
conn.execute("UPDATE filings SET status='extracted' WHERE nse_symbol IN ('TATAMOTORS', 'SUNPHARMA')")
conn.commit()
conn.close()
print("Reset status to extracted — ready for summarization.")
