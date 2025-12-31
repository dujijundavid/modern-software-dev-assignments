from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, JSON, DateTime, Float
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)


class ActionItem(Base):
    __tablename__ = "action_items"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)


# =============================================================================
# Agent Orchestration Models
# =============================================================================

class Agent(Base):
    """Represents an AI agent with its capabilities and configuration."""
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    capabilities = Column(JSON, default=list)  # List of capability strings
    tools = Column(JSON, default=list)  # List of tool names
    coordination_patterns = Column(JSON, default=list)  # List of pattern names
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    executions = relationship("Execution", back_populates="agent", cascade="all, delete-orphan")


class Execution(Base):
    """Represents a single agent execution with inputs, outputs, and metadata."""
    __tablename__ = "executions"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String(100), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    inputs = Column(JSON)  # Agent input parameters
    outputs = Column(JSON)  # Agent output/results
    duration_ms = Column(Integer)  # Execution duration in milliseconds
    status = Column(String(20), nullable=False, default="pending")  # pending, success, failure
    error_message = Column(Text)
    parent_execution_id = Column(Integer, ForeignKey("executions.id"), nullable=True)

    # Relationships
    agent = relationship("Agent", foreign_keys=[agent_name], primaryjoin="Agent.name == Execution.agent_name")
    parent_execution = relationship("Execution", remote_side=[id], backref="child_executions")
    workflow_execution = relationship("WorkflowExecution", back_populates="executions")


class CoordinationPattern(Base):
    """Documentation of coordination patterns with examples."""
    __tablename__ = "coordination_patterns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    diagram_url = Column(String(500))
    example_workflow_id = Column(ForeignKey("workflow_templates.id"), nullable=True)
    when_to_use = Column(Text)  # Guidance on when to use this pattern


class WorkflowTemplate(Base):
    """Pre-defined multi-agent workflow templates."""
    __tablename__ = "workflow_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    steps = Column(JSON, nullable=False)  # Array of agent calls with parameters
    coordination_pattern = Column(String(50))  # sequential, parallel, hierarchical
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    executions = relationship("WorkflowExecution", back_populates="workflow_template")


class WorkflowExecution(Base):
    """Execution instance of a workflow template."""
    __tablename__ = "workflow_executions"

    id = Column(Integer, primary_key=True, index=True)
    workflow_template_id = Column(ForeignKey("workflow_templates.id"), nullable=False)
    status = Column(String(20), default="pending")  # pending, running, success, failure
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    parameters = Column(JSON)  # Runtime parameters for the workflow

    # Relationships
    workflow_template = relationship("WorkflowTemplate", back_populates="executions")
    executions = relationship("Execution", secondary="workflow_execution_links", back_populates="workflow_execution")


class WorkflowExecutionLink(Base):
    """Junction table for workflow execution to agent execution relationship."""
    __tablename__ = "workflow_execution_links"

    workflow_execution_id = Column(ForeignKey("workflow_executions.id"), primary_key=True)
    execution_id = Column(ForeignKey("executions.id"), primary_key=True)
    step_order = Column(Integer)  # Order in the workflow
