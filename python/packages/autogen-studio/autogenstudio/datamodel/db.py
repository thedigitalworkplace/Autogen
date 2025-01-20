# defines how core data types in autogenstudio are serialized and stored in the database

from datetime import datetime
from enum import Enum
from typing import List, Optional, Tuple, Type, Union
from uuid import UUID, uuid4

from loguru import logger
from pydantic import BaseModel
from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlmodel import JSON, Column, DateTime, Field, Relationship, SQLModel, func

from .types import (
    AgentConfig,
    MessageConfig,
    MessageMeta,
    ModelConfig,
    TeamConfig,
    TeamResult,
    ToolConfig,
)

# added for python3.11 and sqlmodel 0.0.22 incompatibility
if hasattr(SQLModel, "model_config"):
    SQLModel.model_config["protected_namespaces"] = ()
elif hasattr(SQLModel, "Config"):

    class CustomSQLModel(SQLModel):
        class Config:
            protected_namespaces = ()

    SQLModel = CustomSQLModel
else:
    logger.warning("Unable to set protected_namespaces.")

# pylint: disable=protected-access


class ComponentTypes(Enum):
    TEAM = "team"
    AGENT = "agent"
    MODEL = "model"
    TOOL = "tool"

    @property
    def model_class(self) -> Type[SQLModel]:
        return {
            ComponentTypes.TEAM: Team,
            ComponentTypes.AGENT: Agent,
            ComponentTypes.MODEL: Model,
            ComponentTypes.TOOL: Tool,
        }[self]


class LinkTypes(Enum):
    AGENT_MODEL = "agent_model"
    AGENT_TOOL = "agent_tool"
    TEAM_AGENT = "team_agent"

    @property
    # type: ignore
    def link_config(self) -> Tuple[Type[SQLModel], Type[SQLModel], Type[SQLModel]]:
        return {
            LinkTypes.AGENT_MODEL: (Agent, Model, AgentModelLink),
            LinkTypes.AGENT_TOOL: (Agent, Tool, AgentToolLink),
            LinkTypes.TEAM_AGENT: (Team, Agent, TeamAgentLink),
        }[self]

    @property
    def primary_class(self) -> Type[SQLModel]:  # type: ignore
        return self.link_config[0]

    @property
    def secondary_class(self) -> Type[SQLModel]:  # type: ignore
        return self.link_config[1]

    @property
    def link_table(self) -> Type[SQLModel]:  # type: ignore
        return self.link_config[2]


# link models
class AgentToolLink(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("agent_id", "sequence", name="unique_agent_tool_sequence"),
        {"sqlite_autoincrement": True},
    )
    agent_id: int = Field(default=None, primary_key=True, foreign_key="agent.id")
    tool_id: int = Field(default=None, primary_key=True, foreign_key="tool.id")
    sequence: Optional[int] = Field(default=0, primary_key=True)


class AgentModelLink(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("agent_id", "sequence", name="unique_agent_tool_sequence"),
        {"sqlite_autoincrement": True},
    )
    agent_id: int = Field(default=None, primary_key=True, foreign_key="agent.id")
    model_id: int = Field(default=None, primary_key=True, foreign_key="model.id")
    sequence: Optional[int] = Field(default=0, primary_key=True)


class TeamAgentLink(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("agent_id", "sequence", name="unique_agent_tool_sequence"),
        {"sqlite_autoincrement": True},
    )
    team_id: int = Field(default=None, primary_key=True, foreign_key="team.id")
    agent_id: int = Field(default=None, primary_key=True, foreign_key="agent.id")
    sequence: Optional[int] = Field(default=0, primary_key=True)


# database models


class Tool(SQLModel, table=True):
    __table_args__ = {"sqlite_autoincrement": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )  # pylint: disable=not-callable
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now()),
    )  # pylint: disable=not-callable
    user_id: Optional[str] = None
    version: Optional[str] = "0.0.1"
    config: Union[ToolConfig, dict] = Field(sa_column=Column(JSON))
    agents: List["Agent"] = Relationship(
        back_populates="tools", link_model=AgentToolLink
    )


