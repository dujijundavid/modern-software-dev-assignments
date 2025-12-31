"""Agent Registry API endpoints."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Agent, CoordinationPattern

router = APIRouter()


@router.get("/agents")
def list_agents(
    capability: Optional[str] = None,
    pattern: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all agents with optional filtering by capability or coordination pattern."""
    query = db.query(Agent)

    if capability:
        query = query.filter(Agent.capabilities.contains(capability))
    if pattern:
        query = query.filter(Agent.coordination_patterns.contains(pattern))

    agents = query.order_by(Agent.name).all()
    return [
        {
            "id": agent.id,
            "name": agent.name,
            "description": agent.description,
            "capabilities": agent.capabilities or [],
            "tools": agent.tools or [],
            "coordination_patterns": agent.coordination_patterns or [],
            "created_at": agent.created_at.isoformat() if agent.created_at else None,
        }
        for agent in agents
    ]


@router.get("/agents/{agent_id}")
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    """Get details of a specific agent."""
    agent = db.get(Agent, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    return {
        "id": agent.id,
        "name": agent.name,
        "description": agent.description,
        "capabilities": agent.capabilities or [],
        "tools": agent.tools or [],
        "coordination_patterns": agent.coordination_patterns or [],
        "created_at": agent.created_at.isoformat() if agent.created_at else None,
    }


@router.post("/agents")
def create_agent(
    name: str,
    description: str,
    capabilities: List[str],
    tools: List[str],
    coordination_patterns: List[str],
    db: Session = Depends(get_db)
):
    """Register a new agent."""
    # Check if agent already exists
    existing = db.query(Agent).filter(Agent.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Agent '{name}' already exists")

    agent = Agent(
        name=name,
        description=description,
        capabilities=capabilities,
        tools=tools,
        coordination_patterns=coordination_patterns
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)

    return {
        "id": agent.id,
        "name": agent.name,
        "description": agent.description,
        "capabilities": agent.capabilities,
        "tools": agent.tools,
        "coordination_patterns": agent.coordination_patterns,
    }


@router.delete("/agents/{agent_id}")
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    """Delete an agent."""
    agent = db.get(Agent, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    db.delete(agent)
    db.commit()

    return {"message": f"Agent '{agent.name}' deleted"}


@router.get("/patterns")
def list_patterns(db: Session = Depends(get_db)):
    """List all coordination patterns with documentation."""
    patterns = db.query(CoordinationPattern).order_by(CoordinationPattern.name).all()
    return [
        {
            "id": pattern.id,
            "name": pattern.name,
            "description": pattern.description,
            "diagram_url": pattern.diagram_url,
            "example_workflow_id": pattern.example_workflow_id,
            "when_to_use": pattern.when_to_use,
        }
        for pattern in patterns
    ]


@router.get("/patterns/{pattern_id}")
def get_pattern(pattern_id: int, db: Session = Depends(get_db)):
    """Get details of a specific coordination pattern."""
    pattern = db.get(CoordinationPattern, pattern_id)
    if not pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")

    return {
        "id": pattern.id,
        "name": pattern.name,
        "description": pattern.description,
        "diagram_url": pattern.diagram_url,
        "example_workflow_id": pattern.example_workflow_id,
        "when_to_use": pattern.when_to_use,
    }
