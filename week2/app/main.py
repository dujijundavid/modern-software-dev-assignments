from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .db import init_db
from .routers import action_items, notes
from . import db

init_db()

app = FastAPI(title="Action Item Extractor")


@app.exception_handler(db.NotFoundError)
async def notfound_error_handler(request, exc: db.NotFoundError):
    """Handle NotFoundError - return 404 status."""
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(db.DatabaseError)
async def database_error_handler(request, exc: db.DatabaseError):
    """Handle DatabaseError - return 500 status."""
    return JSONResponse(
        status_code=500,
        content={"detail": exc.message},
    )


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    html_path = Path(__file__).resolve().parents[1] / "frontend" / "index.html"
    return html_path.read_text(encoding="utf-8")


app.include_router(notes.router)
app.include_router(action_items.router)


static_dir = Path(__file__).resolve().parents[1] / "frontend"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")