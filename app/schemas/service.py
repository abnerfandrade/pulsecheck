from pydantic import BaseModel
from datetime import datetime


class ServiceCreate(BaseModel):
    name: str
    url: str
    frequency: int


class ServiceRead(ServiceCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
