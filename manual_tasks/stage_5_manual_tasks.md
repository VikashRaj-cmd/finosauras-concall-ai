# Manual Tasks — Stage 5: FastAPI Backend + WebSocket

---

## Step 1: Start the backend server

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO: Uvicorn running on http://0.0.0.0:8000
INFO: Watcher started. Polling every 300s.
INFO: Finosauras Concall AI backend started.
```

---

## Step 2: Test the REST API

Open these URLs in your browser:

- All summaries: http://localhost:8000/api/summaries
- Reliance summary: http://localhost:8000/api/summaries/RELIANCE
- HDFC markdown: http://localhost:8000/api/summaries/HDFCBANK/markdown
- All filings: http://localhost:8000/api/filings
- Health check: http://localhost:8000/health
- Auto docs: http://localhost:8000/docs

---

## Step 3: Test the WebSocket

Open browser console on any tab and run:

```javascript
const ws = new WebSocket("ws://localhost:8000/ws");
ws.onmessage = (e) => console.log("New summary:", JSON.parse(e.data));
ws.onopen = () => console.log("WebSocket connected!");
```

You should see: `WebSocket connected!`

---

## Git Commit Commands

```bash
git add .
```

```bash
git commit -m "FastAPI backend: REST endpoints, WebSocket, background watcher"
```

```bash
git push origin main
```

---

Once the server starts and http://localhost:8000/api/summaries returns data, reply: **"Stage 5 done"**