class Model(SQLModel, table=True):
    __table_args__ = {"sqlite_autoincrement": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )  # pylint: disable=not-callable
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now()),
    )  # pylint: disable=not-callable
    user_id: Optional[str] = None
    version: Optional[str] = "0.0.1"
    config: Union[ModelConfig, dict] = Field(sa_column=Column(JSON))
    agents: List["Agent"] = Relationship(
        back_populates="models", link_model=AgentModelLink
    )


class Team(SQLModel, table=True):
    __table_args__ = {"sqlite_autoincrement": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )  # pylint: disable=not-callable
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now()),
    )  # pylint: disable=not-callable
    user_id: Optional[str] = None
    version: Optional[str] = "0.0.1"
    config: Union[TeamConfig, dict] = Field(sa_column=Column(JSON))
    agents: List["Agent"] = Relationship(
        back_populates="teams", link_model=TeamAgentLink
    )


class Agent(SQLModel, table=True):
    __table_args__ = {"sqlite_autoincrement": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )  # pylint: disable=not-callable
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now()),
    )  # pylint: disable=not-callable
    user_id: Optional[str] = None
    version: Optional[str] = "0.0.1"
    config: Union[AgentConfig, dict] = Field(sa_column=Column(JSON))
    tools: List[Tool] = Relationship(back_populates="agents", link_model=AgentToolLink)
    models: List[Model] = Relationship(
        back_populates="agents", link_model=AgentModelLink
    )
    teams: List[Team] = Relationship(back_populates="agents", link_model=TeamAgentLink)


class Message(SQLModel, table=True):
    __table_args__ = {"sqlite_autoincrement": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )  # pylint: disable=not-callable
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now()),
    )  # pylint: disable=not-callable
    user_id: Optional[str] = None
    version: Optional[str] = "0.0.1"
    config: Union[MessageConfig, dict] = Field(
        default_factory=MessageConfig, sa_column=Column(JSON)
    )
    session_id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, ForeignKey("session.id", ondelete="CASCADE")),
    )
    run_id: Optional[UUID] = Field(default=None, foreign_key="run.id")
    message_meta: Optional[Union[MessageMeta, dict]] = Field(
        default={}, sa_column=Column(JSON)
    )


class Session(SQLModel, table=True):
    __table_args__ = {"sqlite_autoincrement": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )  # pylint: disable=not-callable
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now()),
    )  # pylint: disable=not-callable
    user_id: Optional[str] = None
    version: Optional[str] = "0.0.1"
    team_id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, ForeignKey("team.id", ondelete="CASCADE")),
    )
    name: Optional[str] = None


class RunStatus(str, Enum):
    CREATED = "created"
    ACTIVE = "active"
    COMPLETE = "complete"
    ERROR = "error"
    STOPPED = "stopped"


class Run(SQLModel, table=True):
    """Represents a single execution run within a session"""

    __table_args__ = {"sqlite_autoincrement": True}

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now()),
    )
    session_id: Optional[int] = Field(
        default=None,
        sa_column=Column(
            Integer, ForeignKey("session.id", ondelete="CASCADE"), nullable=False
        ),
    )
    status: RunStatus = Field(default=RunStatus.CREATED)

    # Store the original user task
    task: Union[MessageConfig, dict] = Field(
        default_factory=MessageConfig, sa_column=Column(JSON)
    )

    # Store TeamResult which contains TaskResult
    team_result: Union[TeamResult, dict] = Field(default=None, sa_column=Column(JSON))

    error_message: Optional[str] = None
    version: Optional[str] = "0.0.1"
    messages: Union[List[Message], List[dict]] = Field(
        default_factory=list, sa_column=Column(JSON)
    )

    class Config:
        json_encoders = {UUID: str, datetime: lambda v: v.isoformat()}


class GalleryConfig(SQLModel, table=False):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    title: Optional[str] = None
    description: Optional[str] = None
    run: Run
    team: TeamConfig = None
    tags: Optional[List[str]] = None
    visibility: str = "public"  # public, private, shared

    class Config:
        json_encoders = {UUID: str, datetime: lambda v: v.isoformat()}


class Gallery(SQLModel, table=True):
    __table_args__ = {"sqlite_autoincrement": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now()),
    )
    user_id: Optional[str] = None
    version: Optional[str] = "0.0.1"
    config: Union[GalleryConfig, dict] = Field(
        default_factory=GalleryConfig, sa_column=Column(JSON)
    )
