"""
Pydantic schemas for API request/response validation.

TODO 3: Refactoring - API Contracts
These schemas provide type safety and automatic validation for FastAPI endpoints.
"""

from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


# ============================================================================
# Note Schemas
# ============================================================================

class NoteCreate(BaseModel):
    """Request schema for creating a new note."""
    content: str = Field(..., min_length=1, description="Note content")


class NoteResponse(BaseModel):
    """Response schema for note data."""
    id: int
    content: str
    created_at: str

    @classmethod
    def from_dict(cls, data: dict) -> "NoteResponse":
        """Create NoteResponse from database dict."""
        return cls(**data)


# ============================================================================
# Action Item Schemas
# ============================================================================

class ActionItemResponse(BaseModel):
    """Response schema for a single action item."""
    id: int
    text: str
    note_id: Optional[int] = None
    done: bool = False
    created_at: str

    @classmethod
    def from_dict(cls, data: dict) -> "ActionItemResponse":
        """Create ActionItemResponse from database dict."""
        return cls(
            id=data["id"],
            text=data["text"],
            note_id=data.get("note_id"),
            done=bool(data["done"]),
            created_at=data["created_at"],
        )


# ============================================================================
# Extract Endpoint Schemas
# ============================================================================

class ExtractRequest(BaseModel):
    """Request schema for action item extraction."""
    text: str = Field(..., min_length=1, description="Text to extract action items from")
    save_note: bool = Field(default=False, description="Whether to save text as a note")


class ExtractResponse(BaseModel):
    """Response schema for extraction result."""
    note_id: Optional[int] = None
    items: list[ActionItemResponse]


# ============================================================================
# Mark Done Schema
# ============================================================================

class MarkDoneRequest(BaseModel):
    """Request schema for marking action item as done/undone."""
    done: bool = Field(default=True, description="Done status")
