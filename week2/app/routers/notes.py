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


@router.get("/{note_id}", response_model=NoteResponse)
def get_single_note(note_id: int) -> NoteResponse:
    """Get a single note by ID."""
    row = db.get_note(note_id)
    return NoteResponse.from_dict(row)


