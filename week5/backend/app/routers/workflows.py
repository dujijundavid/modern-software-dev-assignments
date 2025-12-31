"""Workflow Template API endpoints."""
from datetime import datetime
from typing import List, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import WorkflowTemplate, WorkflowExecution, Execution, WorkflowExecutionLink

router = APIRouter()


@router.get("/workflows")
def list_workflows(db: Session = Depends(get_db)):
    """List all workflow templates."""
    workflows = db.query(WorkflowTemplate).order_by(WorkflowTemplate.name).all()
    return [
        {
            "id": w.id,
            "name": w.name,
            "description": w.description,
            "coordination_pattern": w.coordination_pattern,
            "steps": w.steps,
            "created_at": w.created_at.isoformat() if w.created_at else None,
        }
        for w in workflows
    ]


@router.get("/workflows/{workflow_id}")
def get_workflow(workflow_id: int, db: Session = Depends(get_db)):
    """Get details of a specific workflow template."""
    workflow = db.get(WorkflowTemplate, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    return {
        "id": workflow.id,
        "name": workflow.name,
        "description": workflow.description,
        "coordination_pattern": workflow.coordination_pattern,
        "steps": workflow.steps,
        "created_at": workflow.created_at.isoformat() if workflow.created_at else None,
    }


@router.post("/workflows")
def create_workflow(
    name: str,
    description: str,
    steps: List[Dict],
    coordination_pattern: str,
    db: Session = Depends(get_db)
):
    """Create a new workflow template.

    Steps format:
    [
        {"agent": "TestAgent", "params": {"test_path": "..."}},
        {"agent": "CodeAgent", "params": {"feature": "..."}},
    ]
    """
    # Check if workflow already exists
    existing = db.query(WorkflowTemplate).filter(WorkflowTemplate.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Workflow '{name}' already exists")

    workflow = WorkflowTemplate(
        name=name,
        description=description,
        steps=steps,
        coordination_pattern=coordination_pattern
    )
    db.add(workflow)
    db.commit()
    db.refresh(workflow)

    return {
        "id": workflow.id,
        "name": workflow.name,
        "description": workflow.description,
        "coordination_pattern": workflow.coordination_pattern,
        "steps": workflow.steps,
    }


@router.post("/workflows/{workflow_id}/execute")
def execute_workflow(
    workflow_id: int,
    parameters: Optional[Dict] = None,
    db: Session = Depends(get_db)
):
    """
    Execute a workflow template.

    This creates a WorkflowExecution record and returns it.
    Actual agent orchestration happens outside the API (via Claude Code).
    """
    workflow = db.get(WorkflowTemplate, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    # Create workflow execution record
    workflow_exec = WorkflowExecution(
        workflow_template_id=workflow_id,
        status="running",
        parameters=parameters or {}
    )
    db.add(workflow_exec)
    db.commit()
    db.refresh(workflow_exec)

    return {
        "workflow_execution_id": workflow_exec.id,
        "workflow_id": workflow_id,
        "workflow_name": workflow.name,
        "status": "running",
        "steps": workflow.steps,
        "parameters": parameters or {},
    }


@router.get("/workflows/executions/{execution_id}")
def get_workflow_execution(execution_id: int, db: Session = Depends(get_db)):
    """Get details of a workflow execution."""
    workflow_exec = db.get(WorkflowExecution, execution_id)
    if not workflow_exec:
        raise HTTPException(status_code=404, detail="Workflow execution not found")

    # Get associated agent executions
    links = db.query(WorkflowExecutionLink).filter(
        WorkflowExecutionLink.workflow_execution_id == execution_id
    ).order_by(WorkflowExecutionLink.step_order).all()

    execution_ids = [link.execution_id for link in links]
    agent_executions = db.query(Execution).filter(Execution.id.in_(execution_ids)).all()

    return {
        "id": workflow_exec.id,
        "workflow_template_id": workflow_exec.workflow_template_id,
        "status": workflow_exec.status,
        "started_at": workflow_exec.started_at.isoformat() if workflow_exec.started_at else None,
        "completed_at": workflow_exec.completed_at.isoformat() if workflow_exec.completed_at else None,
        "parameters": workflow_exec.parameters,
        "executions": [
            {
                "id": e.id,
                "agent_name": e.agent_name,
                "status": e.status,
                "timestamp": e.timestamp.isoformat() if e.timestamp else None,
                "duration_ms": e.duration_ms,
            }
            for e in agent_executions
        ],
    }


@router.post("/workflows/executions/{execution_id}/complete")
def complete_workflow_execution(
    execution_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """Mark a workflow execution as complete."""
    workflow_exec = db.get(WorkflowExecution, execution_id)
    if not workflow_exec:
        raise HTTPException(status_code=404, detail="Workflow execution not found")

    workflow_exec.status = status
    workflow_exec.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(workflow_exec)

    return {
        "id": workflow_exec.id,
        "status": workflow_exec.status,
        "completed_at": workflow_exec.completed_at.isoformat() if workflow_exec.completed_at else None,
    }


@router.post("/workflows/executions/{execution_id}/add-step")
def add_execution_to_workflow(
    execution_id: int,
    agent_execution_id: int,
    step_order: int,
    db: Session = Depends(get_db)
):
    """
    Link an agent execution to a workflow execution.

    Called when an agent completes a step in the workflow.
    """
    workflow_exec = db.get(WorkflowExecution, execution_id)
    if not workflow_exec:
        raise HTTPException(status_code=404, detail="Workflow execution not found")

    agent_exec = db.get(Execution, agent_execution_id)
    if not agent_exec:
        raise HTTPException(status_code=404, detail="Agent execution not found")

    link = WorkflowExecutionLink(
        workflow_execution_id=execution_id,
        execution_id=agent_execution_id,
        step_order=step_order
    )
    db.add(link)
    db.commit()

    return {
        "message": "Agent execution linked to workflow",
        "workflow_execution_id": execution_id,
        "agent_execution_id": agent_execution_id,
        "step_order": step_order,
    }
