from datetime import datetime
from typing import Any, Literal

from .._models import BaseModel


class DeploymentCreateParams(BaseModel):
    strategy_name: str
    strategy_version: str
    agent_name: str
    deployment_name: str
    config: dict[str, Any]


class DeploymentCreated(BaseModel):
    id: str
    strategy_name: str
    strategy_version: str
    agent_name: str
    deployment_name: str
    status: str
    created_at: datetime


class LogEntry(BaseModel):
    timestamp: datetime
    level: str
    message: str


class DeploymentLogs(BaseModel):
    deployment_id: str
    logs: list[LogEntry]


class MetricEntry(BaseModel):
    timestamp: datetime
    name: str
    value: float


class DeploymentMetrics(BaseModel):
    deployment_id: str
    metrics: list[MetricEntry]


class DeploymentHeartbeat(BaseModel):
    deployment_id: str
    last_heartbeat: datetime
    status: str


class Deployment(BaseModel):
    id: str
    strategy_name: str
    strategy_version: str
    agent_name: str
    deployment_name: str
    status: str
    created_at: datetime
    last_heartbeat: datetime | None


class DeploymentList(BaseModel):
    data: list[Deployment]
    object: Literal["list"]


class DeploymentStopped(BaseModel):
    deployment_id: str
    status: str
    stopped_at: datetime
