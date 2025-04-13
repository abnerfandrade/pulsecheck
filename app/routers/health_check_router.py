from typing import Optional
from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.services.health_check import check_service
from app.schemas.health_check import HealthCheckRead
from app.core.database import get_session
from app.models.service import Service

router = APIRouter(prefix="/health_check", tags=["HealthCheck"])


@router.get("/", response_model=HealthCheckRead)
async def check_status(
    id_service: Optional[int] = Query(
        None, description="Execute the check on an existing registered service " \
                          "by filtering with the service ID"
    ),
    url: Optional[str] = Query(
        None, description="URL of the service/site to be checked. " \
                          "The protocol must be included at the beginning, e.g., https://"
    ),
    session: AsyncSession = Depends(get_session)
):
    if id_service:
        result = await session.execute(select(Service).where(Service.id == id_service))
        service = result.scalars().first()
        url = service.url

    response = await check_service(url)

    return response
