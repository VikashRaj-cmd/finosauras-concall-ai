from ingestion.database import _connect

with _connect() as conn:
    conn.execute("UPDATE filings SET status='extracted' WHERE nse_symbol='INFY'")
    conn.commit()
print("Reset done")
