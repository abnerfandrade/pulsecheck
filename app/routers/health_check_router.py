import re
from typing import Optional
from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.services.health_check import check_service
from app.schemas.health_check import (
    HealthCheckRead, ListCheckLogs, SuccessStatus
)
from app.core.database import get_session
from app.models.service import Service
from app.services.mongo_client import logs_collection

router = APIRouter(prefix="/health_check", tags=["HealthCheck"])


@router.get(
    "/",
    summary="Execute a health check on an URL without saving log",
    response_model=HealthCheckRead
)
async def check_status(
    service_id: Optional[int] = Query(
        None,
        description="Execute the check on an existing registered service "
                    "by filtering with the service ID"
    ),
    url: Optional[str] = Query(
        None,
        description="URL of the service/site to be checked. The protocol "
                    "must be included at the beginning, e.g., https://"
    ),
    session: AsyncSession = Depends(get_session)
):
    if service_id:
        result = await session.execute(
            select(Service).where(Service.id == service_id)
        )
        service = result.scalars().first()
        url = service.url

    response = await check_service(url)

    return response


@router.get(
    "/logs",
    summary="Return heath check logs",
    response_model=list[ListCheckLogs]
)
async def list_check_logs(
    service_id: Optional[int] = Query(
        None, description="Filter logs by service ID"
    ),
    url: Optional[str] = Query(
        None, description="Filter logs by URL"
    ),
    success: SuccessStatus = Query(
        None, description="Filter logs by success status"
    )
):
    query = {}

    if service_id is not None:
        query["service_id"] = service_id

    if url:
        query["url"] = {"$regex": re.escape(url), "$options": "i"}

    if success is not None:
        query["success"] = success == SuccessStatus.true

    cursor = logs_collection.find(query).sort("created_at", -1).limit(100)

    logs = []
    async for log in cursor:
        log["_id"] = str(log["_id"])
        logs.append(log)

    return logs
