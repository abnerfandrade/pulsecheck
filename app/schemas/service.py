from datetime import datetime
from pydantic import BaseModel


class ServiceCreate(BaseModel):
    name: str
    url: str
    frequency: int


class ServiceRead(ServiceCreate):
    id: int
    created_at: datetime

    class ConfigDict:
        from_attributes = True
