from __future__ import annotations

from typing import List

from fastapi import APIRouter

from .. import db
from ..schemas import NoteCreate, NoteResponse


router = APIRouter(prefix="/notes", tags=["notes"])


# TODO 3: Refactored to use Pydantic schemas for type safety and validation
@router.post("", response_model=NoteResponse)
def create_note(payload: NoteCreate) -> NoteResponse:
    """Create a new note. Input is automatically validated by Pydantic."""
    note_id = db.insert_note(payload.content)
    note = db.get_note(note_id)
    return NoteResponse.from_dict(note)


# TODO 4: List Notes endpoint for Agentic Mode
@router.get("", response_model=List[NoteResponse])
def list_notes() -> List[NoteResponse]:
    """List all notes ordered by ID (newest first)."""
    rows = db.list_notes()
    return [NoteResponse.from_dict(row) for row in rows]


@router.get("/{note_id}", response_model=NoteResponse)
def get_single_note(note_id: int) -> NoteResponse:
    """Get a single note by ID."""
    row = db.get_note(note_id)
    return NoteResponse.from_dict(row)


