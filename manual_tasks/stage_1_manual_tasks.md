# Manual Tasks — Stage 1: Project Setup

Complete these steps manually in your terminal before replying "Stage 1 done".

---

## Step 1: Initialize Git repository

Open terminal in `e:\finosauras-concall-ai` and run:

```bash
git init
```

---

## Step 2: Create Python virtual environment

```bash
python -m venv venv
```

Then activate it:

```bash
venv\Scripts\activate
```

You should see `(venv)` at the start of your terminal prompt.

---

## Step 3: Install all dependencies

```bash
pip install -r requirements.txt
```

This will take 2–3 minutes. Wait for it to finish completely.

---

## Step 4: Create your .env file

```bash
copy .env.example .env
```

Then open `.env` in VS Code and fill in your API key.

**Get a FREE Gemini API key:**
1. Go to https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it as: `GEMINI_API_KEY=your_actual_key_here`
5. Set `AI_PROVIDER=gemini`

Keep `TRACKED_SYMBOLS=RELIANCE,HDFCBANK,TATAMOTORS,SUNPHARMA,INFY` as is for now.

---

## Step 5: Verify folder structure

Run this to confirm everything is in place:

```bash
dir /s /b /ad
```

You should see folders: ingestion, extraction, summarization, backend, data, tests, manual_tasks

---

## Git Commit Commands for Stage 1

Run these one by one in your terminal:

```bash
git add .
```

```bash
git commit -m "Stage 1: Project setup — folder structure, dependencies, config files"
```

```bash
git push origin main
```

> Note: If `git push` fails because you haven't created a GitHub repo yet:
> 1. Go to https://github.com/new
> 2. Create a new public repo named `finosauras-concall-ai`
> 3. Run: `git remote add origin https://github.com/YOUR_USERNAME/finosauras-concall-ai.git`
> 4. Run: `git branch -M main`
> 5. Then run: `git push -u origin main`

---

Once all steps are done, reply: **"Stage 1 done"**
