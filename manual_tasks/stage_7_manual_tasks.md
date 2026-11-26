# Manual Tasks — Stage 7: Docker + Final Cleanup

---

## Step 1: Verify final project structure

```bash
dir /b
```

You should see: backend, data, extraction, frontend, ingestion, summarization, tests, manual_tasks,
.env.example, .gitignore, docker-compose.yml, Dockerfile.backend, README.md, requirements.txt

---

## Step 2: Test Docker (optional but impressive)

If you have Docker Desktop installed:

```bash
docker compose up --build
```

Then open http://localhost:3000

If Docker is not installed, skip this — the manual startup works fine.

---

## Step 3: Final git commit

```bash
git add .
```

```bash
git commit -m "Docker setup, final README, project cleanup"
```

```bash
git push origin main
```

---

## Step 4: Write your submission email reply

Reply to dy@saras.market with:

Subject: Re: Finosauras Software Engineer Intern — Take-Home Assignment

---

Hi Dhrumit,

Please find my submission for the take-home assignment.

GitHub: https://github.com/YOUR_USERNAME/finosauras-concall-ai

Approach (2–3 sentences):
I built a 4-stage pipeline — NSE/BSE announcement polling → PDF extraction (pymupdf with OCR fallback) → map-reduce AI summarization using Gemini → FastAPI backend with WebSocket streaming to a React dashboard. Long transcripts are handled by splitting into ~3000-token chunks, summarizing each independently, then merging into a structured JSON (map-reduce). The watcher runs as a background asyncio task and broadcasts each new summary to all connected clients in real time.

I confirm I am open to relocating to Surat and can join by [YOUR DATE].

Best regards,
[Your Name]

---

You're done! 🎉
