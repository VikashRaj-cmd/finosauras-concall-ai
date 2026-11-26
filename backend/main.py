import asyncio
import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import router
from backend.websocket import manager

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

POLL_INTERVAL = int(os.getenv("POLL_INTERVAL_SECONDS", "300"))

app = FastAPI(title="Finosauras Concall AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            await ws.receive_text()  # keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(ws)


async def _watcher_loop():
    """
    Background task: polls NSE/BSE every POLL_INTERVAL seconds,
    runs extraction + summarization on new filings,
    and broadcasts each new summary over WebSocket.
    """
    # Import here to avoid circular imports at startup
    from ingestion.pipeline import run_ingestion
    from extraction.pipeline import run_extraction
    from summarization.pipeline import run_summarization

    logger.info(f"Watcher started. Polling every {POLL_INTERVAL}s.")

    while True:
        try:
            logger.info("Watcher: checking for new filings...")
            new_filings = run_ingestion()

            if new_filings:
                extracted = run_extraction(new_filings)
                summaries = run_summarization(extracted)

                for summary in summaries:
                    await manager.broadcast(summary)
                    logger.info(f"Broadcast: {summary.get('company')}")
            else:
                logger.info("Watcher: no new filings.")

        except Exception as e:
            logger.error(f"Watcher error: {e}")

        await asyncio.sleep(POLL_INTERVAL)


@app.on_event("startup")
async def startup():
    asyncio.create_task(_watcher_loop())
    logger.info("Finosauras Concall AI backend started.")


@app.get("/health")
def health():
    return {"status": "ok"}
