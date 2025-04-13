from fastapi import APIRouter, Query
from app.services.health_check import check_service
from app.schemas.health_check import HealthCheckRead

router = APIRouter(prefix="/health_check", tags=["HealthCheck"])


@router.get("/", response_model=HealthCheckRead)
async def check_status(
    url: str = Query(description="URL of the service/site to be checked. " \
                                 "The protocol must be included at the beginning, e.g., https://")
):
    response = await check_service(url)

    return response
