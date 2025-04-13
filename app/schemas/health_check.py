from pydantic import BaseModel


class HealthCheckRead(BaseModel):
    status: int
    success: bool
