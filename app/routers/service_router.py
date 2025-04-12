from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.service import ServiceCreate, ServiceRead
from app.models.service import Service
from app.core.database import get_session

router = APIRouter(prefix="/services", tags=["Services"])

@router.post("/", response_model=ServiceRead)
async def create_service(service: ServiceCreate, session: AsyncSession = Depends(get_session)):
    new_service = Service(
        name=service.name,
        url=service.url,
        frequency=service.frequency
    )

    session.add(new_service)
    await session.commit()
    await session.refresh(new_service)

    return new_service

@router.get("/")
async def list_services():
    return {"response": "teste get"}
