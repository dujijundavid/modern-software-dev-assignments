from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .db import apply_seed_if_needed, engine
from .models import Base
from .routers import action_items as action_items_router
from .routers import notes as notes_router
from .routers import agents as agents_router
from .routers import executions as executions_router
from .routers import workflows as workflows_router

app = FastAPI(
    title="Agent Orchestration System",
    description="Multi-Agent Execution Tracker - Week 5: Multi-Agent Workflows with Claude Code"
)

# Ensure data dir exists
Path("data").mkdir(parents=True, exist_ok=True)

# Mount static frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.on_event("startup")
def startup_event() -> None:
    Base.metadata.create_all(bind=engine)
    apply_seed_if_needed()


@app.get("/")
async def root() -> FileResponse:
    return FileResponse("frontend/index.html")


# Routers
app.include_router(notes_router.router)
app.include_router(action_items_router.router)
app.include_router(agents_router.router, prefix="/api", tags=["agents"])
app.include_router(executions_router.router, prefix="/api", tags=["executions"])
app.include_router(workflows_router.router, prefix="/api", tags=["workflows"])
