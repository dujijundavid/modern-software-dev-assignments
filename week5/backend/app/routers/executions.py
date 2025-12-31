"""Agent Execution API endpoints."""
from datetime import datetime
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Execution

router = APIRouter()


@router.get("/executions")
def list_executions(
    agent_name: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = Query(100, le=500),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List agent executions with optional filtering."""
    query = db.query(Execution)

    if agent_name:
        query = query.filter(Execution.agent_name == agent_name)
    if status:
        query = query.filter(Execution.status == status)
    if start_date:
        try:
            start = datetime.fromisoformat(start_date)
            query = query.filter(Execution.timestamp >= start)
        except ValueError:
            pass
    if end_date:
        try:
            end = datetime.fromisoformat(end_date)
            query = query.filter(Execution.timestamp <= end)
        except ValueError:
            pass

    total = query.count()
    executions = query.order_by(Execution.timestamp.desc()).offset(offset).limit(limit).all()

    return {
        "items": [
            {
                "id": e.id,
                "agent_name": e.agent_name,
                "timestamp": e.timestamp.isoformat() if e.timestamp else None,
                "inputs": e.inputs,
                "outputs": e.outputs,
                "duration_ms": e.duration_ms,
                "status": e.status,
                "error_message": e.error_message,
                "parent_execution_id": e.parent_execution_id,
            }
            for e in executions
        ],
        "total": total,
        "offset": offset,
        "limit": limit,
    }


@router.get("/executions/timeline")
def get_execution_timeline(
    agent_name: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get execution timeline with hierarchical handoff relationships.

    Returns a tree structure showing agent executions and their handoffs.
    """
    query = db.query(Execution)

    if agent_name:
        query = query.filter(Execution.agent_name == agent_name)
    if start_date:
        try:
            start = datetime.fromisoformat(start_date)
            query = query.filter(Execution.timestamp >= start)
        except ValueError:
            pass
    if end_date:
        try:
            end = datetime.fromisoformat(end_date)
            query = query.filter(Execution.timestamp <= end)
        except ValueError:
            pass

    executions = query.order_by(Execution.timestamp.asc()).all()

    # Build hierarchical structure
    def build_tree(parent_id=None):
        children = [e for e in executions if e.parent_execution_id == parent_id]
        return [
            {
                "id": e.id,
                "agent_name": e.agent_name,
                "timestamp": e.timestamp.isoformat() if e.timestamp else None,
                "duration_ms": e.duration_ms,
                "status": e.status,
                "children": build_tree(e.id),
            }
            for e in children
        ]

    return build_tree()


@router.get("/executions/graph")
def get_execution_graph(
    agent_name: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get execution data for graph visualization.

    Returns nodes (agents) and edges (handoffs) with metadata.
    """
    query = db.query(Execution)

    if agent_name:
        query = query.filter(Execution.agent_name == agent_name)
    if start_date:
        try:
            start = datetime.fromisoformat(start_date)
            query = query.filter(Execution.timestamp >= start)
        except ValueError:
            pass
    if end_date:
        try:
            end = datetime.fromisoformat(end_date)
            query = query.filter(Execution.timestamp <= end)
        except ValueError:
            pass

    executions = query.all()

    # Build nodes and edges
    nodes = {}
    edges = []

    for e in executions:
        # Count executions per agent
        if e.agent_name not in nodes:
            nodes[e.agent_name] = {"count": 0, "success": 0, "failure": 0}
        nodes[e.agent_name]["count"] += 1
        if e.status == "success":
            nodes[e.agent_name]["success"] += 1
        elif e.status == "failure":
            nodes[e.agent_name]["failure"] += 1

        # Build edges for handoffs
        if e.parent_execution_id:
            parent = next((p for p in executions if p.id == e.parent_execution_id), None)
            if parent:
                edge_key = f"{parent.agent_name}->{e.agent_name}"
                existing = next((edge for edge in edges if edge["source"] == parent.agent_name and edge["target"] == e.agent_name), None)
                if existing:
                    existing["count"] += 1
                    if e.status == "success":
                        existing["success"] += 1
                    else:
                        existing["failure"] += 1
                else:
                    edges.append({
                        "source": parent.agent_name,
                        "target": e.agent_name,
                        "count": 1,
                        "success": 1 if e.status == "success" else 0,
                        "failure": 1 if e.status == "failure" else 0,
                    })

    return {
        "nodes": [
            {
                "id": agent_name,
                "count": data["count"],
                "success": data["success"],
                "failure": data["failure"],
            }
            for agent_name, data in nodes.items()
        ],
        "edges": edges,
    }


@router.get("/executions/{execution_id}")
def get_execution(execution_id: int, db: Session = Depends(get_db)):
    """Get details of a specific execution."""
    execution = db.get(Execution, execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")

    return {
        "id": execution.id,
        "agent_name": execution.agent_name,
        "timestamp": execution.timestamp.isoformat() if execution.timestamp else None,
        "inputs": execution.inputs,
        "outputs": execution.outputs,
        "duration_ms": execution.duration_ms,
        "status": execution.status,
        "error_message": execution.error_message,
        "parent_execution_id": execution.parent_execution_id,
    }


@router.post("/executions")
def create_execution(
    agent_name: str,
    inputs: Dict,
    parent_execution_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Log a new agent execution."""
    execution = Execution(
        agent_name=agent_name,
        inputs=inputs,
        parent_execution_id=parent_execution_id,
        status="pending"
    )
    db.add(execution)
    db.commit()
    db.refresh(execution)

    return {
        "id": execution.id,
        "agent_name": execution.agent_name,
        "timestamp": execution.timestamp.isoformat() if execution.timestamp else None,
        "status": execution.status,
    }


@router.post("/executions/{execution_id}/complete")
def complete_execution(
    execution_id: int,
    outputs: Dict,
    duration_ms: int,
    status: str,
    error_message: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Mark an execution as complete with results."""
    execution = db.get(Execution, execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")

    execution.outputs = outputs
    execution.duration_ms = duration_ms
    execution.status = status
    execution.error_message = error_message

    db.commit()
    db.refresh(execution)

    return {
        "id": execution.id,
        "status": execution.status,
        "duration_ms": execution.duration_ms,
    }


@router.get("/metrics")
def get_metrics(
    agent_name: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get agent performance metrics."""
    query = db.query(Execution)

    if agent_name:
        query = query.filter(Execution.agent_name == agent_name)
    if start_date:
        try:
            start = datetime.fromisoformat(start_date)
            query = query.filter(Execution.timestamp >= start)
        except ValueError:
            pass
    if end_date:
        try:
            end = datetime.fromisoformat(end_date)
            query = query.filter(Execution.timestamp <= end)
        except ValueError:
            pass

    executions = query.all()

    if not executions:
        return {
            "total_executions": 0,
            "success_rate": 0,
            "average_duration_ms": 0,
            "executions_by_agent": {},
        }

    total = len(executions)
    successful = len([e for e in executions if e.status == "success"])
    total_duration = sum(e.duration_ms or 0 for e in executions)

    # Count by agent
    by_agent = {}
    for e in executions:
        if e.agent_name not in by_agent:
            by_agent[e.agent_name] = {"total": 0, "success": 0, "duration": 0}
        by_agent[e.agent_name]["total"] += 1
        if e.status == "success":
            by_agent[e.agent_name]["success"] += 1
        by_agent[e.agent_name]["duration"] += e.duration_ms or 0

    return {
        "total_executions": total,
        "success_rate": round(successful / total * 100, 2) if total > 0 else 0,
        "average_duration_ms": round(total_duration / total) if total > 0 else 0,
        "executions_by_agent": {
            agent: {
                "total": data["total"],
                "success_rate": round(data["success"] / data["total"] * 100, 2) if data["total"] > 0 else 0,
                "average_duration_ms": round(data["duration"] / data["total"]) if data["total"] > 0 else 0,
            }
            for agent, data in by_agent.items()
        },
    }
