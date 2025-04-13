from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
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

@router.get("/", response_model=list[ServiceRead])
async def list_services(
    name: Optional[str] = Query(None, description="Filter by service name"),
    url: Optional[str] = Query(None, description="Filter by service URL"),
    session: AsyncSession = Depends(get_session)
):
    query = select(Service)

    if name:
        query = query.where(Service.name.ilike(f"%{name}%"))

    if url:
        query = query.where(Service.url.ilike(f"%{url}%"))

    result = await session.execute(query)
    services = result.scalars().all()

    return services

@router.get("/{id_service}", response_model=ServiceRead)
async def read_service(id_service: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Service).where(Service.id == id_service))
    service = result.scalars().first()

    return service
