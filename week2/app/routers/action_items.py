from __future__ import annotations

from typing import List, Optional
import logging

from fastapi import APIRouter, HTTPException

from .. import db
from ..services.extract import extract_action_items, extract_action_items_llm
from ..schemas import (
    ExtractRequest,
    ExtractResponse,
    ActionItemResponse,
    MarkDoneRequest,
)

# TODO 3: Added proper logging instead of print statements
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/action-items", tags=["action-items"])


# TODO 3: Refactored to use Pydantic schemas, removed debug prints
@router.post("/extract", response_model=ExtractResponse)
def extract(payload: ExtractRequest) -> ExtractResponse:
    """Extract action items from text using heuristic patterns."""
    logger.info(f"Extracting action items from text (length: {len(payload.text)} chars)")
    
    note_id: Optional[int] = None
    if payload.save_note:
        note_id = db.insert_note(payload.text)
        logger.info(f"Saved note with ID: {note_id}")

    items = extract_action_items(payload.text)
    ids = db.insert_action_items(items, note_id=note_id)
    
    logger.info(f"Extracted {len(items)} action items")
    
    # TODO 3: Fetch the actual action items from DB to get created_at timestamps
    created_items = db.list_action_items(note_id=note_id)
    # Filter to only the items we just created (by ID)
    created_items_map = {item["id"]: item for item in created_items}
    
    return ExtractResponse(
        note_id=note_id,
        items=[
            ActionItemResponse(
                id=item_id,
                text=created_items_map[item_id]["text"],
                note_id=created_items_map[item_id]["note_id"],
                done=bool(created_items_map[item_id]["done"]),
                created_at=created_items_map[item_id]["created_at"],
            )
            for item_id in ids
        ],
    )


@router.get("", response_model=List[ActionItemResponse])
def list_all(note_id: Optional[int] = None) -> List[ActionItemResponse]:
    """List all action items, optionally filtered by note_id."""
    rows = db.list_action_items(note_id=note_id)
    return [
        ActionItemResponse(
            id=r["id"],
            note_id=r["note_id"],
            text=r["text"],
            done=bool(r["done"]),
            created_at=r["created_at"],
        )
        for r in rows
    ]


# TODO 4: New LLM-powered extraction endpoint
@router.post("/extract-llm", response_model=ExtractResponse)
def extract_llm(payload: ExtractRequest) -> ExtractResponse:
    """Extract action items using LLM (more intelligent, works with free-form text)."""
    logger.info(f"Extracting action items with LLM from text (length: {len(payload.text)} chars)")
    
    note_id: Optional[int] = None
    if payload.save_note:
        note_id = db.insert_note(payload.text)
        logger.info(f"Saved note with ID: {note_id}")

    items = extract_action_items_llm(payload.text)
    ids = db.insert_action_items(items, note_id=note_id)
    
    logger.info(f"LLM extracted {len(items)} action items")
    
    # Fetch the actual action items from DB to get created_at timestamps
    created_items = db.list_action_items(note_id=note_id)
    created_items_map = {item["id"]: item for item in created_items}
    
    return ExtractResponse(
        note_id=note_id,
        items=[
            ActionItemResponse(
                id=item_id,
                text=created_items_map[item_id]["text"],
                note_id=created_items_map[item_id]["note_id"],
                done=bool(created_items_map[item_id]["done"]),
                created_at=created_items_map[item_id]["created_at"],
            )
            for item_id in ids
        ],
    )


@router.post("/{action_item_id}/done")
def mark_done(action_item_id: int, payload: MarkDoneRequest) -> dict:
    """Mark an action item as done or undone."""
    db.mark_action_item_done(action_item_id, payload.done)
    logger.info(f"Marked action item {action_item_id} as done={payload.done}")
    return {"id": action_item_id, "done": payload.done}


