from ingestion.database import _connect

conn = _connect()
conn.execute("UPDATE filings SET status='downloaded' WHERE nse_symbol IN ('TATAMOTORS', 'SUNPHARMA')")
conn.commit()
conn.close()
print("Reset done")
