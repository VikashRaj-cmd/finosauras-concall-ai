# Manual Tasks — Stage 6: React Frontend

---

## Step 1: Make sure the backend is running

Open terminal 1 and run:
```bash
venv\Scripts\activate
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Step 2: Start the frontend dev server

Open terminal 2 and run:
```bash
cd frontend
npm run dev
```

You should see:
```
  VITE v6.x.x  ready in xxx ms
  ➜  Local:   http://localhost:5173/
```

---

## Step 3: Open the dashboard

Go to: http://localhost:5173

You should see:
- Header: "Finosauras Concall AI" with a green "Live" badge
- 3 company cards: Reliance, HDFC Bank, Infosys
- Each card shows the company name, quarter, and first TL;DR bullet

Click any card to see the full summary detail page with:
- TL;DR bullets
- Management Commentary
- Key Metrics table
- Segment Performance
- Notable Q&A
- Risks

---

## Git Commit Commands

Run in terminal 2 (frontend folder or root — both work):

```bash
git add .
```

```bash
git commit -m "React dashboard: company list, summary detail, WebSocket live badge"
```

```bash
git push origin main
```

---

Once the dashboard loads with 3 companies, reply: **"Stage 6 done"**
