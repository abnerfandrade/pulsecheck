from enum import Enum
from pydantic import BaseModel


class HealthCheckRead(BaseModel):
    status: int
    success: bool


class ListCheckLogs(BaseModel):
    _id: str
    service_id: int
    url: str
    status: int
    success: bool
    created_at: str


class SuccessStatus(str, Enum):
    true = "true"
    false = "false"
